from dcs.helicopters import (
    AH_64D,
)
from dcs.planes import (
    C_130,
    E_3A,
    F_16C_50,
    KC130,
    KC_135,
    M_2000C,
    Mirage_2000_5,
    WingLoong_I,
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

UAE_2005 = {
    "country": "United Arab Emirates",
    "side": "blue",
    "units":[
        M_2000C,
        Mirage_2000_5,
        F_16C_50,

        KC_135,
        KC130,
        C_130,
        E_3A,

        AH_64D,

        Armor.MBT_Leclerc,
        Armor.IFV_BMP_3,
        Armor.TPz_Fuchs,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,

        AirDefence.Rapier_FSA_Launcher,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ], "boat":[
        "OliverHazardPerryGroupGenerator"
    ],
    "has_jtac": True,
    "jtac_unit": WingLoong_I
}