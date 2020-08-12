from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

Netherlands_1990 = {
    "country": "The Netherlands",
    "side": "blue",
    "units": [
        F_16C_50,
        F_5E_3,

        KC_135,
        KC130,
        C_130,
        E_3A,

        AH_64A,

        Armor.APC_M113,
        Armor.MBT_Leopard_1A3,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,

        AirDefence.SAM_Hawk_PCP,
        AirDefence.SAM_Avenger_M1097,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ],
    "shorad": [
        AirDefence.SAM_Avenger_M1097
    ], "boat": [
        "OliverHazardPerryGroupGenerator"
    ], "has_jtac": True
}
