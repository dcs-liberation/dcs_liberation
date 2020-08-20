from dcs.terrain import syria

from .conflicttheater import *
from .landmap import *


class SyriaTheater(ConflictTheater):
    terrain = dcs.terrain.Syria()
    overview_image = "syria.gif"
    reference_points = {(syria.Eyn_Shemer.position.x, syria.Eyn_Shemer.position.y): (1300, 1380),
                        (syria.Tabqa.position.x, syria.Tabqa.position.y): (2060, 570)}
    landmap = load_landmap("resources\\syrialandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (8, 16),
        "dusk": (16, 18),
        "night": (0, 5),
    }

    def __init__(self):
        super(SyriaTheater, self).__init__()


class GolanHeights(SyriaTheater):

    def __init__(self):
        super(GolanHeights, self).__init__()

        self.ramatDavid = ControlPoint.from_airport(syria.Ramat_David, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.kinghussein = ControlPoint.from_airport(syria.King_Hussein_Air_College, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.khalkhala = ControlPoint.from_airport(syria.Khalkhalah, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)

        self.khalkhala.allow_sea_units = False
        self.ramatDavid.allow_sea_units = False
        self.kinghussein.allow_sea_units = False

        self.marjruhayyil = ControlPoint.from_airport(syria.Marj_Ruhayyil, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.mezzeh = ControlPoint.from_airport(syria.Mezzeh, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)
        self.aldumayr = ControlPoint.from_airport(syria.Al_Dumayr, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)

        self.carrier = ControlPoint.carrier("Carrier", Point(-280000, -238000), 1001)
        self.lha = ControlPoint.lha("LHA Carrier", Point(-237000, -89800), 1002)

        self.add_controlpoint(self.ramatDavid, connected_to=[self.khalkhala])
        self.add_controlpoint(self.khalkhala, connected_to=[self.ramatDavid, self.kinghussein, self.marjruhayyil])
        self.add_controlpoint(self.kinghussein, connected_to=[self.khalkhala])
        self.add_controlpoint(self.marjruhayyil, connected_to=[self.khalkhala, self.mezzeh, self.aldumayr])
        self.add_controlpoint(self.mezzeh, connected_to=[self.marjruhayyil])
        self.add_controlpoint(self.aldumayr, connected_to=[self.marjruhayyil])

        self.add_controlpoint(self.carrier)
        self.add_controlpoint(self.lha)

        self.ramatDavid.captured = True
        self.carrier.captured = True
        self.lha.captured = True

        self.aldumayr.captured_invert = True
        self.carrier.captured_invert = True
        self.lha.captured_invert = True


class TurkishInvasion(SyriaTheater):

    def __init__(self):
        super(TurkishInvasion, self).__init__()

        self.hatay = ControlPoint.from_airport(syria.Hatay, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.incirlik = ControlPoint.from_airport(syria.Incirlik, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.minakh = ControlPoint.from_airport(syria.Minakh, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.aleppo = ControlPoint.from_airport(syria.Aleppo, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)
        self.kuweires = ControlPoint.from_airport(syria.Kuweires, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.jirah = ControlPoint.from_airport(syria.Jirah, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.tabqa = ControlPoint.from_airport(syria.Tabqa, LAND, SIZE_REGULAR, IMPORTANCE_LOW)

        self.carrier = ControlPoint.carrier("Carrier", Point(133000, -54000), 1001)
        self.lha = ControlPoint.lha("LHA", Point(155000, -19000), 1002)

        self.add_controlpoint(self.incirlik, connected_to=[])
        self.add_controlpoint(self.hatay, connected_to=[self.minakh])
        self.add_controlpoint(self.minakh, connected_to=[self.aleppo, self.hatay])
        self.add_controlpoint(self.aleppo, connected_to=[self.kuweires, self.minakh])
        self.add_controlpoint(self.kuweires, connected_to=[self.jirah, self.aleppo])
        self.add_controlpoint(self.jirah, connected_to=[self.tabqa, self.kuweires])
        self.add_controlpoint(self.tabqa, connected_to=[self.jirah])

        self.add_controlpoint(self.carrier)
        self.add_controlpoint(self.lha)

        self.incirlik.captured = True
        self.hatay.captured = True
        self.carrier.captured = True
        self.lha.captured = True

        self.tabqa.captured_invert = True


class SyrianCivilWar(SyriaTheater):

    def __init__(self):
        super(SyrianCivilWar, self).__init__()

        self.basselAlAssad = ControlPoint.from_airport(syria.Bassel_Al_Assad, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.marjruhayyil = ControlPoint.from_airport(syria.Marj_Ruhayyil, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.aldumayr = ControlPoint.from_airport(syria.Al_Dumayr, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)
        self.hama = ControlPoint.from_airport(syria.Hama, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.alqusair= ControlPoint.from_airport(syria.Al_Qusayr, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.aleppo = ControlPoint.from_airport(syria.Aleppo, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)

        self.palmyra = ControlPoint.from_airport(syria.Palmyra, LAND, SIZE_REGULAR, IMPORTANCE_LOW)

        self.carrier = ControlPoint.carrier("Carrier", Point(18537, -52000), 1001)
        self.lha = ControlPoint.lha("LHA", Point(116000, 30000), 1002)

        self.add_controlpoint(self.basselAlAssad, connected_to=[self.hama])
        self.add_controlpoint(self.marjruhayyil, connected_to=[self.aldumayr])

        self.add_controlpoint(self.hama, connected_to=[self.basselAlAssad, self.aleppo, self.alqusair])
        self.add_controlpoint(self.aleppo, connected_to=[self.hama])
        self.add_controlpoint(self.alqusair, connected_to=[self.hama, self.aldumayr, self.palmyra])
        self.add_controlpoint(self.palmyra, connected_to=[self.alqusair])
        self.add_controlpoint(self.aldumayr, connected_to=[self.alqusair, self.marjruhayyil])

        self.add_controlpoint(self.carrier)
        self.add_controlpoint(self.lha)

        self.basselAlAssad.captured = True
        self.marjruhayyil.captured = True
        self.carrier.captured = True
        self.lha.captured = True

        self.aleppo.captured_invert = True
        self.carrier.captured_invert = True
        self.lha.captured_invert = True


class InherentResolve(SyriaTheater):

    def __init__(self):
        super(InherentResolve, self).__init__()

        self.kinghussein = ControlPoint.from_airport(syria.King_Hussein_Air_College, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.khalkhala = ControlPoint.from_airport(syria.Khalkhalah, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)
        self.palmyra = ControlPoint.from_airport(syria.Palmyra, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.jirah = ControlPoint.from_airport(syria.Jirah, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.tabqa = ControlPoint.from_airport(syria.Tabqa, LAND, SIZE_REGULAR, IMPORTANCE_LOW)

        self.carrier = ControlPoint.carrier("Carrier", Point(-210000, -200000), 1001)
        self.lha = ControlPoint.lha("LHA", Point(-131000, -161000), 1002)

        self.add_controlpoint(self.kinghussein, connected_to=[self.khalkhala])
        self.add_controlpoint(self.khalkhala, connected_to=[self.kinghussein, self.palmyra])
        self.add_controlpoint(self.palmyra, connected_to=[self.khalkhala, self.tabqa])
        self.add_controlpoint(self.tabqa, connected_to=[self.palmyra, self.jirah])
        self.add_controlpoint(self.jirah, connected_to=[self.tabqa])

        self.add_controlpoint(self.carrier)
        self.add_controlpoint(self.lha)

        self.kinghussein.captured = True
        self.carrier.captured = True
        self.lha.captured = True

        self.jirah.captured_invert = True
        self.carrier.captured_invert = True
        self.lha.captured_invert = True


class SyriaFullMap(SyriaTheater):

    def __init__(self):
        super(SyriaFullMap, self).__init__()

        self.ramatDavid = ControlPoint.from_airport(syria.Ramat_David, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.kinghussein = ControlPoint.from_airport(syria.King_Hussein_Air_College, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.khalkhala = ControlPoint.from_airport(syria.Khalkhalah, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)
        self.palmyra = ControlPoint.from_airport(syria.Palmyra, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.jirah = ControlPoint.from_airport(syria.Jirah, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.tabqa = ControlPoint.from_airport(syria.Tabqa, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.aldumayr = ControlPoint.from_airport(syria.Al_Dumayr, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)
        self.hama = ControlPoint.from_airport(syria.Hama, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.alqusair= ControlPoint.from_airport(syria.Al_Qusayr, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.aleppo = ControlPoint.from_airport(syria.Aleppo, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)
        self.basselAlAssad = ControlPoint.from_airport(syria.Bassel_Al_Assad, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.renemouawad = ControlPoint.from_airport(syria.Rene_Mouawad, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.minakh = ControlPoint.from_airport(syria.Minakh, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.hatay = ControlPoint.from_airport(syria.Hatay, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.incirlik = ControlPoint.from_airport(syria.Incirlik, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)


        self.carrier = ControlPoint.carrier("Carrier", Point(-151000, -106000), 1001)
        self.lha = ControlPoint.lha("LHA", Point(-131000, -161000), 1002)

        self.add_controlpoint(self.ramatDavid, connected_to=[self.kinghussein])
        self.add_controlpoint(self.kinghussein, connected_to=[self.khalkhala, self.ramatDavid])
        self.add_controlpoint(self.khalkhala, connected_to=[self.kinghussein, self.aldumayr])
        self.add_controlpoint(self.aldumayr, connected_to=[self.khalkhala, self.alqusair])
        self.add_controlpoint(self.alqusair, connected_to=[self.hama, self.aldumayr, self.palmyra, self.renemouawad])
        self.add_controlpoint(self.renemouawad, connected_to=[self.alqusair, self.basselAlAssad])
        self.add_controlpoint(self.hama, connected_to=[self.aleppo, self.alqusair, self.basselAlAssad])
        self.add_controlpoint(self.basselAlAssad, connected_to=[self.hama, self.hatay, self.renemouawad])
        self.add_controlpoint(self.palmyra, connected_to=[self.tabqa, self.alqusair])
        self.add_controlpoint(self.tabqa, connected_to=[self.palmyra, self.jirah])
        self.add_controlpoint(self.jirah, connected_to=[self.tabqa, self.aleppo])
        self.add_controlpoint(self.aleppo, connected_to=[self.hama, self.jirah, self.minakh])
        self.add_controlpoint(self.minakh, connected_to=[self.hatay, self.aleppo, self.incirlik])
        self.add_controlpoint(self.hatay, connected_to=[self.minakh, self.basselAlAssad])
        self.add_controlpoint(self.incirlik, connected_to=[self.minakh])

        self.add_controlpoint(self.carrier)
        self.add_controlpoint(self.lha)

        self.ramatDavid.captured = True
        self.carrier.captured = True
        self.lha.captured = True

        self.hatay.captured_invert = True
        self.carrier.captured_invert = True
        self.lha.captured_invert = True


