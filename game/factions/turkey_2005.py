from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

Turkey_2005 = {
    "country": "Turkey",
    "side": "blue",
    "units":[
        F_16C_50,
        F_4E,

        KC_135,
        KC130,
        C_130,
        E_3A,

        UH_1H,
        AH_1W,

        Armor.MBT_Leopard_2,
        Armor.MBT_Leopard_1A3,
        Armor.MBT_M60A3_Patton,
        Armor.APC_Cobra,
        Armor.APC_BTR_80,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,

        AirDefence.SAM_Avenger_M1097,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ], "shorad":[
        AirDefence.AAA_ZU_23_Emplacement,
        AirDefence.SPAAA_ZSU_23_4_Shilka
    ], "boat":[
        "OliverHazardPerryGroupGenerator"
    ], "has_jtac": True
}