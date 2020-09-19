import os
from collections import defaultdict
from dataclasses import dataclass
import random
from typing import List

from game import db
from dcs.mission import Mission
from .aircraft import FlightData
from .airfields import RunwayData
from .airsupportgen import AwacsInfo, TankerInfo
from .armor import JtacInfo
from .conflictgen import Conflict
from .ground_forces.combat_stance import CombatStance
from .radios import RadioFrequency


@dataclass
class CommInfo:
    """Communications information for the kneeboard."""
    name: str
    freq: RadioFrequency


class MissionInfoGenerator:
    """Base type for generators of mission information for the player.

    Examples of subtypes include briefing generators, kneeboard generators, etc.
    """

    def __init__(self, mission: Mission) -> None:
        self.mission = mission
        self.awacs: List[AwacsInfo] = []
        self.comms: List[CommInfo] = []
        self.flights: List[FlightData] = []
        self.jtacs: List[JtacInfo] = []
        self.tankers: List[TankerInfo] = []

    def add_awacs(self, awacs: AwacsInfo) -> None:
        """Adds an AWACS/GCI to the mission.

        Args:
            awacs: AWACS information.
        """
        self.awacs.append(awacs)

    def add_comm(self, name: str, freq: RadioFrequency) -> None:
        """Adds communications info to the mission.

        Args:
            name: Name of the radio channel.
            freq: Frequency of the radio channel.
        """
        self.comms.append(CommInfo(name, freq))

    def add_flight(self, flight: FlightData) -> None:
        """Adds flight info to the mission.

        Args:
            flight: Flight information.
        """
        self.flights.append(flight)

    def add_jtac(self, jtac: JtacInfo) -> None:
        """Adds a JTAC to the mission.

        Args:
            jtac: JTAC information.
        """
        self.jtacs.append(jtac)

    def add_tanker(self, tanker: TankerInfo) -> None:
        """Adds a tanker to the mission.

        Args:
            tanker: Tanker information.
        """
        self.tankers.append(tanker)

    def generate(self) -> None:
        """Generates the mission information."""
        raise NotImplementedError


class BriefingGenerator(MissionInfoGenerator):

    def __init__(self, mission: Mission, conflict: Conflict, game):
        super().__init__(mission)
        self.conflict = conflict
        self.game = game
        self.title = ""
        self.description = ""
        self.dynamic_runways: List[RunwayData] = []

    def add_dynamic_runway(self, runway: RunwayData) -> None:
        """Adds a dynamically generated runway to the briefing.

        Dynamic runways are any valid landing point that is a unit rather than a
        map feature. These include carriers, ships with a helipad, and FARPs.
        """
        self.dynamic_runways.append(runway)

    def add_flight_description(self, flight: FlightData):
        assert flight.client_units

        aircraft = flight.aircraft_type
        flight_unit_name = db.unit_type_name(aircraft)
        self.description += "-" * 50 + "\n"
        self.description += f"{flight_unit_name} x {flight.size + 2}\n\n"

        for i, wpt in enumerate(flight.waypoints):
            self.description += f"#{i + 1} -- {wpt.name} : {wpt.description}\n"
        self.description += f"#{len(flight.waypoints) + 1} -- RTB\n\n"

    def add_ally_flight_description(self, flight: FlightData):
        assert not flight.client_units
        aircraft = flight.aircraft_type
        flight_unit_name = db.unit_type_name(aircraft)
        self.description += (
            f"{flight.flight_type.name} {flight_unit_name} x {flight.size}, "
            f"departing in {flight.departure_delay} minutes\n"
        )

    def generate(self):
        self.description = ""

        self.description += "DCS Liberation turn #" + str(self.game.turn) + "\n"
        self.description += "=" * 15 + "\n\n"

        self.generate_ongoing_war_text()

        self.description += "\n"*2
        self.description += "Your flights:" + "\n"
        self.description += "=" * 15 + "\n\n"

        for flight in self.flights:
            if flight.client_units:
                self.add_flight_description(flight)

        self.description += "\n"*2
        self.description += "Planned ally flights:" + "\n"
        self.description += "=" * 15 + "\n"
        allied_flights_by_departure = defaultdict(list)
        for flight in self.flights:
            if not flight.client_units and flight.friendly:
                name = flight.departure.airfield_name
                allied_flights_by_departure[name].append(flight)
        for departure, flights in allied_flights_by_departure.items():
            self.description += f"\nFrom {departure}\n"
            self.description += "-" * 50 + "\n\n"
            for flight in flights:
                self.add_ally_flight_description(flight)

        if self.comms:
            self.description += "\n\nComms Frequencies:\n"
            self.description += "=" * 15 + "\n"
            for comm_info in self.comms:
                self.description += f"{comm_info.name}: {comm_info.freq}\n"
        self.description += ("-" * 50) + "\n"

        for runway in self.dynamic_runways:
            self.description += f"{runway.airfield_name}\n"
            self.description += f"RADIO : {runway.atc}\n"
            if runway.tacan is not None:
                self.description += f"TACAN : {runway.tacan} {runway.tacan_callsign}\n"
            if runway.icls is not None:
                self.description += f"ICLS Channel : {runway.icls}\n"
            self.description += "-" * 50 + "\n"


        self.description += "JTACS [F-10 Menu] : \n"
        self.description += "===================\n\n"
        for jtac in self.jtacs:
            self.description += f"{jtac.region} -- Code : {jtac.code}\n"

        self.mission.set_description_text(self.description)

        self.mission.add_picture_blue(os.path.abspath(
            "./resources/ui/splash_screen.png"))


    def generate_ongoing_war_text(self):

        self.description += "Current situation:\n"
        self.description += "=" * 15 + "\n\n"

        conflict_number = 0

        for c in self.game.theater.conflicts():
            conflict_number = conflict_number + 1
            if c[0].captured:
                player_base = c[0]
                enemy_base = c[1]
            else:
                player_base = c[1]
                enemy_base = c[0]

            has_numerical_superiority = player_base.base.total_armor > enemy_base.base.total_armor
            self.description += self.__random_frontline_sentence(player_base.name, enemy_base.name)

            if enemy_base.id in player_base.stances.keys():
                stance = player_base.stances[enemy_base.id]

                if player_base.base.total_armor == 0:
                    self.description += "We do not have a single vehicle available to hold our position, the situation is critical, and we will lose ground inevitably.\n"
                elif enemy_base.base.total_armor == 0:
                    self.description += "The enemy forces have been crushed, we will be able to make significant progress toward " + enemy_base.name + ". \n"
                if stance == CombatStance.AGGRESIVE:
                    if has_numerical_superiority:
                        self.description += "On this location, our ground forces will try to make progress against the enemy"
                        self.description += ". As the enemy is outnumbered, our forces should have no issue making progress.\n"
                    elif has_numerical_superiority:
                        self.description += "On this location, our ground forces will try an audacious assault against enemies in superior numbers. The operation is risky, and the enemy might counter attack.\n"
                elif stance == CombatStance.ELIMINATION:
                    if has_numerical_superiority:
                        self.description += "On this location, our ground forces will focus on the destruction of enemy assets, before attempting to make progress toward " + enemy_base.name + ". "
                        self.description += "The enemy is already outnumbered, and this maneuver might draw a final blow to their forces.\n"
                    elif has_numerical_superiority:
                        self.description += "On this location, our ground forces will try an audacious assault against enemies in superior numbers. The operation is risky, and the enemy might counter attack.\n"
                elif stance == CombatStance.BREAKTHROUGH:
                    if has_numerical_superiority:
                        self.description += "On this location, our ground forces will focus on progression toward " + enemy_base.name + ".\n"
                    elif has_numerical_superiority:
                        self.description += "On this location, our ground forces have been ordered to rush toward " + enemy_base.name + ". Wish them luck... We are also expecting a counter attack.\n"
                elif stance in [CombatStance.DEFENSIVE, CombatStance.AMBUSH]:
                    if has_numerical_superiority:
                        self.description += "On this location, our ground forces will hold position. We are not expecting an enemy assault.\n"
                    elif has_numerical_superiority:
                        self.description += "On this location, our ground forces have been ordered to hold still, and defend against enemy attacks. An enemy assault might be iminent.\n"

        if conflict_number == 0:
            self.description += "There are currently no fights on the ground.\n"

        self.description += "\n\n"


    def __random_frontline_sentence(self, player_base_name, enemy_base_name):
        templates = [
            "There are combats between {} and {}. ",
            "The war on the ground is still going on between {} and {}. ",
            "Our ground forces in {} are opposed to enemy forces based in {}. ",
            "Our forces from {} are fighting enemies based in {}. ",
            "There is an active frontline between {} and {}. ",
        ]
        return random.choice(templates).format(player_base_name, enemy_base_name)


