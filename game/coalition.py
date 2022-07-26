from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from faker import Faker

from game.armedforces.armedforces import ArmedForces
from game.ato.airtaaskingorder import AirTaskingOrder
from game.campaignloader.defaultsquadronassigner import DefaultSquadronAssigner
from game.commander import TheaterCommander
from game.commander.missionscheduler import MissionScheduler
from game.income import Income
from game.navmesh import NavMesh
from game.orderedset import OrderedSet
from game.procurement import AircraftProcurementRequest, ProcurementAi
from game.profiling import MultiEventTracer, logged_duration
from game.squadrons import AirWing
from game.theater.bullseye import Bullseye
from game.theater.transitnetwork import TransitNetwork, TransitNetworkBuilder
from game.threatzones import ThreatZones
from game.transfers import PendingTransfers

if TYPE_CHECKING:
    from .campaignloader import CampaignAirWingConfig
    from .data.doctrine import Doctrine
    from .factions.faction import Faction
    from .game import Game
    from .sim import GameUpdateEvents


class Coalition:
    def __init__(
        self, game: Game, faction: Faction, budget: float, player: bool
    ) -> None:
        self.game = game
        self.player = player
        self.faction = faction
        self.budget = budget
        self.ato = AirTaskingOrder()
        self.transit_network = TransitNetwork()
        self.procurement_requests: OrderedSet[AircraftProcurementRequest] = OrderedSet()
        self.bullseye = Bullseye(self.game.point_in_world(0, 0))
        self.faker = Faker(self.faction.locales)
        self.air_wing = AirWing(player, game, self.faction)
        self.armed_forces = ArmedForces(self.faction)
        self.transfers = PendingTransfers(game, player)

        # Late initialized because the two coalitions in the game are mutually
        # dependent, so must be both constructed before this property can be set.
        self._opponent: Optional[Coalition] = None

        # Volatile properties that are not persisted to the save file since they can be
        # recomputed on load. Keeping this data out of the save file makes save compat
        # breaks less frequent. Each of these properties has a non-underscore-prefixed
        # @property that should be used for non-Optional access.
        #
        # All of these are late-initialized (whether via on_load or called later), but
        # will be non-None after the game has finished loading.
        self._threat_zone: Optional[ThreatZones] = None
        self._navmesh: Optional[NavMesh] = None
        self.on_load()

    @property
    def doctrine(self) -> Doctrine:
        return self.faction.doctrine

    @property
    def coalition_id(self) -> int:
        if self.player:
            return 2
        return 1

    @property
    def country_name(self) -> str:
        return self.faction.country

    @property
    def opponent(self) -> Coalition:
        assert self._opponent is not None
        return self._opponent

    @property
    def threat_zone(self) -> ThreatZones:
        assert self._threat_zone is not None
        return self._threat_zone

    @property
    def nav_mesh(self) -> NavMesh:
        assert self._navmesh is not None
        return self._navmesh

    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        # Avoid persisting any volatile types that can be deterministically
        # recomputed on load for the sake of save compatibility.
        del state["_threat_zone"]
        del state["_navmesh"]
        del state["faker"]
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        # Regenerate any state that was not persisted.
        self.on_load()

    def on_load(self) -> None:
        self.faker = Faker(self.faction.locales)

    def set_opponent(self, opponent: Coalition) -> None:
        if self._opponent is not None:
            raise RuntimeError("Double-initialization of Coalition.opponent")
        self._opponent = opponent

    def configure_default_air_wing(
        self, air_wing_config: CampaignAirWingConfig
    ) -> None:
        DefaultSquadronAssigner(air_wing_config, self.game, self).assign()

    def adjust_budget(self, amount: float) -> None:
        self.budget += amount

    def compute_threat_zones(self, events: GameUpdateEvents) -> None:
        self._threat_zone = ThreatZones.for_faction(self.game, self.player)
        events.update_threat_zones(self.player, self._threat_zone)

    def compute_nav_meshes(self, events: GameUpdateEvents) -> None:
        self._navmesh = NavMesh.from_threat_zones(
            self.opponent.threat_zone, self.game.theater
        )
        events.update_navmesh(self.player, self._navmesh)

    def update_transit_network(self) -> None:
        self.transit_network = TransitNetworkBuilder(
            self.game.theater, self.player
        ).build()

    def set_bullseye(self, bullseye: Bullseye) -> None:
        self.bullseye = bullseye

    def end_turn(self) -> None:
        """Processes coalition-specific turn finalization.

        For more information on turn finalization in general, see the documentation for
        `Game.finish_turn`.
        """
        self.air_wing.end_turn()
        self.budget += Income(self.game, self.player).total

        # Need to recompute before transfers and deliveries to account for captures.
        # This happens in in initialize_turn as well, because cheating doesn't advance a
        # turn but can capture bases so we need to recompute there as well.
        self.update_transit_network()

        # Must happen *before* unit deliveries are handled, or else new units will spawn
        # one hop ahead. ControlPoint.process_turn handles unit deliveries. The
        # coalition-specific turn-end happens before the theater-wide turn-end, so this
        # is handled correctly.
        self.transfers.perform_transfers()

    def preinit_turn_0(self) -> None:
        """Runs final Coalition initialization.

        Final initialization occurs before Game.initialize_turn runs for turn 0.
        """
        self.air_wing.populate_for_turn_0()

    def initialize_turn(self) -> None:
        """Processes coalition-specific turn initialization.

        For more information on turn initialization in general, see the documentation
        for `Game.initialize_turn`.
        """
        # Needs to happen *before* planning transfers so we don't cancel them.
        self.ato.clear()
        self.air_wing.reset()
        self.refund_outstanding_orders()
        self.procurement_requests.clear()

        with logged_duration("Transit network identification"):
            self.update_transit_network()
        with logged_duration("Procurement of airlift assets"):
            self.transfers.order_airlift_assets()
        with logged_duration("Transport planning"):
            self.transfers.plan_transports()

        self.plan_missions()
        self.plan_procurement()

    def refund_outstanding_orders(self) -> None:
        # TODO: Split orders between air and ground units.
        # This isn't quite right. If the player has ground purchases automated we should
        # be refunding the ground units, and if they have air automated but not ground
        # we should be refunding air units.
        if self.player and not self.game.settings.automate_aircraft_reinforcements:
            return

        for cp in self.game.theater.control_points_for(self.player):
            cp.ground_unit_orders.refund_all(self)
        for squadron in self.air_wing.iter_squadrons():
            squadron.refund_orders()

    def plan_missions(self) -> None:
        color = "Blue" if self.player else "Red"
        with MultiEventTracer() as tracer:
            with tracer.trace(f"{color} mission planning"):
                with tracer.trace(f"{color} mission identification"):
                    TheaterCommander(self.game, self.player).plan_missions(tracer)
                with tracer.trace(f"{color} mission scheduling"):
                    MissionScheduler(
                        self, self.game.settings.desired_player_mission_duration
                    ).schedule_missions()

    def plan_procurement(self) -> None:
        # The first turn needs to buy a *lot* of aircraft to fill CAPs, so it gets much
        # more of the budget that turn. Otherwise budget (after repairs) is split evenly
        # between air and ground. For the default starting budget of 2000 this gives 600
        # to ground forces and 1400 to aircraft. After that the budget will be spent
        # proportionally based on how much is already invested.

        if self.player:
            manage_runways = self.game.settings.automate_runway_repair
            manage_front_line = self.game.settings.automate_front_line_reinforcements
            manage_aircraft = self.game.settings.automate_aircraft_reinforcements
        else:
            manage_runways = True
            manage_front_line = True
            manage_aircraft = True

        self.budget = ProcurementAi(
            self.game,
            self.player,
            self.faction,
            manage_runways,
            manage_front_line,
            manage_aircraft,
        ).spend_budget(self.budget)

    def add_procurement_request(self, request: AircraftProcurementRequest) -> None:
        self.procurement_requests.add(request)
