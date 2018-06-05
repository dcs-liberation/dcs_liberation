from dcs.terrain import caucasus

from .conflicttheater import *
from .base import *

class CaucasusTheater(ConflictTheater):
    soganlug = ControlPoint.from_airport(caucasus.Soganlug, ALL_RADIALS, SIZE_SMALL, IMPORTANCE_LOW)
    kutaisi = ControlPoint.from_airport(caucasus.Kutaisi, ALL_RADIALS, SIZE_SMALL, IMPORTANCE_LOW)
    senaki = ControlPoint.from_airport(caucasus.Senaki_Kolkhi, ALL_RADIALS, SIZE_REGULAR, IMPORTANCE_LOW)
    kobuleti = ControlPoint.from_airport(caucasus.Kobuleti, COAST_VERTICAL, SIZE_SMALL, IMPORTANCE_LOW)
    batumi = ControlPoint.from_airport(caucasus.Batumi, COAST_VERTICAL, SIZE_SMALL, IMPORTANCE_MEDIUM)
    sukhumi = ControlPoint.from_airport(caucasus.Sukhumi_Babushara, COAST_VERTICAL, SIZE_REGULAR, IMPORTANCE_MEDIUM)
    gudauta = ControlPoint.from_airport(caucasus.Gudauta, COAST_VERTICAL, SIZE_REGULAR, IMPORTANCE_MEDIUM)
    sochi = ControlPoint.from_airport(caucasus.Sochi_Adler, COAST_VERTICAL, SIZE_BIG, IMPORTANCE_HIGH)

    maykop = ControlPoint.from_airport(caucasus.Maykop_Khanskaya, ALL_RADIALS, SIZE_LARGE, IMPORTANCE_HIGH)
    krasnodar = ControlPoint.from_airport(caucasus.Krasnodar_Center, ALL_RADIALS, SIZE_LARGE, IMPORTANCE_HIGH)
    novorossiysk = ControlPoint.from_airport(caucasus.Novorossiysk, COAST_VERTICAL, SIZE_BIG, IMPORTANCE_HIGH)
    gelendzhik = ControlPoint.from_airport(caucasus.Gelendzhik, COAST_VERTICAL, SIZE_BIG, IMPORTANCE_HIGH)
    krymsk = ControlPoint.from_airport(caucasus.Krymsk, ALL_RADIALS, SIZE_LARGE, IMPORTANCE_HIGH)
    anapa = ControlPoint.from_airport(caucasus.Anapa_Vityazevo, ALL_RADIALS, SIZE_LARGE, IMPORTANCE_HIGH)

    beslan = ControlPoint.from_airport(caucasus.Beslan, ALL_RADIALS, SIZE_REGULAR, IMPORTANCE_MEDIUM)
    nalchik = ControlPoint.from_airport(caucasus.Nalchik, ALL_RADIALS, SIZE_REGULAR, IMPORTANCE_MEDIUM)
    mineralnye = ControlPoint.from_airport(caucasus.Mineralnye_Vody, ALL_RADIALS, SIZE_BIG, IMPORTANCE_HIGH)
    mozdok = ControlPoint.from_airport(caucasus.Mozdok, ALL_RADIALS, SIZE_BIG, IMPORTANCE_HIGH)

    #carrier_1 = ControlPoint()

    def __init__(self):
        self.soganlug.captured = True

        self.add_controlpoint(self.soganlug, connected_to=[self.kutaisi, self.beslan])
        self.add_controlpoint(self.beslan, connected_to=[self.soganlug, self.mozdok, self.nalchik])
        self.add_controlpoint(self.nalchik, connected_to=[self.beslan, self.mozdok, self.mineralnye])
        self.add_controlpoint(self.mozdok, connected_to=[self.nalchik, self.beslan, self.mineralnye])
        self.add_controlpoint(self.mineralnye, connected_to=[self.nalchik, self.mozdok, self.maykop])
        self.add_controlpoint(self.maykop, connected_to=[self.mineralnye, self.krasnodar])

        self.add_controlpoint(self.kutaisi, connected_to=[self.soganlug, self.senaki])
        self.add_controlpoint(self.senaki, connected_to=[self.kobuleti, self.sukhumi, self.kutaisi])
        self.add_controlpoint(self.kobuleti, connected_to=[self.batumi, self.senaki])
        self.add_controlpoint(self.batumi, connected_to=[self.kobuleti])
        self.add_controlpoint(self.sukhumi, connected_to=[self.gudauta, self.senaki])
        self.add_controlpoint(self.gudauta, connected_to=[self.sochi, self.sukhumi])
        self.add_controlpoint(self.sochi, connected_to=[self.gudauta, self.gelendzhik])

        self.add_controlpoint(self.gelendzhik, connected_to=[self.sochi, self.novorossiysk])
        self.add_controlpoint(self.novorossiysk, connected_to=[self.gelendzhik, self.anapa])
        self.add_controlpoint(self.krymsk, connected_to=[self.novorossiysk, self.anapa, self.krasnodar])
        self.add_controlpoint(self.anapa, connected_to=[self.novorossiysk, self.krymsk])
        self.add_controlpoint(self.krasnodar, connected_to=[self.krymsk, self.maykop])
