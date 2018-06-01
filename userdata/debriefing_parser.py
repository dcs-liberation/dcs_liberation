import typing
import json


class Debriefing:
    def __init__(self):
        self.destroyed_units = {}  # type: typing.Dict[str, typing.Dict[str, int]]

    def parse(self, path: str):
        with open(path, "r") as f:
            events = json.load(f)

