from dcs.terrain import caucasus

from .conflicttheater import *
from .base import *

class CaucasusTheater(ConflictTheater):
    sukhumi = ControlPoint(caucasus.Sukhumi().position, 1000, 5, True, Base())
    krymsk = ControlPoint(caucasus.Krymsk().position, 1500, 10, False, None)
    kransnodar = ControlPoint(caucasus.KrasnodarCenter().position, 3000, 30, False, Base())

    def __init__(self):
        self.add_controlpoint(self.sukhumi, [self.krymsk])
        self.add_controlpoint(self.krymsk, [self.sukhumi, self.kransnodar])
        self.add_controlpoint(self.kransnodar, [self.krymsk])
