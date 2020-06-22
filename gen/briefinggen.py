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
        self.description += "#" + str(len(flight.points) + 1) + " -- RTB\n"

        self.description += "-" * 50 + "\n"

    def add_ally_flight_description(self, flight):
        if flight.client_count == 0:
            flight_unit_name = db.unit_type_name(flight.unit_type)
            self.description += flight.flight_type.name + " " + flight_unit_name + " x " + str(flight.count) + ", departing in " + str(flight.scheduled_in) + " minutes \n"


    def generate(self):

        self.description = ""

        self.description += "DCS Liberation turn #" + str(self.game.turn) + "\n"
        self.description += "=" * 15 + "\n\n"

        self.description += "Current situation:\n"
        self.description += "=" * 15 + "\n\n"

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


