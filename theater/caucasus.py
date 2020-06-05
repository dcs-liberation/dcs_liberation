import re

from dcs.terrain import caucasus
from dcs import mapping

from .landmap import *
from .conflicttheater import *
from .base import *


class CaucasusTheater(ConflictTheater):
    terrain = caucasus.Caucasus()
    overview_image = "caumap.gif"
    reference_points = {(-317948.32727306, 635639.37385346): (278.5*4, 319*4),
                        (-355692.3067714, 617269.96285781): (263*4, 352*4), }

    landmap = load_landmap("resources\\caulandmap.p")
    daytime_map = {
        "dawn": (6, 9),
        "day": (9, 18),
        "dusk": (18, 20),
        "night": (0, 5),
    }

    carrier_1 = ControlPoint.carrier("Carrier", mapping.Point(-305810.6875, 406399.1875))

    def __init__(self, load_ground_objects=True):
        super(CaucasusTheater, self).__init__()

        self.soganlug = ControlPoint.from_airport(caucasus.Soganlug, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.kutaisi = ControlPoint.from_airport(caucasus.Kutaisi, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.senaki = ControlPoint.from_airport(caucasus.Senaki_Kolkhi, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.kobuleti = ControlPoint.from_airport(caucasus.Kobuleti, COAST_A_E, SIZE_SMALL, 1.1)
        self.batumi = ControlPoint.from_airport(caucasus.Batumi, COAST_DL_E, SIZE_SMALL, 1.3)
        self.sukhumi = ControlPoint.from_airport(caucasus.Sukhumi_Babushara, COAST_DR_E, SIZE_REGULAR, 1.2)
        self.gudauta = ControlPoint.from_airport(caucasus.Gudauta, COAST_DR_E, SIZE_REGULAR, 1.2)
        self.sochi = ControlPoint.from_airport(caucasus.Sochi_Adler, COAST_DR_E, SIZE_BIG, IMPORTANCE_HIGH)
        self.gelendzhik = ControlPoint.from_airport(caucasus.Gelendzhik, COAST_DR_E, SIZE_BIG, 1.1)
        self.maykop = ControlPoint.from_airport(caucasus.Maykop_Khanskaya, LAND, SIZE_LARGE, IMPORTANCE_HIGH)
        self.krasnodar = ControlPoint.from_airport(caucasus.Krasnodar_Center, LAND, SIZE_LARGE, IMPORTANCE_HIGH)
        self.krymsk = ControlPoint.from_airport(caucasus.Krymsk, LAND, SIZE_LARGE, 1.2)
        self.anapa = ControlPoint.from_airport(caucasus.Anapa_Vityazevo, LAND, SIZE_LARGE, IMPORTANCE_HIGH)
        self.beslan = ControlPoint.from_airport(caucasus.Beslan, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.nalchik = ControlPoint.from_airport(caucasus.Nalchik, LAND, SIZE_REGULAR, 1.1)
        self.mineralnye = ControlPoint.from_airport(caucasus.Mineralnye_Vody, LAND, SIZE_BIG, 1.3)
        self.mozdok = ControlPoint.from_airport(caucasus.Mozdok, LAND, SIZE_BIG, 1.1)

        self.soganlug.frontline_offset = 0.5
        self.soganlug.base.strength = 1

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

        self.add_controlpoint(self.gelendzhik, connected_to=[self.sochi, ])
        self.add_controlpoint(self.krymsk, connected_to=[self.anapa, self.krasnodar])
        self.add_controlpoint(self.anapa, connected_to=[self.krymsk])
        self.add_controlpoint(self.krasnodar, connected_to=[self.krymsk, self.maykop])

        self.add_controlpoint(self.carrier_1)

        self.carrier_1.captured = True
        self.batumi.captured = True


"""
A smaller version of the caucasus map in western georgia.
Ideal for smaller scale campaign
"""
class WesternGeorgia(ConflictTheater):

    terrain = caucasus.Caucasus()
    overview_image = "caumap.gif"
    reference_points = {(-317948.32727306, 635639.37385346): (278.5 * 4, 319 * 4),
                        (-355692.3067714, 617269.96285781): (263 * 4, 352 * 4), }
    landmap = load_landmap("resources\\caulandmap.p")
    daytime_map = {
        "dawn": (6, 9),
        "day": (9, 18),
        "dusk": (18, 20),
        "night": (0, 5),
    }


    def __init__(self, load_ground_objects=True):
        super(WesternGeorgia, self).__init__()

        self.kobuleti = ControlPoint.from_airport(caucasus.Kobuleti, COAST_A_E, SIZE_SMALL, 1.1)
        self.senaki = ControlPoint.from_airport(caucasus.Senaki_Kolkhi, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.kutaisi = ControlPoint.from_airport(caucasus.Kutaisi, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.sukhumi = ControlPoint.from_airport(caucasus.Sukhumi_Babushara, COAST_DR_E, SIZE_REGULAR, 1.2)
        self.gudauta = ControlPoint.from_airport(caucasus.Gudauta, COAST_DR_E, SIZE_REGULAR, 1.2)
        self.sochi = ControlPoint.from_airport(caucasus.Sochi_Adler, COAST_DR_E, SIZE_BIG, IMPORTANCE_HIGH)
        self.carrier_1 = ControlPoint.carrier("Carrier", mapping.Point(-285810.6875, 496399.1875))

        self.add_controlpoint(self.kutaisi, connected_to=[self.senaki])
        self.add_controlpoint(self.senaki, connected_to=[self.kobuleti, self.sukhumi, self.kutaisi])
        self.add_controlpoint(self.kobuleti, connected_to=[self.senaki])
        self.add_controlpoint(self.sukhumi, connected_to=[self.gudauta, self.senaki])
        self.add_controlpoint(self.gudauta, connected_to=[self.sochi, self.sukhumi])
        self.add_controlpoint(self.sochi, connected_to=[self.gudauta])
        self.add_controlpoint(self.carrier_1)

        self.carrier_1.captured = True
        self.kobuleti.captured = True


"""
Georgian Theather [inverted starting position]
Ideal for smaller scale campaign
"""
class WesternGeorgiaInverted(ConflictTheater):

    terrain = caucasus.Caucasus()
    overview_image = "caumap.gif"
    reference_points = {(-317948.32727306, 635639.37385346): (278.5 * 4, 319 * 4),
                        (-355692.3067714, 617269.96285781): (263 * 4, 352 * 4), }
    landmap = load_landmap("resources\\caulandmap.p")
    daytime_map = {
        "dawn": (6, 9),
        "day": (9, 18),
        "dusk": (18, 20),
        "night": (0, 5),
    }


    def __init__(self, load_ground_objects=True):
        super(WesternGeorgiaInverted, self).__init__()

        self.kutaisi = ControlPoint.from_airport(caucasus.Kutaisi, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.senaki = ControlPoint.from_airport(caucasus.Senaki_Kolkhi, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.kobuleti = ControlPoint.from_airport(caucasus.Kobuleti, COAST_A_E, SIZE_SMALL, 1.1)
        self.sukhumi = ControlPoint.from_airport(caucasus.Sukhumi_Babushara, COAST_DR_E, SIZE_REGULAR, 1.2)
        self.gudauta = ControlPoint.from_airport(caucasus.Gudauta, COAST_DR_E, SIZE_REGULAR, 1.2)
        self.sochi = ControlPoint.from_airport(caucasus.Sochi_Adler, COAST_DR_E, SIZE_BIG, IMPORTANCE_HIGH)
        self.carrier_1 = ControlPoint.carrier("Carrier", mapping.Point(-285810.6875, 496399.1875))

        self.add_controlpoint(self.kutaisi, connected_to=[self.senaki])
        self.add_controlpoint(self.senaki, connected_to=[self.kobuleti, self.sukhumi, self.kutaisi])
        self.add_controlpoint(self.kobuleti, connected_to=[self.senaki])
        self.add_controlpoint(self.sukhumi, connected_to=[self.gudauta, self.senaki])
        self.add_controlpoint(self.gudauta, connected_to=[self.sochi, self.sukhumi])
        self.add_controlpoint(self.sochi, connected_to=[self.gudauta])
        self.add_controlpoint(self.carrier_1)

        self.carrier_1.captured = True
        self.sochi.captured = True




class NorthCaucasus(ConflictTheater):
    terrain = caucasus.Caucasus()
    overview_image = "caumap.gif"
    reference_points = {(-317948.32727306, 635639.37385346): (278.5*4, 319*4),
                        (-355692.3067714, 617269.96285781): (263*4, 352*4), }

    landmap = load_landmap("resources\\caulandmap.p")
    daytime_map = {
        "dawn": (6, 9),
        "day": (9, 18),
        "dusk": (18, 20),
        "night": (0, 5),
    }

    carrier_1 = ControlPoint.carrier("Carrier", mapping.Point(-305810.6875, 406399.1875))

    def __init__(self, load_ground_objects=True):
        super(NorthCaucasus, self).__init__()

        self.kutaisi = ControlPoint.from_airport(caucasus.Kutaisi, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.vaziani = ControlPoint.from_airport(caucasus.Vaziani, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.maykop = ControlPoint.from_airport(caucasus.Maykop_Khanskaya, LAND, SIZE_LARGE, IMPORTANCE_HIGH)
        self.beslan = ControlPoint.from_airport(caucasus.Beslan, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.nalchik = ControlPoint.from_airport(caucasus.Nalchik, LAND, SIZE_REGULAR, 1.1)
        self.mineralnye = ControlPoint.from_airport(caucasus.Mineralnye_Vody, LAND, SIZE_BIG, 1.3)
        self.mozdok = ControlPoint.from_airport(caucasus.Mozdok, LAND, SIZE_BIG, 1.1)
        self.carrier_1 = ControlPoint.carrier("Carrier", mapping.Point(-285810.6875, 496399.1875))

        self.vaziani.frontline_offset = 0.5
        self.vaziani.base.strength = 1

        self.add_controlpoint(self.kutaisi, connected_to=[self.vaziani])
        self.add_controlpoint(self.vaziani, connected_to=[self.beslan, self.kutaisi])
        self.add_controlpoint(self.beslan, connected_to=[self.vaziani, self.mozdok, self.nalchik])
        self.add_controlpoint(self.nalchik, connected_to=[self.beslan, self.mozdok, self.mineralnye])
        self.add_controlpoint(self.mozdok, connected_to=[self.nalchik, self.beslan, self.mineralnye])
        self.add_controlpoint(self.mineralnye, connected_to=[self.nalchik, self.mozdok, self.maykop])
        self.add_controlpoint(self.maykop, connected_to=[self.mineralnye])
        self.add_controlpoint(self.carrier_1, connected_to=[])

        self.carrier_1.captured = True
        self.vaziani.captured = True
        self.kutaisi.captured = True
