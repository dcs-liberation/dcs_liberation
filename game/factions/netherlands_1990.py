from dcs.helicopters import (
    AH_64A,
)
from dcs.planes import (
    C_130,
    E_3A,
    F_16C_50,
    F_5E_3,
    KC130,
    KC_135,
)
from dcs.ships import (
    Armed_speedboat,
    CVN_74_John_C__Stennis,
    LHA_1_Tarawa,
)
from dcs.vehicles import (
    AirDefence,
    Armor,
    Infantry,
    Unarmed,
)

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
