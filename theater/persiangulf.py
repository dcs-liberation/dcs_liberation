from dcs.terrain import persiangulf
from dcs import mapping

from .conflicttheater import *
from .base import *
from .landmap import load_landmap


class PersianGulfTheater(ConflictTheater):
    terrain = dcs.terrain.PersianGulf()
    overview_image = "persiangulf.gif"
    reference_points = {(persiangulf.Sir_Abu_Nuayr.position.x, persiangulf.Sir_Abu_Nuayr.position.y): (321, 145),
                        (persiangulf.Sirri_Island.position.x, persiangulf.Sirri_Island.position.y): (347, 82), }
    landmap = load_landmap("resources\\gulflandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (8, 16),
        "dusk": (16, 18),
        "night": (0, 5),
    }

    al_dhafra = ControlPoint.from_airport(persiangulf.Al_Dhafra_AB, LAND, SIZE_BIG, IMPORTANCE_LOW)
    al_maktoum = ControlPoint.from_airport(persiangulf.Al_Maktoum_Intl, LAND, SIZE_BIG, IMPORTANCE_LOW)
    al_minhad = ControlPoint.from_airport(persiangulf.Al_Minhad_AB, LAND, SIZE_REGULAR, 1.1)
    sir_abu_nuayr = ControlPoint.from_airport(persiangulf.Sir_Abu_Nuayr, [0, 330], SIZE_SMALL, 1.1, has_frontline=False)

    dubai = ControlPoint.from_airport(persiangulf.Dubai_Intl, COAST_DL_E, SIZE_LARGE, IMPORTANCE_MEDIUM)
    sharjah = ControlPoint.from_airport(persiangulf.Sharjah_Intl, LAND, SIZE_BIG, 1.0)
    fujairah = ControlPoint.from_airport(persiangulf.Fujairah_Intl, COAST_V_W, SIZE_REGULAR, 1.0)
    khasab = ControlPoint.from_airport(persiangulf.Khasab, LAND, SIZE_SMALL, IMPORTANCE_MEDIUM)

    sirri = ControlPoint.from_airport(persiangulf.Sirri_Island, COAST_DL_W, SIZE_REGULAR, IMPORTANCE_LOW, has_frontline=False)
    abu_musa = ControlPoint.from_airport(persiangulf.Abu_Musa_Island_Airport, LAND, SIZE_SMALL, IMPORTANCE_MEDIUM, has_frontline=False)
    tunb_island = ControlPoint.from_airport(persiangulf.Tunb_Island_AFB, [0, 270, 330], SIZE_SMALL, IMPORTANCE_MEDIUM, has_frontline=False)
    tunb_kochak = ControlPoint.from_airport(persiangulf.Tunb_Kochak, [135, 180], SIZE_SMALL, 1.1, has_frontline=False)

    bandar_lengeh = ControlPoint.from_airport(persiangulf.Bandar_Lengeh, [270, 315, 0, 45], SIZE_SMALL, IMPORTANCE_HIGH)
    qeshm = ControlPoint.from_airport(persiangulf.Qeshm_Island, [270, 315, 0, 45, 90, 135, 180], SIZE_SMALL, 1.1, has_frontline=False)

    havadarya = ControlPoint.from_airport(persiangulf.Havadarya, COAST_DL_W, SIZE_REGULAR, IMPORTANCE_HIGH)
    bandar_abbas = ControlPoint.from_airport(persiangulf.Bandar_Abbas_Intl, LAND, SIZE_BIG, IMPORTANCE_HIGH)
    lar = ControlPoint.from_airport(persiangulf.Lar_Airbase, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
    shiraz = ControlPoint.from_airport(persiangulf.Shiraz_International_Airport, LAND, SIZE_BIG, IMPORTANCE_HIGH)
    kerman = ControlPoint.from_airport(persiangulf.Kerman_Airport, LAND, SIZE_BIG, IMPORTANCE_HIGH)

    west_carrier = ControlPoint.carrier("West carrier", Point(-69043.813952358, -159916.65947136))
    east_carrier = ControlPoint.carrier("East carrier", Point(59514.324335475, 28165.517980635))

    def __init__(self):
        super(PersianGulfTheater, self).__init__()

        self.add_controlpoint(self.shiraz, connected_to=[self.lar, self.kerman])
        self.add_controlpoint(self.kerman, connected_to=[self.lar, self.shiraz])
        self.add_controlpoint(self.lar, connected_to=[self.bandar_lengeh, self.qeshm, self.havadarya, self.shiraz, self.kerman])

        self.add_controlpoint(self.al_dhafra, connected_to=[self.sir_abu_nuayr, self.al_maktoum])
        self.add_controlpoint(self.al_maktoum, connected_to=[self.al_dhafra, self.al_minhad, self.sir_abu_nuayr])
        self.add_controlpoint(self.al_minhad, connected_to=[self.al_maktoum, self.dubai])
        self.add_controlpoint(self.dubai, connected_to=[self.al_minhad, self.sharjah])
        self.add_controlpoint(self.sharjah, connected_to=[self.dubai, self.khasab])
        self.add_controlpoint(self.fujairah, connected_to=[self.dubai, self.khasab])
        self.add_controlpoint(self.khasab, connected_to=[self.sharjah, self.fujairah, self.tunb_island])

        self.add_controlpoint(self.sir_abu_nuayr, connected_to=[self.al_dhafra, self.al_maktoum, self.sirri])
        self.add_controlpoint(self.sirri, connected_to=[self.sir_abu_nuayr, self.abu_musa])
        self.add_controlpoint(self.abu_musa, connected_to=[self.sirri, self.sir_abu_nuayr])
        self.add_controlpoint(self.tunb_kochak, connected_to=[self.sirri, self.abu_musa, self.tunb_island])

        self.add_controlpoint(self.tunb_island, connected_to=[self.khasab, self.qeshm, self.tunb_kochak])
        self.add_controlpoint(self.bandar_lengeh, connected_to=[self.tunb_island, self.lar, self.qeshm])
        self.add_controlpoint(self.qeshm, connected_to=[self.bandar_lengeh, self.havadarya, self.tunb_island, self.lar])
        self.add_controlpoint(self.havadarya, connected_to=[self.lar, self.qeshm, self.bandar_abbas])
        self.add_controlpoint(self.bandar_abbas, connected_to=[self.havadarya])

        self.add_controlpoint(self.west_carrier)
        self.add_controlpoint(self.east_carrier)

        self.west_carrier.captured = True
        self.east_carrier.captured = True
        self.al_dhafra.captured = True
