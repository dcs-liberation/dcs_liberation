import typing
import dcs

from .controlpoint import *

class ConflictTheater:
    controlpoints = [] # type: typing.Collection[ControlPoint]

    def add_controlpoint(self, point: ControlPoint, connected_to: typing.Collection[ControlPoint]):
        for connected_point in connected_to:
            point.connect(to=connected_point)

        self.controlpoints.append(point)

    def player_bases(self) -> typing.Collection[ControlPoint]:
        return [point for point in self.controlpoints if point.captured and point.base]
