from __future__ import annotations

import logging
from typing import List, TYPE_CHECKING, Type

from dcs.mapping import Point
from dcs.task import Task
from dcs.unittype import VehicleType

from game import persistency
from game.debriefing import AirLosses, Debriefing
from game.infos.information import Information
from game.operation.operation import Operation
from game.theater import ControlPoint
from gen import AirTaskingOrder
from gen.ground_forces.combat_stance import CombatStance
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

    def __init__(
        self,
        game,
        from_cp: ControlPoint,
        target_cp: ControlPoint,
        location: Point,
        attacker_name: str,
        defender_name: str,
    ):
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
            persistency.mission_path_for("liberation_nextturn.miz")
        )
        return unit_map

    @staticmethod
    def _transfer_aircraft(
        ato: AirTaskingOrder, losses: AirLosses, for_player: bool
    ) -> None:
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
                        "was captured"
                    )
                    continue

                transfer_count = losses.surviving_flight_members(flight)
                if transfer_count < 0:
                    logging.error(
                        f"{flight} had {flight.count} aircraft but "
                        f"{transfer_count} losses were recorded."
                    )
                    continue

                aircraft = flight.unit_type
                available = flight.departure.base.total_units_of_type(aircraft)
                if available < transfer_count:
                    logging.error(
                        f"Found killed {aircraft} from {flight.departure} but "
                        f"that airbase has only {available} available."
                    )
                    continue

                flight.departure.base.aircraft[aircraft] -= transfer_count
                if aircraft not in flight.arrival.base.aircraft:
                    # TODO: Should use defaultdict.
                    flight.arrival.base.aircraft[aircraft] = 0
                flight.arrival.base.aircraft[aircraft] += transfer_count

    def complete_aircraft_transfers(self, debriefing: Debriefing) -> None:
        self._transfer_aircraft(
            self.game.blue_ato, debriefing.air_losses, for_player=True
        )
        self._transfer_aircraft(
            self.game.red_ato, debriefing.air_losses, for_player=False
        )

    def commit_air_losses(self, debriefing: Debriefing) -> None:
        for loss in debriefing.air_losses.losses:
            if (
                not loss.pilot.player
                or not self.game.settings.invulnerable_player_pilots
            ):
                loss.pilot.kill()
            aircraft = loss.flight.unit_type
            cp = loss.flight.departure
            available = cp.base.total_units_of_type(aircraft)
            if available <= 0:
                logging.error(
                    f"Found killed {aircraft} from {cp} but that airbase has "
                    "none available."
                )
                continue

            logging.info(f"{aircraft} destroyed from {cp}")
            cp.base.aircraft[aircraft] -= 1

    @staticmethod
    def _commit_pilot_experience(ato: AirTaskingOrder) -> None:
        for package in ato.packages:
            for flight in package.flights:
                for idx, pilot in enumerate(flight.roster.pilots):
                    if pilot is None:
                        logging.error(
                            f"Cannot award experience to pilot #{idx} of {flight} "
                            "because no pilot is assigned"
                        )
                        continue
                    pilot.record.missions_flown += 1

    def commit_pilot_experience(self) -> None:
        self._commit_pilot_experience(self.game.blue_ato)
        self._commit_pilot_experience(self.game.red_ato)

    @staticmethod
    def commit_front_line_losses(debriefing: Debriefing) -> None:
        for loss in debriefing.front_line_losses:
            unit_type = loss.unit_type
            control_point = loss.origin
            available = control_point.base.total_units_of_type(unit_type)
            if available <= 0:
                logging.error(
                    f"Found killed {unit_type} from {control_point} but that "
                    "airbase has none available."
                )
                continue

            logging.info(f"{unit_type} destroyed from {control_point}")
            control_point.base.armor[unit_type] -= 1

    @staticmethod
    def commit_convoy_losses(debriefing: Debriefing) -> None:
        for loss in debriefing.convoy_losses:
            unit_type = loss.unit_type
            convoy = loss.convoy
            available = loss.convoy.units.get(unit_type, 0)
            convoy_name = f"convoy from {convoy.origin} to {convoy.destination}"
            if available <= 0:
                logging.error(
                    f"Found killed {unit_type} in {convoy_name} but that convoy has "
                    "none available."
                )
                continue

            logging.info(f"{unit_type} destroyed in {convoy_name}")
            convoy.kill_unit(unit_type)

    @staticmethod
    def commit_cargo_ship_losses(debriefing: Debriefing) -> None:
        for ship in debriefing.cargo_ship_losses:
            logging.info(
                f"All units destroyed in cargo ship from {ship.origin} to "
                f"{ship.destination}."
            )
            ship.kill_all()

    @staticmethod
    def commit_airlift_losses(debriefing: Debriefing) -> None:
        for loss in debriefing.airlift_losses:
            transfer = loss.transfer
            airlift_name = f"airlift from {transfer.origin} to {transfer.destination}"
            for unit_type in loss.cargo:
                try:
                    transfer.kill_unit(unit_type)
                    logging.info(f"{unit_type} destroyed in {airlift_name}")
                except KeyError:
                    logging.exception(
                        f"Found killed {unit_type} in {airlift_name} but that airlift "
                        "has none available."
                    )

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
            self.game.informations.append(
                Information(
                    "Building destroyed",
                    f"{loss.ground_object.dcs_identifier} has been destroyed at "
                    f"location {loss.ground_object.obj_name}",
                    self.game.turn,
                )
            )

    @staticmethod
    def commit_damaged_runways(debriefing: Debriefing) -> None:
        for damaged_runway in debriefing.damaged_runways:
            damaged_runway.damage_runway()

    def commit_captures(self, debriefing: Debriefing) -> None:
        for captured in debriefing.base_captures:
            try:
                if captured.captured_by_player:
                    info = Information(
                        f"{captured.control_point} captured!",
                        f"We took control of {captured.control_point}.",
                        self.game.turn,
                    )
                else:
                    info = Information(
                        f"{captured.control_point} lost!",
                        f"The enemy took control of {captured.control_point}.",
                        self.game.turn,
                    )

                self.game.informations.append(info)
                captured.control_point.capture(self.game, captured.captured_by_player)
                logging.info(f"Will run redeploy for {captured.control_point}")
                self.redeploy_units(captured.control_point)
            except Exception:
                logging.exception(f"Could not process base capture {captured}")

    def commit(self, debriefing: Debriefing):
        logging.info("Committing mission results")

        self.commit_air_losses(debriefing)
        self.commit_pilot_experience()
        self.commit_front_line_losses(debriefing)
        self.commit_convoy_losses(debriefing)
        self.commit_airlift_losses(debriefing)
        self.commit_ground_object_losses(debriefing)
        self.commit_building_losses(debriefing)
        self.commit_damaged_runways(debriefing)
        self.commit_captures(debriefing)
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
                print(
                    "Compute frontline progression for : "
                    + cp.name
                    + " to "
                    + enemy_cp.name
                )

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

                player_aggresive = cp.stances[enemy_cp.id] in [
                    CombatStance.AGGRESSIVE,
                    CombatStance.ELIMINATION,
                    CombatStance.BREAKTHROUGH,
                ]

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

                        if (
                            ally_units_alive > 2 * enemy_units_alive
                            and player_aggresive
                        ):
                            # Even with casualties if the enemy is overwhelmed, they are going to lose ground
                            player_won = True
                            delta = MINOR_DEFEAT_INFLUENCE
                        elif (
                            ally_units_alive > 3 * enemy_units_alive
                            and player_aggresive
                        ):
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
                    if player_won and cp.stances[enemy_cp.id] in [
                        CombatStance.DEFENSIVE,
                        CombatStance.AMBUSH,
                    ]:
                        print("Defensive stance, progress is limited")
                        delta = MINOR_DEFEAT_INFLUENCE

                if player_won:
                    print(cp.name + " won !  factor > " + str(delta))
                    cp.base.affect_strength(delta)
                    enemy_cp.base.affect_strength(-delta)
                    info = Information(
                        "Frontline Report",
                        "Our ground forces from "
                        + cp.name
                        + " are making progress toward "
                        + enemy_cp.name,
                        self.game.turn,
                    )
                    self.game.informations.append(info)
                else:
                    print(cp.name + " lost !  factor > " + str(delta))
                    enemy_cp.base.affect_strength(delta)
                    cp.base.affect_strength(-delta)
                    info = Information(
                        "Frontline Report",
                        "Our ground forces from "
                        + cp.name
                        + " are losing ground against the enemy forces from "
                        + enemy_cp.name,
                        self.game.turn,
                    )
                    self.game.informations.append(info)

    def redeploy_units(self, cp: ControlPoint) -> None:
        """ "
        Auto redeploy units to newly captured base
        """

        ally_connected_cps = [
            ocp for ocp in cp.connected_points if cp.captured == ocp.captured
        ]
        enemy_connected_cps = [
            ocp for ocp in cp.connected_points if cp.captured != ocp.captured
        ]

        # If the newly captured cp does not have enemy connected cp,
        # then it is not necessary to redeploy frontline units there.
        if len(enemy_connected_cps) == 0:
            return

        # From each ally cp, send reinforcements
        for ally_cp in ally_connected_cps:
            self.redeploy_between(cp, ally_cp)

    def redeploy_between(self, destination: ControlPoint, source: ControlPoint) -> None:
        total_units_redeployed = 0
        moved_units = {}

        if source.has_active_frontline or not destination.captured:
            # If there are still active front lines to defend at the
            # transferring CP we should not transfer all units.
            #
            # Opfor also does not transfer all of their units.
            # TODO: Balance the CPs rather than moving half from everywhere.
            move_factor = 0.5
        else:
            # Otherwise we can move everything.
            move_factor = 1

        for frontline_unit, count in source.base.armor.items():
            moved_units[frontline_unit] = int(count * move_factor)
            total_units_redeployed = total_units_redeployed + int(count * move_factor)

        destination.base.commission_units(moved_units)
        source.base.commit_losses(moved_units)

        # Also transfer pending deliveries.
        for unit_type, count in source.pending_unit_deliveries.units.items():
            if not issubclass(unit_type, VehicleType):
                continue
            if count <= 0:
                # Don't transfer *sales*...
                continue
            move_count = int(count * move_factor)
            source.pending_unit_deliveries.sell({unit_type: move_count})
            destination.pending_unit_deliveries.order({unit_type: move_count})
            total_units_redeployed += move_count

        if total_units_redeployed > 0:
            text = (
                f"{total_units_redeployed}  units have been redeployed from "
                f"{source.name} to {destination.name}"
            )
            info = Information("Units redeployed", text, self.game.turn)
            self.game.informations.append(info)
            logging.info(text)
