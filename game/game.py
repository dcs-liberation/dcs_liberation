import typing

from theater.conflicttheater import *
from theater.controlpoint import *
from .event import *

class Game:
    events = [] # type: typing.List[Event]

    def __init__(self, theater: ConflictTheater):
        self.theater = theater

    def _fill_cap_events(self):
        for cp in [x for x in self.theater.controlpoints if x.captured]:
            for connected_cp in [x for x in cp.connected_points if not x.captured]:
                self.events.append(CaptureEvent(cp, connected_cp))

    def pass_turn(self):
        self.events = [] # type: typing.List[Event]
        self._fill_cap_events()

