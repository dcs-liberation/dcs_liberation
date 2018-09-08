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

    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.m = mission
        self.conflict = conflict
        self.game = game

        self.freqs = []
        self.targets = []

    def append_frequency(self, name: str, frequency: str):
        self.freqs.append((name, frequency))

    def append_target(self, description: str, markpoint: str = None):
        self.targets.append((description, markpoint))

    def generate(self):
        description = ""

        if self.title:
            description += self.title

        if self.description:
            description += "\n\n" + self.description

        if self.freqs:
            description += "\n\n RADIO:"
            for name, freq in self.freqs:
                description += "\n{}: {}".format(name, freq)

        if self.targets:
            description += "\n\n TARGETS:"
            for name, tp in self.targets:
                description += "\n{} {}".format(name, "(TP {})".format(tp) if tp else "")

        self.m.set_description_text(description)
