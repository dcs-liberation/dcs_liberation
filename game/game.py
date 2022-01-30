from __future__ import annotations

import itertools
import logging
import math
from collections.abc import Iterator
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, List, TYPE_CHECKING, Type, TypeVar, Union, cast

from dcs.countries import Switzerland, USAFAggressors, UnitedNationsPeacekeepers
from dcs.country import Country
from dcs.mapping import Point
from dcs.task import CAP, CAS, PinpointStrike
from dcs.vehicles import AirDefence
from faker import Faker

from game.models.game_stats import GameStats
from game.plugins import LuaPluginManager
from game.utils import Distance
from gen import naming
from gen.flights.closestairfields import ObjectiveDistanceCache
from gen.ground_forces.ai_ground_planner import GroundPlanner
from . import persistency
from .ato.flighttype import FlightType
from .campaignloader import CampaignAirWingConfig
from .coalition import Coalition
from .factions.faction import Faction
from .infos.information import Information
from .profiling import logged_duration
from .settings import Settings
from .theater import ConflictTheater
from .theater.bullseye import Bullseye
from .theater.theatergroundobject import (
    EwrGroundObject,
    SamGroundObject,
    TheaterGroundObject,
)
from .theater.transitnetwork import TransitNetwork, TransitNetworkBuilder
from .weather import Conditions, TimeOfDay

if TYPE_CHECKING:
    from .ato.airtaaskingorder import AirTaskingOrder
    from .navmesh import NavMesh
    from .squadrons import AirWing
    from .threatzones import ThreatZones

COMMISION_UNIT_VARIETY = 4
COMMISION_LIMITS_SCALE = 1.5
COMMISION_LIMITS_FACTORS = {
    PinpointStrike: 10,
    CAS: 5,
    CAP: 8,
    AirDefence: 8,
}

COMMISION_AMOUNTS_SCALE = 1.5
COMMISION_AMOUNTS_FACTORS = {
    PinpointStrike: 3,
    CAS: 1,
    CAP: 2,
    AirDefence: 0.8,
}

PLAYER_INTERCEPT_GLOBAL_PROBABILITY_BASE = 30
PLAYER_INTERCEPT_GLOBAL_PROBABILITY_LOG = 2
PLAYER_BASEATTACK_THRESHOLD = 0.4

# amount of strength player bases recover for the turn
PLAYER_BASE_STRENGTH_RECOVERY = 0.2

# amount of strength enemy bases recover for the turn
ENEMY_BASE_STRENGTH_RECOVERY = 0.05

# cost of AWACS for single operation
AWACS_BUDGET_COST = 4

# Bonus multiplier logarithm base
PLAYER_BUDGET_IMPORTANCE_LOG = 2


class TurnState(Enum):
    WIN = 0
    LOSS = 1
    CONTINUE = 2


class Game:
    def __init__(
        self,
        player_faction: Faction,
        enemy_faction: Faction,
        theater: ConflictTheater,
        air_wing_config: CampaignAirWingConfig,
        start_date: datetime,
        settings: Settings,
        player_budget: float,
        enemy_budget: float,
    ) -> None:
        self.settings = settings
        self.theater = theater
        self.turn = 0
        # NB: This is the *start* date. It is never updated.
        self.date = date(start_date.year, start_date.month, start_date.day)
        self.game_stats = GameStats()
        self.notes = ""
        self.ground_planners: dict[int, GroundPlanner] = {}
        self.informations: list[Information] = []
        self.message("Game Start", "-" * 40)
        # Culling Zones are for areas around points of interest that contain things we may not wish to cull.
        self.__culling_zones: List[Point] = []
        self.__destroyed_units: list[dict[str, Union[float, str]]] = []
        self.savepath = ""
        self.current_unit_id = 0
        self.current_group_id = 0
        self.name_generator = naming.namegen

        self.conditions = self.generate_conditions()

        self.sanitize_sides(player_faction, enemy_faction)
        self.blue = Coalition(self, player_faction, player_budget, player=True)
        self.red = Coalition(self, enemy_faction, enemy_budget, player=False)
        self.blue.set_opponent(self.red)
        self.red.set_opponent(self.blue)

        for control_point in self.theater.controlpoints:
            control_point.finish_init(self)

        self.blue.configure_default_air_wing(air_wing_config)
        self.red.configure_default_air_wing(air_wing_config)

        self.on_load(game_still_initializing=True)

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        # Regenerate any state that was not persisted.
        self.on_load()

    @property
    def coalitions(self) -> Iterator[Coalition]:
        yield self.blue
        yield self.red

    def ato_for(self, player: bool) -> AirTaskingOrder:
        return self.coalition_for(player).ato

    def transit_network_for(self, player: bool) -> TransitNetwork:
        return self.coalition_for(player).transit_network

    def generate_conditions(self) -> Conditions:
        return Conditions.generate(
            self.theater, self.current_day, self.current_turn_time_of_day, self.settings
        )

    @staticmethod
    def sanitize_sides(player_faction: Faction, enemy_faction: Faction) -> None:
        """
        Make sure the opposing factions are using different countries
        :return:
        """
        if player_faction.country == enemy_faction.country:
            if player_faction.country == "USA":
                enemy_faction.country = "USAF Aggressors"
            elif player_faction.country == "Russia":
                enemy_faction.country = "USSR"
            else:
                enemy_faction.country = "Russia"

    def faction_for(self, player: bool) -> Faction:
        return self.coalition_for(player).faction

    def faker_for(self, player: bool) -> Faker:
        return self.coalition_for(player).faker

    def air_wing_for(self, player: bool) -> AirWing:
        return self.coalition_for(player).air_wing

    def country_for(self, player: bool) -> str:
        return self.coalition_for(player).country_name

    def bullseye_for(self, player: bool) -> Bullseye:
        return self.coalition_for(player).bullseye

    @property
    def neutral_country(self) -> Type[Country]:
        """Return the best fitting country that can be used as neutral faction in the generated mission"""
        countries_in_use = [self.red.country_name, self.blue.country_name]
        if UnitedNationsPeacekeepers not in countries_in_use:
            return UnitedNationsPeacekeepers
        elif Switzerland.name not in countries_in_use:
            return Switzerland
        else:
            return USAFAggressors

    def coalition_for(self, player: bool) -> Coalition:
        if player:
            return self.blue
        return self.red

    def adjust_budget(self, amount: float, player: bool) -> None:
        self.coalition_for(player).adjust_budget(amount)

    def on_load(self, game_still_initializing: bool = False) -> None:
        if not hasattr(self, "name_generator"):
            self.name_generator = naming.namegen
        # Hack: Replace the global name generator state with the state from the save
        # game.
        #
        # We need to persist this state so that names generated after game load don't
        # conflict with those generated before exit.
        naming.namegen = self.name_generator
        LuaPluginManager.load_settings(self.settings)
        ObjectiveDistanceCache.set_theater(self.theater)
        self.compute_unculled_zones()
        if not game_still_initializing:
            self.compute_threat_zones()

    def finish_turn(self, skipped: bool = False) -> None:
        """Finalizes the current turn and advances to the next turn.

        This handles the turn-end portion of passing a turn. Initialization of the next
        turn is handled by `initialize_turn`. These are separate processes because while
        turns may be initialized more than once under some circumstances (see the
        documentation for `initialize_turn`), `finish_turn` performs the work that
        should be guaranteed to happen only once per turn:

        * Turn counter increment.
        * Delivering units ordered the previous turn.
        * Transfer progress.
        * Squadron replenishment.
        * Income distribution.
        * Base strength (front line position) adjustment.
        * Weather/time-of-day generation.

        Some actions (like transit network assembly) will happen both here and in
        `initialize_turn`. We need the network to be up to date so we can account for
        base captures when processing the transfers that occurred last turn, but we also
        need it to be up to date in the case of a re-initialization in `initialize_turn`
        (such as to account for a cheat base capture) so that orders are only placed
        where a supply route exists to the destination. This is a relatively cheap
        operation so duplicating the effort is not a problem.

        Args:
            skipped: True if the turn was skipped.
        """
        self.message("End of turn #" + str(self.turn), "-" * 40)
        self.turn += 1

        # The coalition-specific turn finalization *must* happen before unit deliveries,
        # since the coalition-specific finalization handles transit network updates and
        # transfer processing. If in the other order, units may be delivered to captured
        # bases, and freshly delivered units will spawn one leg through their journey.
        self.blue.end_turn()
        self.red.end_turn()

        for control_point in self.theater.controlpoints:
            control_point.process_turn(self)

        if not skipped:
            for cp in self.theater.player_points():
                cp.base.affect_strength(+PLAYER_BASE_STRENGTH_RECOVERY)

        self.conditions = self.generate_conditions()

    def begin_turn_0(self) -> None:
        """Initialization for the first turn of the game."""
        self.blue.preinit_turn_0()
        self.red.preinit_turn_0()
        self.initialize_turn()

    def pass_turn(self, no_action: bool = False) -> None:
        """Ends the current turn and initializes the new turn.

        Called both when skipping a turn or by ending the turn as the result of combat.

        Args:
            no_action: True if the turn was skipped.
        """
        logging.info("Pass turn")
        with logged_duration("Turn finalization"):
            self.finish_turn(no_action)
        with logged_duration("Turn initialization"):
            self.initialize_turn()

        # Autosave progress
        persistency.autosave(self)

    def check_win_loss(self) -> TurnState:
        player_airbases = {
            cp for cp in self.theater.player_points() if cp.runway_is_operational()
        }
        if not player_airbases:
            return TurnState.LOSS

        enemy_airbases = {
            cp for cp in self.theater.enemy_points() if cp.runway_is_operational()
        }
        if not enemy_airbases:
            return TurnState.WIN

        return TurnState.CONTINUE

    def set_bullseye(self) -> None:
        player_cp, enemy_cp = self.theater.closest_opposing_control_points()
        self.blue.bullseye = Bullseye(enemy_cp.position)
        self.red.bullseye = Bullseye(player_cp.position)

    def initialize_turn(self, for_red: bool = True, for_blue: bool = True) -> None:
        """Performs turn initialization for the specified players.

        Turn initialization performs all of the beginning-of-turn actions. *End-of-turn*
        processing happens in `pass_turn` (despite the name, it's called both for
        skipping the turn and ending the turn after combat).

        Special care needs to be taken here because initialization can occur more than
        once per turn. A number of events can require re-initializing a turn:

        * Cheat capture. Bases changing hands invalidates many missions in both ATOs,
          purchase orders, threat zones, transit networks, etc. Practically speaking,
          after a base capture the turn needs to be treated as fully new. The game might
          even be over after a capture.
        * Cheat front line position. CAS missions are no longer in the correct location,
          and the ground planner may also need changes.
        * Selling/buying units at TGOs. Selling a TGO might leave missions in the ATO
          with invalid targets. Buying a new SAM (or even replacing some units in a SAM)
          potentially changes the threat zone and may alter mission priorities and
          flight planning.

        Most of the work is delegated to initialize_turn_for, which handles the
        coalition-specific turn initialization. In some cases only one coalition will be
        (re-) initialized. This is the case when buying or selling TGO units, since we
        don't want to force the player to redo all their planning just because they
        repaired a SAM, but should replan opfor when that happens. On the other hand,
        base captures are significant enough (and likely enough to be the first thing
        the player does in a turn) that we replan blue as well. Front lines are less
        impactful but also likely to be early, so they also cause a blue replan.

        Args:
            for_red: True if opfor should be re-initialized.
            for_blue: True if the player coalition should be re-initialized.
        """
        self.set_bullseye()

        # Update statistics
        self.game_stats.update(self)

        # Check for win or loss condition
        turn_state = self.check_win_loss()
        if turn_state in (TurnState.LOSS, TurnState.WIN):
            return self.process_win_loss(turn_state)

        # Plan flights & combat for next turn
        with logged_duration("Threat zone computation"):
            self.compute_threat_zones()

        # Plan Coalition specific turn
        if for_blue:
            self.blue.initialize_turn()
        if for_red:
            self.red.initialize_turn()

        # Plan GroundWar
        self.ground_planners = {}
        for cp in self.theater.controlpoints:
            if cp.has_frontline:
                gplanner = GroundPlanner(cp, self)
                gplanner.plan_groundwar()
                self.ground_planners[cp.id] = gplanner

        # Update cull zones
        with logged_duration("Computing culling positions"):
            self.compute_unculled_zones()

    def message(self, title: str, text: str = "") -> None:
        self.informations.append(Information(title, text, turn=self.turn))

    @property
    def current_turn_time_of_day(self) -> TimeOfDay:
        return list(TimeOfDay)[self.turn % 4]

    @property
    def current_day(self) -> date:
        return self.date + timedelta(days=self.turn // 4)

    def next_unit_id(self) -> int:
        """
        Next unit id for pre-generated units
        """
        self.current_unit_id += 1
        return self.current_unit_id

    def next_group_id(self) -> int:
        """
        Next unit id for pre-generated units
        """
        self.current_group_id += 1
        return self.current_group_id

    def compute_transit_network_for(self, player: bool) -> TransitNetwork:
        return TransitNetworkBuilder(self.theater, player).build()

    def compute_threat_zones(self) -> None:
        self.blue.compute_threat_zones()
        self.red.compute_threat_zones()
        self.blue.compute_nav_meshes()
        self.red.compute_nav_meshes()

    def threat_zone_for(self, player: bool) -> ThreatZones:
        return self.coalition_for(player).threat_zone

    def navmesh_for(self, player: bool) -> NavMesh:
        return self.coalition_for(player).nav_mesh

    def compute_unculled_zones(self) -> None:
        """
        Compute the current conflict position(s) used for culling calculation
        """
        from game.missiongenerator.frontlineconflictdescription import (
            FrontLineConflictDescription,
        )

        zones = []

        # By default, use the existing frontline conflict position
        for front_line in self.theater.conflicts():
            position = FrontLineConflictDescription.frontline_position(
                front_line, self.theater
            )
            zones.append(position[0])
            zones.append(front_line.blue_cp.position)
            zones.append(front_line.red_cp.position)

        for cp in self.theater.controlpoints:
            # If do_not_cull_carrier is enabled, add carriers as culling point
            if self.settings.perf_do_not_cull_carrier:
                if cp.is_carrier or cp.is_lha:
                    zones.append(cp.position)

        # If there is no conflict take the center point between the two nearest opposing bases
        if len(zones) == 0:
            cpoint = None
            min_distance = math.inf
            for cp in self.theater.player_points():
                for cp2 in self.theater.enemy_points():
                    d = cp.position.distance_to_point(cp2.position)
                    if d < min_distance:
                        min_distance = d
                        cpoint = Point(
                            (cp.position.x + cp2.position.x) / 2,
                            (cp.position.y + cp2.position.y) / 2,
                        )
                        zones.append(cp.position)
                        zones.append(cp2.position)
                        break
                if cpoint is not None:
                    break
            if cpoint is not None:
                zones.append(cpoint)

        packages = itertools.chain(self.blue.ato.packages, self.red.ato.packages)
        for package in packages:
            if package.primary_task is FlightType.BARCAP:
                # BARCAPs will be planned at most locations on smaller theaters,
                # rendering culling fairly useless. BARCAP packages don't really
                # need the ground detail since they're defensive. SAMs nearby
                # are only interesting if there are enemies in the area, and if
                # there are they won't be culled because of the enemy's mission.
                continue
            zones.append(package.target.position)

        # Else 0,0, since we need a default value
        # (in this case this means the whole map is owned by the same player, so it is not an issue)
        if len(zones) == 0:
            zones.append(Point(0, 0))

        self.__culling_zones = zones

    def add_destroyed_units(self, data: dict[str, Union[float, str]]) -> None:
        pos = Point(cast(float, data["x"]), cast(float, data["z"]))
        if self.theater.is_on_land(pos):
            self.__destroyed_units.append(data)

    def get_destroyed_units(self) -> list[dict[str, Union[float, str]]]:
        return self.__destroyed_units

    def position_culled(self, pos: Point) -> bool:
        """
        Check if unit can be generated at given position depending on culling performance settings
        :param pos: Position you are tryng to spawn stuff at
        :return: True if units can not be added at given position
        """
        if not self.settings.perf_culling:
            return False
        for z in self.__culling_zones:
            if z.distance_to_point(pos) < self.settings.perf_culling_distance * 1000:
                return False
        return True

    def iads_considerate_culling(self, tgo: TheaterGroundObject[Any]) -> bool:
        if not self.settings.perf_do_not_cull_threatening_iads:
            return self.position_culled(tgo.position)
        else:
            if self.settings.perf_culling:
                if isinstance(tgo, EwrGroundObject):
                    max_detection_range = tgo.max_detection_range().meters
                    for z in self.__culling_zones:
                        seperation = z.distance_to_point(tgo.position)
                        # Don't cull EWR if in detection range.
                        if seperation < max_detection_range:
                            return False
                if isinstance(tgo, SamGroundObject):
                    max_threat_range = tgo.max_threat_range().meters
                    for z in self.__culling_zones:
                        seperation = z.distance_to_point(tgo.position)
                        # Create a 12nm buffer around nearby SAMs.
                        respect_bubble = (
                            max_threat_range + Distance.from_nautical_miles(12).meters
                        )
                        if seperation < respect_bubble:
                            return False
            return self.position_culled(tgo.position)

    def get_culling_zones(self) -> list[Point]:
        """
        Check culling points
        :return: List of culling zones
        """
        return self.__culling_zones

    def process_win_loss(self, turn_state: TurnState) -> None:
        if turn_state is TurnState.WIN:
            self.message(
                "Congratulations, you are victorious! Start a new campaign to continue."
            )
        elif turn_state is TurnState.LOSS:
            self.message("Game Over, you lose. Start a new campaign to continue.")
