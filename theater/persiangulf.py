from dcs.terrain import persiangulf
from dcs import mapping

from .conflicttheater import *
from .base import *
from .landmap import load_landmap


class PersianGulfTheater(ConflictTheater):
    terrain = dcs.terrain.PersianGulf()
    overview_image = "persiangulf.gif"
    reference_points = {
        (persiangulf.Shiraz_International_Airport.position.x, persiangulf.Shiraz_International_Airport.position.y): (772, -1970),
        (persiangulf.Liwa_Airbase.position.x, persiangulf.Liwa_Airbase.position.y): (1188, 78), }
    landmap = load_landmap("resources\\gulflandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (8, 16),
        "dusk": (16, 18),
        "night": (0, 5),
    }


    def __init__(self):
        super(PersianGulfTheater, self).__init__()

        self.al_dhafra = ControlPoint.from_airport(persiangulf.Al_Dhafra_AB, LAND, SIZE_BIG, IMPORTANCE_LOW)
        self.al_maktoum = ControlPoint.from_airport(persiangulf.Al_Maktoum_Intl, LAND, SIZE_BIG, IMPORTANCE_LOW)
        self.al_minhad = ControlPoint.from_airport(persiangulf.Al_Minhad_AB, LAND, SIZE_REGULAR, 1.1)
        self.sir_abu_nuayr = ControlPoint.from_airport(persiangulf.Sir_Abu_Nuayr, [0, 330], SIZE_SMALL, 1.1,has_frontline=False)
        self.dubai = ControlPoint.from_airport(persiangulf.Dubai_Intl, COAST_DL_E, SIZE_LARGE, IMPORTANCE_MEDIUM)
        self.sharjah = ControlPoint.from_airport(persiangulf.Sharjah_Intl, LAND, SIZE_BIG, 1.0)
        self.fujairah = ControlPoint.from_airport(persiangulf.Fujairah_Intl, COAST_V_W, SIZE_REGULAR, 1.0)
        self.khasab = ControlPoint.from_airport(persiangulf.Khasab, LAND, SIZE_SMALL, IMPORTANCE_MEDIUM)
        self.sirri = ControlPoint.from_airport(persiangulf.Sirri_Island, COAST_DL_W, SIZE_REGULAR, IMPORTANCE_LOW,has_frontline=False)
        self.abu_musa = ControlPoint.from_airport(persiangulf.Abu_Musa_Island_Airport, LAND, SIZE_SMALL,IMPORTANCE_MEDIUM, has_frontline=False)
        self.tunb_island = ControlPoint.from_airport(persiangulf.Tunb_Island_AFB, [0, 270, 330], SIZE_SMALL,IMPORTANCE_MEDIUM, has_frontline=False)
        self.tunb_kochak = ControlPoint.from_airport(persiangulf.Tunb_Kochak, [135, 180], SIZE_SMALL, 1.1,has_frontline=False)
        self.bandar_lengeh = ControlPoint.from_airport(persiangulf.Bandar_Lengeh, [270, 315, 0, 45], SIZE_SMALL,IMPORTANCE_HIGH)
        self.qeshm = ControlPoint.from_airport(persiangulf.Qeshm_Island, [270, 315, 0, 45, 90, 135, 180], SIZE_SMALL,1.1, has_frontline=False)
        self.havadarya = ControlPoint.from_airport(persiangulf.Havadarya, COAST_DL_W, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.bandar_abbas = ControlPoint.from_airport(persiangulf.Bandar_Abbas_Intl, LAND, SIZE_BIG, IMPORTANCE_HIGH)
        self.lar = ControlPoint.from_airport(persiangulf.Lar_Airbase, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.shiraz = ControlPoint.from_airport(persiangulf.Shiraz_International_Airport, LAND, SIZE_BIG,IMPORTANCE_HIGH)
        self.kerman = ControlPoint.from_airport(persiangulf.Kerman_Airport, LAND, SIZE_BIG, IMPORTANCE_HIGH)
        self.ras_al_khaimah = ControlPoint.from_airport(persiangulf.Ras_Al_Khaimah, LAND, SIZE_REGULAR,IMPORTANCE_MEDIUM)
        self.al_ain = ControlPoint.from_airport(persiangulf.Al_Ain_International_Airport, LAND, SIZE_BIG,IMPORTANCE_HIGH)
        self.liwa = ControlPoint.from_airport(persiangulf.Liwa_Airbase, LAND, SIZE_BIG, IMPORTANCE_HIGH)
        self.jiroft = ControlPoint.from_airport(persiangulf.Jiroft_Airport, LAND, SIZE_BIG, IMPORTANCE_HIGH)
        self.bandar_e_jask = ControlPoint.from_airport(persiangulf.Bandar_e_Jask_airfield, LAND, SIZE_TINY,IMPORTANCE_LOW)
        self.west_carrier = ControlPoint.carrier("West carrier", Point(-69043.813952358, -159916.65947136), 1001)
        self.east_carrier = ControlPoint.carrier("East carrier", Point(59514.324335475, 28165.517980635), 1002)

        self.add_controlpoint(self.liwa, connected_to=[self.al_dhafra])
        self.add_controlpoint(self.al_dhafra, connected_to=[self.liwa, self.al_maktoum, self.al_ain])
        self.add_controlpoint(self.al_ain, connected_to=[self.al_dhafra, self.al_maktoum])
        self.add_controlpoint(self.al_maktoum, connected_to=[self.al_dhafra, self.al_minhad, self.al_ain])
        self.add_controlpoint(self.al_minhad, connected_to=[self.al_maktoum, self.dubai])
        self.add_controlpoint(self.dubai, connected_to=[self.al_minhad, self.sharjah, self.fujairah])
        self.add_controlpoint(self.sharjah, connected_to=[self.dubai, self.ras_al_khaimah])
        self.add_controlpoint(self.ras_al_khaimah, connected_to=[self.sharjah, self.khasab])
        self.add_controlpoint(self.fujairah, connected_to=[self.dubai, self.khasab])
        self.add_controlpoint(self.khasab, connected_to=[self.ras_al_khaimah, self.fujairah])

        self.add_controlpoint(self.sir_abu_nuayr, connected_to=[])
        self.add_controlpoint(self.sirri, connected_to=[])
        self.add_controlpoint(self.abu_musa, connected_to=[])
        self.add_controlpoint(self.tunb_kochak, connected_to=[])

        self.add_controlpoint(self.tunb_island, connected_to=[])
        self.add_controlpoint(self.bandar_lengeh, connected_to=[self.lar, self.qeshm])
        self.add_controlpoint(self.qeshm, connected_to=[self.bandar_lengeh, self.havadarya])
        self.add_controlpoint(self.havadarya, connected_to=[self.lar, self.qeshm, self.bandar_abbas])
        self.add_controlpoint(self.bandar_abbas, connected_to=[self.havadarya, self.kerman])

        self.add_controlpoint(self.shiraz, connected_to=[self.lar, self.kerman])
        self.add_controlpoint(self.kerman, connected_to=[self.lar, self.shiraz, self.bandar_abbas])
        self.add_controlpoint(self.lar, connected_to=[self.havadarya, self.shiraz, self.kerman])

        self.add_controlpoint(self.west_carrier)
        self.add_controlpoint(self.east_carrier)

        self.west_carrier.captured = True
        self.east_carrier.captured = True
        self.liwa.captured = True


class IranianCampaign(ConflictTheater):

    terrain = dcs.terrain.PersianGulf()
    overview_image = "persiangulf.gif"
    reference_points = {
        (persiangulf.Shiraz_International_Airport.position.x, persiangulf.Shiraz_International_Airport.position.y): (
        772, -1970),
        (persiangulf.Liwa_Airbase.position.x, persiangulf.Liwa_Airbase.position.y): (1188, 78), }
    landmap = load_landmap("resources\\gulflandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (8, 16),
        "dusk": (16, 18),
        "night": (0, 5),
    }

    def __init__(self):
        super(IranianCampaign, self).__init__()
        self.al_dhafra = ControlPoint.from_airport(persiangulf.Al_Dhafra_AB, LAND, SIZE_BIG, IMPORTANCE_LOW)
        self.al_maktoum = ControlPoint.from_airport(persiangulf.Al_Maktoum_Intl, LAND, SIZE_BIG, IMPORTANCE_LOW)
        self.al_minhad = ControlPoint.from_airport(persiangulf.Al_Minhad_AB, LAND, SIZE_REGULAR, 1.1)
        self.sir_abu_nuayr = ControlPoint.from_airport(persiangulf.Sir_Abu_Nuayr, [0, 330], SIZE_SMALL, 1.1,has_frontline=False)
        self.dubai = ControlPoint.from_airport(persiangulf.Dubai_Intl, COAST_DL_E, SIZE_LARGE, IMPORTANCE_MEDIUM)
        self.sharjah = ControlPoint.from_airport(persiangulf.Sharjah_Intl, LAND, SIZE_BIG, 1.0)
        self.fujairah = ControlPoint.from_airport(persiangulf.Fujairah_Intl, COAST_V_W, SIZE_REGULAR, 1.0)
        self.khasab = ControlPoint.from_airport(persiangulf.Khasab, LAND, SIZE_SMALL, IMPORTANCE_MEDIUM)
        self.sirri = ControlPoint.from_airport(persiangulf.Sirri_Island, COAST_DL_W, SIZE_REGULAR, IMPORTANCE_LOW,has_frontline=False)
        self.abu_musa = ControlPoint.from_airport(persiangulf.Abu_Musa_Island_Airport, LAND, SIZE_SMALL,IMPORTANCE_MEDIUM, has_frontline=False)
        self.tunb_island = ControlPoint.from_airport(persiangulf.Tunb_Island_AFB, [0, 270, 330], SIZE_SMALL,IMPORTANCE_MEDIUM, has_frontline=False)
        self.tunb_kochak = ControlPoint.from_airport(persiangulf.Tunb_Kochak, [135, 180], SIZE_SMALL, 1.1,has_frontline=False)
        self.bandar_lengeh = ControlPoint.from_airport(persiangulf.Bandar_Lengeh, [270, 315, 0, 45], SIZE_SMALL,IMPORTANCE_HIGH)
        self.qeshm = ControlPoint.from_airport(persiangulf.Qeshm_Island, [270, 315, 0, 45, 90, 135, 180], SIZE_SMALL,1.1, has_frontline=False)
        self.havadarya = ControlPoint.from_airport(persiangulf.Havadarya, COAST_DL_W, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.bandar_abbas = ControlPoint.from_airport(persiangulf.Bandar_Abbas_Intl, LAND, SIZE_BIG, IMPORTANCE_HIGH)
        self.lar = ControlPoint.from_airport(persiangulf.Lar_Airbase, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.shiraz = ControlPoint.from_airport(persiangulf.Shiraz_International_Airport, LAND, SIZE_BIG,IMPORTANCE_HIGH)
        self.kerman = ControlPoint.from_airport(persiangulf.Kerman_Airport, LAND, SIZE_BIG, IMPORTANCE_HIGH)
        self.jiroft = ControlPoint.from_airport(persiangulf.Jiroft_Airport, LAND, SIZE_BIG, IMPORTANCE_HIGH)
        self.bandar_e_jask = ControlPoint.from_airport(persiangulf.Bandar_e_Jask_airfield, LAND, SIZE_TINY,IMPORTANCE_LOW)
        self.ras_al_khaimah = ControlPoint.from_airport(persiangulf.Ras_Al_Khaimah, LAND, SIZE_REGULAR,IMPORTANCE_MEDIUM)

        self.east_carrier = ControlPoint.carrier("East carrier", Point(59514.324335475, 28165.517980635), 1001)
        self.west_carrier = ControlPoint.lha("Tarawa", Point(-27500.813952358, -147000.65947136), 1002)

        self.add_controlpoint(self.ras_al_khaimah, connected_to=[self.khasab])
        self.add_controlpoint(self.khasab, connected_to=[self.ras_al_khaimah])

        self.add_controlpoint(self.bandar_lengeh, connected_to=[self.lar])
        self.add_controlpoint(self.qeshm, connected_to=[])
        self.add_controlpoint(self.havadarya, connected_to=[self.lar, self.bandar_abbas])
        self.add_controlpoint(self.bandar_abbas, connected_to=[self.havadarya, self.jiroft])

        self.add_controlpoint(self.shiraz, connected_to=[self.lar, self.kerman])
        self.add_controlpoint(self.jiroft, connected_to=[self.kerman, self.bandar_abbas])
        self.add_controlpoint(self.kerman, connected_to=[self.lar, self.shiraz, self.jiroft])
        self.add_controlpoint(self.lar, connected_to=[self.bandar_lengeh, self.havadarya, self.shiraz, self.kerman])

        self.add_controlpoint(self.east_carrier)
        self.add_controlpoint(self.west_carrier)

        self.east_carrier.captured = True
        self.west_carrier.captured = True
        self.al_dhafra.captured = True
        self.ras_al_khaimah.captured = True
        self.khasab.captured = True
        self.qeshm.captured = True
        self.havadarya.captured = True
        self.bandar_abbas.captured = True


class Emirates(ConflictTheater):
    terrain = dcs.terrain.PersianGulf()
    overview_image = "persiangulf.gif"
    reference_points = {
        (persiangulf.Shiraz_International_Airport.position.x, persiangulf.Shiraz_International_Airport.position.y): (
        772, -1970),
        (persiangulf.Liwa_Airbase.position.x, persiangulf.Liwa_Airbase.position.y): (1188, 78), }
    landmap = load_landmap("resources\\gulflandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (8, 16),
        "dusk": (16, 18),
        "night": (0, 5),
    }


    def __init__(self):
        super(Emirates, self).__init__()

        self.al_dhafra = ControlPoint.from_airport(persiangulf.Al_Dhafra_AB, LAND, SIZE_BIG, IMPORTANCE_MEDIUM)
        self.al_maktoum = ControlPoint.from_airport(persiangulf.Al_Maktoum_Intl, LAND, SIZE_BIG, IMPORTANCE_LOW)
        self.al_minhad = ControlPoint.from_airport(persiangulf.Al_Minhad_AB, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.sharjah = ControlPoint.from_airport(persiangulf.Sharjah_Intl, LAND, SIZE_BIG, IMPORTANCE_LOW)
        self.fujairah = ControlPoint.from_airport(persiangulf.Fujairah_Intl, COAST_V_W, SIZE_REGULAR, IMPORTANCE_LOW)
        self.ras_al_khaimah = ControlPoint.from_airport(persiangulf.Ras_Al_Khaimah, LAND, SIZE_REGULAR,IMPORTANCE_LOW)
        self.al_ain = ControlPoint.from_airport(persiangulf.Al_Ain_International_Airport, LAND, SIZE_BIG,IMPORTANCE_LOW)

        self.east_carrier = ControlPoint.carrier("Carrier", Point(-61770, 69039), 1001)
        self.tarawa_carrier = ControlPoint.lha("LHA Carrier", Point(-79770, 49430), 1002)

        self.add_controlpoint(self.al_dhafra, connected_to=[self.al_ain, self.al_maktoum])
        self.add_controlpoint(self.al_ain, connected_to=[self.fujairah, self.al_maktoum, self.al_dhafra])
        self.add_controlpoint(self.al_maktoum, connected_to=[self.al_dhafra, self.al_minhad, self.al_ain])
        self.add_controlpoint(self.al_minhad, connected_to=[self.al_maktoum, self.sharjah])
        self.add_controlpoint(self.sharjah, connected_to=[self.al_minhad, self.ras_al_khaimah, self.fujairah])
        self.add_controlpoint(self.ras_al_khaimah, connected_to=[self.sharjah])
        self.add_controlpoint(self.fujairah, connected_to=[self.sharjah, self.al_ain])

        self.add_controlpoint(self.tarawa_carrier)
        self.add_controlpoint(self.east_carrier)

        self.tarawa_carrier.captured = True
        self.east_carrier.captured = True
        self.fujairah.captured = True
