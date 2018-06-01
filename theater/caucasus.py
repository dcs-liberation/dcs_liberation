from dcs.terrain import caucasus

from .conflicttheater import *
from .base import *

class CaucasusTheater(ConflictTheater):
    kutaisi = ControlPoint(caucasus.Kutaisi, ALL_RADIALS, SIZE_SMALL, IMPORTANCE_LOW)
    senaki = ControlPoint(caucasus.Senaki, ALL_RADIALS, SIZE_REGULAR, IMPORTANCE_LOW)
    kobuleti = ControlPoint(caucasus.Kobuleti, COAST_VERTICAL, SIZE_SMALL, IMPORTANCE_LOW)
    batumi = ControlPoint(caucasus.Batumi, COAST_VERTICAL, SIZE_SMALL, IMPORTANCE_MEDIUM)
    sukhumi = ControlPoint(caucasus.Sukhumi, COAST_VERTICAL, SIZE_REGULAR, IMPORTANCE_MEDIUM)
    gudauta = ControlPoint(caucasus.Gudauta, COAST_VERTICAL, SIZE_REGULAR, IMPORTANCE_MEDIUM)
    sochi = ControlPoint(caucasus.Sochi, COAST_VERTICAL, SIZE_BIG, IMPORTANCE_HIGH)

    def __init__(self):
        self.kutaisi.captured = True

        self.add_controlpoint(self.kutaisi, connected_to=[self.senaki])
        self.add_controlpoint(self.senaki, connected_to=[self.kobuleti, self.sukhumi, self.kutaisi])
        self.add_controlpoint(self.kobuleti, connected_to=[self.batumi, self.senaki])
        self.add_controlpoint(self.batumi, connected_to=[self.kobuleti])

        self.add_controlpoint(self.sukhumi, connected_to=[self.gudauta, self.senaki])
        self.add_controlpoint(self.gudauta, connected_to=[self.sochi, self.sukhumi])
        self.add_controlpoint(self.sochi, connected_to=[self.gudauta])
