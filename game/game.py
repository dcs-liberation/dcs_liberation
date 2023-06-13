from __future__ import annotations

import itertools
import logging
import math
from collections.abc import Iterator
from datetime import date, datetime, time, timedelta
from typing import Any, List, TYPE_CHECKING, Type, Union, cast

from dcs.countries import Switzerland, USAFAggressors, UnitedNationsPeacekeepers
from dcs.country import Country
from dcs.mapping import Point
from dcs.task import CAP, CAS, PinpointStrike
from dcs.vehicles import AirDefence
from faker import Faker

from game.ato.closestairfields import ObjectiveDistanceCache
from game.models.game_stats import GameStats
from game.plugins import LuaPluginManager
from game.utils import Distance
from . import naming
from .ato.flighttype import FlightType
from .campaignloader import CampaignAirWingConfig
from .coalition import Coalition
from .db.gamedb import GameDb
from .infos.information import Information
from .persistence import SaveManager
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
from .timeofday import TimeOfDay
from .turnstate import TurnState
from .weather.conditions import Conditions

if TYPE_CHECKING:
    from .ato.airtaaskingorder import AirTaskingOrder
    from .factions.faction import Faction
    from .navmesh import NavMesh
    from .sim import GameUpdateEvents
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


class Game:
    def __init__(
        self,
        player_faction: Faction,
        enemy_faction: Faction,
        theater: ConflictTheater,
        air_wing_config: CampaignAirWingConfig,
        start_date: datetime,
        start_time: time | None,
        settings: Settings,
        lua_plugin_manager: LuaPluginManager,
        player_budget: float,
        enemy_budget: float,
    ) -> None:
        self.settings = settings
        self.lua_plugin_manager = lua_plugin_manager
        self.theater = theater
        self.turn = 0
        # NB: This is the *start* date. It is never updated.
        self.date = date(start_date.year, start_date.month, start_date.day)
        self.game_stats = GameStats()
        self.notes = ""
        self.informations: list[Information] = []
        self.message("Game Start", "-" * 40)
        # Culling Zones are for areas around points of interest that contain things we may not wish to cull.
        self.__culling_zones: List[Point] = []
        self.__destroyed_units: list[dict[str, Union[float, str]]] = []
        self.save_manager = SaveManager(self)
        self.current_unit_id = 0
        self.current_group_id = 0
        self.name_generator = naming.namegen

        self.db = GameDb()

        if start_time is None:
            self.time_of_day_offset_for_start_time = list(TimeOfDay).index(
                TimeOfDay.Day
            )
        else:
            self.time_of_day_offset_for_start_time = list(TimeOfDay).index(
                self.theater.daytime_map.best_guess_time_of_day_at(start_time)
            )
        self.conditions = self.generate_conditions(forced_time=start_time)

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

    def point_in_world(self, x: float, y: float) -> Point:
        return Point(x, y, self.theater.terrain)

    def ato_for(self, player: bool) -> AirTaskingOrder:
        return self.coalition_for(player).ato

    def transit_network_for(self, player: bool) -> TransitNetwork:
        return self.coalition_for(player).transit_network

    def generate_conditions(self, forced_time: time | None = None) -> Conditions:
        return Conditions.generate(
            self.theater,
            self.current_day,
            self.current_turn_time_of_day,
            self.settings,
            forced_time=forced_time,
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
        from .sim import GameUpdateEvents

        if not hasattr(self, "name_generator"):
            self.name_generator = naming.namegen
        # Hack: Replace the global name generator state with the state from the save
        # game.
        #
        # We need to persist this state so that names generated after game load don't
        # conflict with those generated before exit.
        naming.namegen = self.name_generator

        # The installed plugins may have changed between runs. We need to load the
        # current configuration and patch in the options that were previously set.
        new_plugin_manager = LuaPluginManager.load()
        new_plugin_manager.update_with(self.lua_plugin_manager)
        self.lua_plugin_manager = new_plugin_manager

        ObjectiveDistanceCache.set_theater(self.theater)
        self.compute_unculled_zones(GameUpdateEvents())
        if not game_still_initializing:
            # We don't need to push events that happen during load. The UI will fully
            # reset when we're done.
            self.compute_threat_zones(GameUpdateEvents())

    def finish_turn(self, events: GameUpdateEvents, skipped: bool = False) -> None:
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
                for front_line in cp.front_lines.values():
                    front_line.update_position()
                    events.update_front_line(front_line)
                cp.base.affect_strength(+PLAYER_BASE_STRENGTH_RECOVERY)

        # We don't actually advance time or change the conditions between turn 0 and
        # turn 1.
        if self.turn > 1:
            self.conditions = self.generate_conditions()

    def begin_turn_0(self, squadrons_start_full: bool) -> None:
        """Initialization for the first turn of the game."""
        from .sim import GameUpdateEvents

        # Build the IADS Network
        with logged_duration("Generate IADS Network"):
            self.theater.iads_network.initialize_network(self.theater.ground_objects)

        for control_point in self.theater.controlpoints:
            control_point.initialize_turn_0()
            for tgo in control_point.connected_objectives:
                self.db.tgos.add(tgo.id, tgo)

        # Correct the heading of specifc TGOs, can only be done after init turn 0
        for tgo in self.theater.ground_objects:
            # If heading is 0 then we change the orientation to head towards the
            # closest conflict. Heading of 0 means that the campaign designer wants
            # to determine the heading automatically by liberation. Values other
            # than 0 mean it is custom defined.
            if tgo.should_head_to_conflict and tgo.heading.degrees == 0:
                # Calculate the heading to conflict
                heading = self.theater.heading_to_conflict_from(tgo.position)
                # Rotate the whole TGO with the new heading
                tgo.rotate(heading or tgo.heading)

        self.blue.preinit_turn_0(squadrons_start_full)
        self.red.preinit_turn_0(squadrons_start_full)
        # TODO: Check for overfull bases.
        # We don't need to actually stream events for turn zero because we haven't given
        # *any* state to the UI yet, so it will need to do a full draw once we do.
        self.initialize_turn(GameUpdateEvents())

    def save_last_turn_state(self) -> None:
        self.save_manager.save_last_turn()

    def pass_turn(self, no_action: bool = False) -> None:
        """Ends the current turn and initializes the new turn.

        Called both when skipping a turn or by ending the turn as the result of combat.

        Args:
            no_action: True if the turn was skipped.
        """
        from .server import EventStream
        from .sim import GameUpdateEvents

        if no_action:
            # Only save the last turn state if the turn was skipped. Otherwise, we'll
            # end up saving the game after we've already applied the results, making
            # this useless...
            self.save_manager.save_last_turn()

        events = GameUpdateEvents()

        logging.info("Pass turn")
        with logged_duration("Turn finalization"):
            self.finish_turn(events, no_action)

        with logged_duration("Turn initialization"):
            self.initialize_turn(events)

        EventStream.put_nowait(events)

        self.save_manager.save_start_of_turn()

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

    def initialize_turn(
        self,
        events: GameUpdateEvents,
        for_red: bool = True,
        for_blue: bool = True,
    ) -> None:
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
            events: Game update event container for turn initialization.
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
            self.compute_threat_zones(events)

        # Plan Coalition specific turn
        if for_blue:
            self.blue.initialize_turn(self.turn == 0)
        if for_red:
            self.red.initialize_turn(self.turn == 0)

        # Update cull zones
        with logged_duration("Computing culling positions"):
            self.compute_unculled_zones(events)

        events.begin_new_turn()

    def message(self, title: str, text: str = "") -> None:
        self.informations.append(Information(title, text, turn=self.turn))

    @property
    def current_turn_time_of_day(self) -> TimeOfDay:
        tod_turn = max(0, self.turn - 1) + self.time_of_day_offset_for_start_time
        return list(TimeOfDay)[tod_turn % 4]

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

    def compute_threat_zones(self, events: GameUpdateEvents) -> None:
        self.blue.compute_threat_zones(events)
        self.red.compute_threat_zones(events)
        self.blue.compute_nav_meshes(events)
        self.red.compute_nav_meshes(events)

    def threat_zone_for(self, player: bool) -> ThreatZones:
        return self.coalition_for(player).threat_zone

    def navmesh_for(self, player: bool) -> NavMesh:
        return self.coalition_for(player).nav_mesh

    def compute_unculled_zones(self, events: GameUpdateEvents) -> None:
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
                        cpoint = cp.position.midpoint(cp2.position)
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

        self.__culling_zones = zones
        events.update_unculled_zones(zones)

    def add_destroyed_units(self, data: dict[str, Union[float, str]]) -> None:
        pos = Point(
            cast(float, data["x"]), cast(float, data["z"]), self.theater.terrain
        )
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

    def iads_considerate_culling(self, tgo: TheaterGroundObject) -> bool:
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
