from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

Israel_1948 = {
    "country": "Israel",
    "side": "blue",
    "units":[
        SpitfireLFMkIXCW,
        SpitfireLFMkIX,
        P_51D,
        P_51D_30_NA,
        Bf_109K_4, # Standing as Avia S-199
        B_17G,

        Armor.MT_M4A4_Sherman_Firefly,
        Armor.APC_M2A1,
        Armor.MT_M4_Sherman,
        Armor.LAC_M8_Greyhound,

        Unarmed.Transport_M818,
        Infantry.Infantry_SMLE_No_4_Mk_1,

        AirDefence.AAA_Bofors_40mm,
        Armed_speedboat,
    ],"requirements":{
        "WW2 Asset Pack": "https://www.digitalcombatsimulator.com/en/products/other/wwii_assets_pack/",
    },
    "shorad": [
        AirDefence.AAA_Bofors_40mm
    ], "boat": [
    ], "has_jtac": False
}