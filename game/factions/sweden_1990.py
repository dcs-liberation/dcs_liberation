from dcs.vehicles import *
from dcs.ships import *
from dcs.planes import *
from dcs.helicopters import *

Sweden_1990 = {
    "country": "Sweden",
    "side": "blue",
    "units": [
        AJS37,

        UH_1H,

        AirDefence.SAM_Hawk_PCP,

        Armor.IFV_MCV_80, # Standing  as Strf 90
        Armor.MBT_Leopard_2,
        Armor.APC_M1126_Stryker_ICV, # Closest thing available

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,
        Infantry.Soldier_AK,
        CV_1143_5_Admiral_Kuznetsov,
        Bulk_cargo_ship_Yakushev,
        Dry_cargo_ship_Ivanov,
        Tanker_Elnya_160,
    ],
    "shorad": [
        AirDefence.SAM_Avenger_M1097
    ], "has_jtac": True
}