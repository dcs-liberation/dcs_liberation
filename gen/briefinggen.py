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

        self.freqs = []
        self.targets = []
        self.waypoints = []

    def append_frequency(self, name: str, frequency: str):
        self.freqs.append((name, frequency))

    def append_target(self, description: str, markpoint: str = None):
        self.targets.append((description, markpoint))

    def append_waypoint(self, description: str):
        self.waypoints.append(description)

    def generate(self):
        self.waypoints.insert(0, "INITIAL")
        self.waypoints.append("RTB")
        self.waypoints.append("RTB Landing")

        description = ""

        if self.title:
            description += self.title

        if self.description:
            description += "\n\n" + self.description

        if self.freqs:
            description += "\n\nCOMMS:"
            for name, freq in self.freqs:
                description += "\n{}: {}".format(name, freq)

        if self.targets:
            description += "\n\nTARGETS:"
            for i, (name, tp) in enumerate(self.targets):
                description += "\n#{} {} {}".format(i+1, name, "(TP {})".format(tp) if tp else "")

        if self.waypoints:
            description += "\n\nWAYPOINTS:"
            for i, descr in enumerate(self.waypoints):
                description += "\n#{}: {}".format(i, descr)

        self.m.set_description_text(description)
