from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

from pydcs_extensions.a4ec.a4ec import A_4E_C

Israel_1973 = {
    "country": "Israel",
    "side": "blue",
    "units":[
        F_4E,
        A_4E_C,

        KC_135,
        KC130,
        C_130,
        E_3A,

        UH_1H,

        Armor.MT_M4A4_Sherman_Firefly,
        Armor.APC_M2A1,
        Armor.MBT_M60A3_Patton,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,

        AirDefence.SAM_Hawk_PCP,
        AirDefence.AAA_Bofors_40mm,
        AirDefence.SAM_Chaparral_M48,

        Armed_speedboat,
    ], "requirements": {
        "Community A-4E": "https://heclak.github.io/community-a4e-c/",
        "WW2 Asset Pack": "https://www.digitalcombatsimulator.com/en/products/other/wwii_assets_pack/",
    }, "shorad": [
        AirDefence.SAM_Chaparral_M48,
        AirDefence.AAA_Bofors_40mm
    ], "boat": [
    ], "has_jtac": True
}

Israel_1973_NO_WW2_UNITS = {
    "country": "Israel",
    "side": "blue",
    "units":[
        F_4E,
        A_4E_C,

        KC_135,
        KC130,
        C_130,
        E_3A,

        UH_1H,

        Armor.MBT_M60A3_Patton,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,

        AirDefence.SAM_Hawk_PCP,
        AirDefence.SAM_Chaparral_M48,

        Armed_speedboat,
    ], "requirements": {
        "Community A-4E": "https://heclak.github.io/community-a4e-c/",
    }, "shorad": [
        AirDefence.SAM_Chaparral_M48,
    ], "boat": [
    ], "has_jtac": True
}