from __future__ import annotations

import logging
import math
from typing import Dict, Iterator, List, TYPE_CHECKING, Tuple, Type

from dcs.mapping import Point
from dcs.task import Task
from dcs.unittype import UnitType

from game import persistency
from game.debriefing import AirLosses, Debriefing
from game.infos.information import Information
from game.operation.operation import Operation
from game.theater import ControlPoint
from gen import AirTaskingOrder
from gen.ground_forces.combat_stance import CombatStance
from ..db import PRICES
from ..unitmap import UnitMap

if TYPE_CHECKING:
    from ..game import Game


MINOR_DEFEAT_INFLUENCE = 0.1
DEFEAT_INFLUENCE = 0.3
STRONG_DEFEAT_INFLUENCE = 0.5


class Event:
    silent = False
    informational = False

    game = None  # type: Game
    location = None  # type: Point
    from_cp = None  # type: ControlPoint
    to_cp = None  # type: ControlPoint
    difficulty = 1  # type: int

    def __init__(self, game, from_cp: ControlPoint, target_cp: ControlPoint, location: Point, attacker_name: str, defender_name: str):
        self.game = game
        self.from_cp = from_cp
        self.to_cp = target_cp
        self.location = location
        self.attacker_name = attacker_name
        self.defender_name = defender_name

    @property
    def is_player_attacking(self) -> bool:
        return self.attacker_name == self.game.player_name

    @property
    def tasks(self) -> List[Type[Task]]:
        return []

    def generate(self) -> UnitMap:
        Operation.prepare(self.game)
        unit_map = Operation.generate()
        Operation.current_mission.save(
            persistency.mission_path_for("liberation_nextturn.miz"))
        return unit_map

    @staticmethod
    def _transfer_aircraft(ato: AirTaskingOrder, losses: AirLosses,
                           for_player: bool) -> None:
        for package in ato.packages:
            for flight in package.flights:
                # No need to transfer to the same location.
                if flight.departure == flight.arrival:
                    continue

                # Don't transfer to bases that were captured. Note that if the
                # airfield was back-filling transfers it may overflow. We could
                # attempt to be smarter in the future by performing transfers in
                # order up a graph to prevent transfers to full airports and
                # send overflow off-map, but overflow is fine for now.
                if flight.arrival.captured != for_player:
                    logging.info(
                        f"Not transferring {flight} because {flight.arrival} "
                        "was captured")
                    continue

                transfer_count = losses.surviving_flight_members(flight)
                if transfer_count < 0:
                    logging.error(f"{flight} had {flight.count} aircraft but "
                                  f"{transfer_count} losses were recorded.")
                    continue

                aircraft = flight.unit_type
                available = flight.departure.base.total_units_of_type(aircraft)
                if available < transfer_count:
                    logging.error(
                        f"Found killed {aircraft} from {flight.departure} but "
                        f"that airbase has only {available} available.")
                    continue

                flight.departure.base.aircraft[aircraft] -= transfer_count
                if aircraft not in flight.arrival.base.aircraft:
                    # TODO: Should use defaultdict.
                    flight.arrival.base.aircraft[aircraft] = 0
                flight.arrival.base.aircraft[aircraft] += transfer_count

    def complete_aircraft_transfers(self, debriefing: Debriefing) -> None:
        self._transfer_aircraft(self.game.blue_ato, debriefing.air_losses,
                                for_player=True)
        self._transfer_aircraft(self.game.red_ato, debriefing.air_losses,
                                for_player=False)

    @staticmethod
    def commit_air_losses(debriefing: Debriefing) -> None:
        for loss in debriefing.air_losses.losses:
            aircraft = loss.unit_type
            cp = loss.departure
            available = cp.base.total_units_of_type(aircraft)
            if available <= 0:
                logging.error(
                    f"Found killed {aircraft} from {cp} but that airbase has "
                    "none available.")
                continue

            logging.info(f"{aircraft} destroyed from {cp}")
            cp.base.aircraft[aircraft] -= 1

    @staticmethod
    def commit_front_line_losses(debriefing: Debriefing) -> None:
        for loss in debriefing.front_line_losses:
            unit_type = loss.unit_type
            control_point = loss.origin
            available = control_point.base.total_units_of_type(unit_type)
            if available <= 0:
                logging.error(
                    f"Found killed {unit_type} from {control_point} but that "
                    "airbase has none available.")
                continue

            logging.info(f"{unit_type} destroyed from {control_point}")
            control_point.base.armor[unit_type] -= 1

    @staticmethod
    def commit_ground_object_losses(debriefing: Debriefing) -> None:
        for loss in debriefing.ground_object_losses:
            # TODO: This should be stored in the TGO, not in the pydcs Group.
            if not hasattr(loss.group, "units_losts"):
                loss.group.units_losts = []

            loss.group.units.remove(loss.unit)
            loss.group.units_losts.append(loss.unit)

    def commit_building_losses(self, debriefing: Debriefing) -> None:
        for loss in debriefing.building_losses:
            loss.ground_object.kill()
            self.game.informations.append(Information(
                "Building destroyed",
                f"{loss.ground_object.dcs_identifier} has been destroyed at "
                f"location {loss.ground_object.obj_name}", self.game.turn
            ))

    @staticmethod
    def commit_damaged_runways(debriefing: Debriefing) -> None:
        for damaged_runway in debriefing.damaged_runways:
            damaged_runway.damage_runway()

    def commit(self, debriefing: Debriefing):
        logging.info("Committing mission results")

        self.commit_air_losses(debriefing)
        self.commit_front_line_losses(debriefing)
        self.commit_ground_object_losses(debriefing)
        self.commit_building_losses(debriefing)
        self.commit_damaged_runways(debriefing)

        # ------------------------------
        # Captured bases
        #if self.game.player_country in db.BLUEFOR_FACTIONS:
        coalition = 2 # Value in DCS mission event for BLUE
        #else:
        #    coalition = 1 # Value in DCS mission event for RED

        for captured in debriefing.base_capture_events:
            try:
                id = int(captured.split("||")[0])
                new_owner_coalition = int(captured.split("||")[1])

                captured_cps = []
                for cp in self.game.theater.controlpoints:
                    if cp.id == id:

                        if cp.captured and new_owner_coalition != coalition:
                            for_player = False
                            info = Information(cp.name + " lost !", "The ennemy took control of " + cp.name + "\nShame on us !", self.game.turn)
                            self.game.informations.append(info)
                            captured_cps.append(cp)
                        elif not(cp.captured) and new_owner_coalition == coalition:
                            for_player = True
                            info = Information(cp.name + " captured !", "We took control of " + cp.name + "! Great job !", self.game.turn)
                            self.game.informations.append(info)
                            captured_cps.append(cp)
                        else:
                            continue

                        cp.capture(self.game, for_player)

                for cp in captured_cps:
                    logging.info("Will run redeploy for " + cp.name)
                    self.redeploy_units(cp)
            except Exception:
                logging.exception(f"Could not process base capture {captured}")

        self.complete_aircraft_transfers(debriefing)

        # Destroyed units carcass
        # -------------------------
        for destroyed_unit in debriefing.state_data.destroyed_statics:
            self.game.add_destroyed_units(destroyed_unit)

        # -----------------------------------
        # Compute damage to bases
        for cp in self.game.theater.player_points():
            enemy_cps = [e for e in cp.connected_points if not e.captured]
            for enemy_cp in enemy_cps:
                print("Compute frontline progression for : " + cp.name + " to " + enemy_cp.name)

                delta = 0.0
                player_won = True
                ally_casualties = debriefing.casualty_count(cp)
                enemy_casualties = debriefing.casualty_count(enemy_cp)
                ally_units_alive = cp.base.total_armor
                enemy_units_alive = enemy_cp.base.total_armor

                print(ally_units_alive)
                print(enemy_units_alive)
                print(ally_casualties)
                print(enemy_casualties)

                ratio = (1.0 + enemy_casualties) / (1.0 + ally_casualties)

                player_aggresive = cp.stances[enemy_cp.id] in [CombatStance.AGGRESSIVE, CombatStance.ELIMINATION, CombatStance.BREAKTHROUGH]

                if ally_units_alive == 0:
                    player_won = False
                    delta = STRONG_DEFEAT_INFLUENCE
                elif enemy_units_alive == 0:
                    player_won = True
                    delta = STRONG_DEFEAT_INFLUENCE
                elif cp.stances[enemy_cp.id] == CombatStance.RETREAT:
                    player_won = False
                    delta = STRONG_DEFEAT_INFLUENCE
                else:
                    if enemy_casualties > ally_casualties:
                        player_won = True
                        if cp.stances[enemy_cp.id] == CombatStance.BREAKTHROUGH:
                            delta = STRONG_DEFEAT_INFLUENCE
                        else:
                            if ratio > 3:
                                delta = STRONG_DEFEAT_INFLUENCE
                            elif ratio < 1.5:
                                delta = MINOR_DEFEAT_INFLUENCE
                            else:
                                delta = DEFEAT_INFLUENCE
                    elif ally_casualties > enemy_casualties:

                        if ally_units_alive > 2*enemy_units_alive and player_aggresive:
                            # Even with casualties if the enemy is overwhelmed, they are going to lose ground
                            player_won = True
                            delta = MINOR_DEFEAT_INFLUENCE
                        elif ally_units_alive > 3*enemy_units_alive and player_aggresive:
                            player_won = True
                            delta = STRONG_DEFEAT_INFLUENCE
                        else:
                            # But is the enemy is not outnumbered, we lose
                            player_won = False
                            if cp.stances[enemy_cp.id] == CombatStance.BREAKTHROUGH:
                                delta = STRONG_DEFEAT_INFLUENCE
                            else:
                                delta = STRONG_DEFEAT_INFLUENCE

                    # No progress with defensive strategies
                    if player_won and cp.stances[enemy_cp.id] in [CombatStance.DEFENSIVE, CombatStance.AMBUSH]:
                        print("Defensive stance, progress is limited")
                        delta = MINOR_DEFEAT_INFLUENCE

                if player_won:
                    print(cp.name + " won !  factor > " + str(delta))
                    cp.base.affect_strength(delta)
                    enemy_cp.base.affect_strength(-delta)
                    info = Information("Frontline Report",
                                       "Our ground forces from " + cp.name + " are making progress toward " + enemy_cp.name,
                                       self.game.turn)
                    self.game.informations.append(info)
                else:
                    print(cp.name + " lost !  factor > " + str(delta))
                    enemy_cp.base.affect_strength(delta)
                    cp.base.affect_strength(-delta)
                    info = Information("Frontline Report",
                                       "Our ground forces from " + cp.name + " are losing ground against the enemy forces from " + enemy_cp.name,
                                       self.game.turn)
                    self.game.informations.append(info)

    def redeploy_units(self, cp):
        """"
        Auto redeploy units to newly captured base
        """

        ally_connected_cps = [ocp for ocp in cp.connected_points if cp.captured == ocp.captured]
        enemy_connected_cps = [ocp for ocp in cp.connected_points if cp.captured != ocp.captured]

        # If the newly captured cp does not have enemy connected cp,
        # then it is not necessary to redeploy frontline units there.
        if len(enemy_connected_cps) == 0:
            return
        else:
            # From each ally cp, send reinforcements
            for ally_cp in ally_connected_cps:
                total_units_redeployed = 0
                own_enemy_cp = [ocp for ocp in ally_cp.connected_points if ally_cp.captured != ocp.captured]

                moved_units = {}

                # If the connected base, does not have any more enemy cp connected.
                # Or if it is not the opponent redeploying forces there (enemy AI will never redeploy all their forces at once)
                if len(own_enemy_cp) > 0 or not cp.captured:
                    for frontline_unit, count in ally_cp.base.armor.items():
                        moved_units[frontline_unit] = int(count/2)
                        total_units_redeployed = total_units_redeployed + int(count/2)
                else: # So if the old base, does not have any more enemy cp connected, or if it is an enemy base
                    for frontline_unit, count in ally_cp.base.armor.items():
                        moved_units[frontline_unit] = count
                        total_units_redeployed = total_units_redeployed + count

                cp.base.commision_units(moved_units)
                ally_cp.base.commit_losses(moved_units)

                if total_units_redeployed > 0:
                    info = Information("Units redeployed", "", self.game.turn)
                    info.text = str(total_units_redeployed) + " units have been redeployed from " + ally_cp.name + " to " + cp.name
                    self.game.informations.append(info)
                    logging.info(info.text)


class UnitsDeliveryEvent:

    def __init__(self, control_point: ControlPoint) -> None:
        self.to_cp = control_point
        self.units: Dict[Type[UnitType], int] = {}

    def __str__(self) -> str:
        return "Pending delivery to {}".format(self.to_cp)

    def order(self, units: Dict[Type[UnitType], int]) -> None:
        for k, v in units.items():
            self.units[k] = self.units.get(k, 0) + v

    def consume_each_order(self) -> Iterator[Tuple[Type[UnitType], int]]:
        while self.units:
            yield self.units.popitem()

    def refund_all(self, game: Game) -> None:
        for unit_type, count in self.consume_each_order():
            try:
                price = PRICES[unit_type]
            except KeyError:
                logging.error(f"Could not refund {unit_type.id}, price unknown")
                continue

            logging.info(
                f"Refunding {count} {unit_type.id} at {self.to_cp.name}")
            game.adjust_budget(price * count, player=self.to_cp.captured)

    def process(self, game: Game) -> None:
        for unit_type, count in self.units.items():
            coalition = "Ally" if self.to_cp.captured else "Enemy"
            aircraft = unit_type.id
            name = self.to_cp.name
            game.message(
                f"{coalition} reinforcements: {aircraft} x {count} at {name}")
        self.to_cp.base.commision_units(self.units)
        self.units = {}
