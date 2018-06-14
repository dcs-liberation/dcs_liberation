from dcs.terrain import persiangulf
from dcs import mapping

from .conflicttheater import *
from .base import *


class PersianGulfTheater(ConflictTheater):
    al_dhafra = ControlPoint.from_airport(persiangulf.Al_Dhafra_AB, ALL_RADIALS, SIZE_BIG, IMPORTANCE_LOW)
    al_maktoum = ControlPoint.from_airport(persiangulf.Al_Maktoum_Intl, ALL_RADIALS, SIZE_BIG, IMPORTANCE_LOW)
    al_minhad = ControlPoint.from_airport(persiangulf.Al_Minhad_AB, ALL_RADIALS, SIZE_REGULAR, IMPORTANCE_LOW)
    sir_abu_nuayr = ControlPoint.from_airport(persiangulf.Sir_Abu_Nuayr, ALL_RADIALS, SIZE_SMALL, IMPORTANCE_LOW)

    dubai = ControlPoint.from_airport(persiangulf.Dubai_Intl, COAST_SWNE, SIZE_LARGE, IMPORTANCE_MEDIUM)
    sharjah = ControlPoint.from_airport(persiangulf.Sharjah_Intl, ALL_RADIALS, SIZE_BIG, IMPORTANCE_MEDIUM)
    fujairah = ControlPoint.from_airport(persiangulf.Fujairah_Intl, COAST_NS_E, SIZE_REGULAR, IMPORTANCE_MEDIUM)
    khasab = ControlPoint.from_airport(persiangulf.Khasab, COAST_EW_S, SIZE_SMALL, IMPORTANCE_MEDIUM)

    sirri = ControlPoint.from_airport(persiangulf.Sirri_Island, ALL_RADIALS, SIZE_SMALL, IMPORTANCE_MEDIUM)
    abu_musa = ControlPoint.from_airport(persiangulf.Abu_Musa_Island_Airport, ALL_RADIALS, SIZE_SMALL, IMPORTANCE_MEDIUM)
    tunb_island = ControlPoint.from_airport(persiangulf.Tunb_Island_AFB, ALL_RADIALS, SIZE_SMALL, IMPORTANCE_HIGH)

    bandar_lengeh = ControlPoint.from_airport(persiangulf.Bandar_Lengeh, COAST_EW_N, SIZE_SMALL, IMPORTANCE_HIGH)
    qeshm = ControlPoint.from_airport(persiangulf.Qeshm_Island, COAST_EW_N, SIZE_SMALL, IMPORTANCE_HIGH)

    havadarya = ControlPoint.from_airport(persiangulf.Havadarya, COAST_SWNE, SIZE_REGULAR, IMPORTANCE_HIGH)
    bandar_abbas = ControlPoint.from_airport(persiangulf.Bandar_Abbas_Intl, COAST_EW_N, SIZE_BIG, IMPORTANCE_HIGH)
    lar = ControlPoint.from_airport(persiangulf.Lar_Airbase, ALL_RADIALS, SIZE_REGULAR, IMPORTANCE_HIGH)

    def __init__(self):
        super(PersianGulfTheater, self).__init__()

        self.add_controlpoint(self.al_dhafra, connected_to=[self.sir_abu_nuayr, self.al_maktoum])
        self.add_controlpoint(self.al_maktoum, connected_to=[self.al_dhafra, self.al_minhad, self.sir_abu_nuayr])
        self.add_controlpoint(self.dubai, connected_to=[self.sir_abu_nuayr, self.al_minhad, self.sharjah])
        self.add_controlpoint(self.sharjah, connected_to=[self.dubai, self.khasab])
        self.add_controlpoint(self.fujairah, connected_to=[self.dubai, self.khasab])
        self.add_controlpoint(self.khasab, connected_to=[self.sharjah, self.fujairah, self.tunb_island])

        self.add_controlpoint(self.sir_abu_nuayr, connected_to=[self.al_dhafra, self.al_maktoum, self.dubai])
        self.add_controlpoint(self.sirri, connected_to=[self.sir_abu_nuayr, self.abu_musa, self.tunb_island])
        self.add_controlpoint(self.abu_musa, connected_to=[self.sirri, self.sir_abu_nuayr, self.tunb_island])

        self.add_controlpoint(self.tunb_island, connected_to=[self.khasab, self.abu_musa, self.sirri, self.qeshm])
        self.add_controlpoint(self.bandar_lengeh, connected_to=[self.tunb_island, self.lar, self.qeshm])
        self.add_controlpoint(self.qeshm, connected_to=[self.bandar_lengeh, self.havadarya, self.tunb_island])
        self.add_controlpoint(self.havadarya, connected_to=[self.lar, self.qeshm, self.bandar_abbas])
        self.add_controlpoint(self.bandar_abbas, connected_to=[self.havadarya])
        self.add_controlpoint(self.lar, connected_to=[self.bandar_lengeh, self.qeshm, self.havadarya])

        self.al_dhafra.captured = True
