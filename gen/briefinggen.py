import logging

from game import db
from .conflictgen import *
from .naming import *

from dcs.mission import *


class BriefingGenerator:
    freqs = None  # type: typing.List[typing.Tuple[str, str]]
    title = ""  # type: str
    description = ""  # type: str
    targets = None  # type: typing.List[typing.Tuple[str, str]]
    waypoints = None  # type: typing.List[str]

    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.m = mission
        self.conflict = conflict
        self.game = game
        self.description = ""

        self.freqs = []
        self.targets = []
        self.waypoints = []

    def append_frequency(self, name: str, frequency: str):
        self.freqs.append((name, frequency))

    def append_target(self, description: str, markpoint: str = None):
        self.targets.append((description, markpoint))

    def append_waypoint(self, description: str):
        self.waypoints.append(description)

    def add_flight_description(self, flight):

        if flight.client_count <= 0:
            return

        flight_unit_name = db.unit_type_name(flight.unit_type)
        self.description += "-" * 50 + "\n"
        self.description += flight_unit_name + " x " + str(flight.count) + 2 * "\n"

        self.description += "#0 -- TAKEOFF : Take off from " + flight.from_cp.name + "\n"
        for i, wpt in enumerate(flight.points):
            self.description += "#" + str(1+i) + " -- " + wpt.name + " : " + wpt.description + "\n"
        self.description += "#" + str(len(flight.points) + 1) + " -- RTB\n\n"

        group = flight.group
        if group is not None:
            for i, nav_target in enumerate(group.nav_target_points):
                self.description += nav_target.text_comment + "\n"
        self.description += "\n"
        self.description += "-" * 50 + "\n"

    def add_ally_flight_description(self, flight):
        if flight.client_count == 0:
            flight_unit_name = db.unit_type_name(flight.unit_type)
            self.description += flight.flight_type.name + " " + flight_unit_name + " x " + str(flight.count) + ", departing in " + str(flight.scheduled_in) + " minutes \n"

    def generate(self):

        self.description = ""

        self.description += "DCS Liberation turn #" + str(self.game.turn) + "\n"
        self.description += "=" * 15 + "\n\n"

        self.generate_ongoing_war_text()

        self.description += "\n"*2
        self.description += "Your flights:" + "\n"
        self.description += "=" * 15 + "\n\n"

        for planner in self.game.planners.values():
            for flight in planner.flights:
                self.add_flight_description(flight)

        self.description += "\n"*2
        self.description += "Planned ally flights:" + "\n"
        self.description += "=" * 15 + "\n"
        for planner in self.game.planners.values():
            if planner.from_cp.captured and len(planner.flights) > 0:
                self.description += "\nFrom " + planner.from_cp.full_name + " \n"
                self.description += "-" * 50 + "\n\n"
                for flight in planner.flights:
                    self.add_ally_flight_description(flight)

        if self.freqs:
            self.description += "\n\nComms Frequencies:\n"
            self.description += "=" * 15 + "\n"
            for name, freq in self.freqs:
                self.description += "{}: {}\n".format(name, freq)
        self.description += ("-" * 50) + "\n"

        for cp in self.game.theater.controlpoints:
            if cp.captured and cp.cptype in [ControlPointType.LHA_GROUP, ControlPointType.AIRCRAFT_CARRIER_GROUP]:
                self.description += cp.name + "\n"
                self.description += "RADIO : 127.5 Mhz AM\n"
                self.description += "TACAN : "
                self.description += str(cp.tacanN)
                if cp.tacanY:
                    self.description += "Y"
                else:
                    self.description += "X"
                self.description += " " + str(cp.tacanI) + "\n"

                if cp.cptype == ControlPointType.AIRCRAFT_CARRIER_GROUP and hasattr(cp, "icls"):
                    self.description += "ICLS Channel : " + str(cp.icls) + "\n"
                self.description += "-" * 50 + "\n"

        self.m.set_description_text(self.description)

        self.m.add_picture_blue(os.path.abspath("./resources/ui/splash_screen.png"))


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
            "The war on the ground is still going on between {} an {}. ",
            "Our ground forces in {} are opposed to enemy forces based in {}. ",
            "Our forces from {} are fighting enemies based in {}. ",
            "There is an active frontline between {} and {}. ",
        ]
        return random.choice(templates).format(player_base_name, enemy_base_name)


