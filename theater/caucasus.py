import re

from dcs.terrain import caucasus
from dcs import mapping

from .landmap import *
from .conflicttheater import *
from .base import *


class CaucasusTheater(ConflictTheater):
    terrain = caucasus.Caucasus()
    overview_image = "caumap.gif"
    reference_points = {(-317948.32727306, 635639.37385346): (282.5, 319),
                        (-355692.3067714, 617269.96285781): (269, 352), }
    landmap_poly = load_poly("resources\\caulandmap.p")
    daytime_map = {
        "dawn": (6, 9),
        "day": (9, 18),
        "dusk": (18, 21),
        "night": (0, 5),
    }

    soganlug = ControlPoint.from_airport(caucasus.Soganlug, LAND, SIZE_SMALL, IMPORTANCE_LOW)
    kutaisi = ControlPoint.from_airport(caucasus.Kutaisi, LAND, SIZE_SMALL, IMPORTANCE_LOW)
    senaki = ControlPoint.from_airport(caucasus.Senaki_Kolkhi, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
    kobuleti = ControlPoint.from_airport(caucasus.Kobuleti, COAST_A_E, SIZE_SMALL, 1.1)
    batumi = ControlPoint.from_airport(caucasus.Batumi, COAST_DL_E, SIZE_SMALL, 1.3)
    sukhumi = ControlPoint.from_airport(caucasus.Sukhumi_Babushara, COAST_DR_E, SIZE_REGULAR, 1.2)
    gudauta = ControlPoint.from_airport(caucasus.Gudauta, COAST_DR_E, SIZE_REGULAR, 1.2)
    sochi = ControlPoint.from_airport(caucasus.Sochi_Adler, COAST_DR_E, SIZE_BIG, IMPORTANCE_HIGH)

    gelendzhik = ControlPoint.from_airport(caucasus.Gelendzhik, COAST_DR_E, SIZE_BIG, 1.1)
    maykop = ControlPoint.from_airport(caucasus.Maykop_Khanskaya, LAND, SIZE_LARGE, IMPORTANCE_HIGH)
    krasnodar = ControlPoint.from_airport(caucasus.Krasnodar_Center, LAND, SIZE_LARGE, IMPORTANCE_HIGH)
    novorossiysk = ControlPoint.from_airport(caucasus.Novorossiysk, COAST_DR_E, SIZE_BIG, 1.2)
    krymsk = ControlPoint.from_airport(caucasus.Krymsk, LAND, SIZE_LARGE, 1.2)
    anapa = ControlPoint.from_airport(caucasus.Anapa_Vityazevo, LAND, SIZE_LARGE, IMPORTANCE_HIGH)

    beslan = ControlPoint.from_airport(caucasus.Beslan, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
    nalchik = ControlPoint.from_airport(caucasus.Nalchik, LAND, SIZE_REGULAR, 1.1)
    mineralnye = ControlPoint.from_airport(caucasus.Mineralnye_Vody, LAND, SIZE_BIG, 1.3)
    mozdok = ControlPoint.from_airport(caucasus.Mozdok, LAND, SIZE_BIG, 1.1)

    carrier_1 = ControlPoint.carrier("Carrier", mapping.Point(-305810.6875, 406399.1875))

    def __init__(self):
        super(CaucasusTheater, self).__init__()

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

        self.add_controlpoint(self.carrier_1)

        self.carrier_1.captured = True
        self.soganlug.captured = True

    def add_controlpoint(self, point: ControlPoint, connected_to: typing.Collection[ControlPoint] = []):
        point.name = " ".join(re.split(r" |-", point.name)[:1])

        super(CaucasusTheater, self).add_controlpoint(point, connected_to=connected_to)