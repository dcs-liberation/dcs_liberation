from dcs.helicopters import (
    AH_1W,
    AH_64D,
)
from dcs.planes import (
    C_130,
    E_3A,
    F_15C,
    F_15E,
    F_16C_50,
    F_4E,
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
    Artillery,
    Infantry,
    Unarmed,
)

Israel_2000 = {
    "country": "Israel",
    "side": "blue",
    "units":[
        F_16C_50,
        F_15C,
        F_15E,
        F_4E,

        KC_135,
        KC130,
        C_130,
        E_3A,

        AH_1W,
        AH_64D,

        Armor.MBT_Merkava_Mk__4,
        Armor.APC_M113,
        Armor.APC_M1043_HMMWV_Armament,
        Armor.ATGM_M1045_HMMWV_TOW,
        Artillery.SPH_M109_Paladin,
        Artillery.MLRS_M270,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,

        AirDefence.SAM_Patriot_EPP_III,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ],
    "shorad": [
        AirDefence.SAM_Avenger_M1097
    ], "boat": [
        "ArleighBurkeGroupGenerator"
    ], "has_jtac": True
}