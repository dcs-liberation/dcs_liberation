from dcs.vehicles import *
from dcs.ships import *
from dcs.planes import *
from dcs.helicopters import *

China_2000 = {
    "country": "China",
    "side": "red",
    "units": [

        MiG_21Bis, # Standing as J-7
        Su_30,
        J_11A,

        IL_76MD,
        IL_78M,
        An_26B,
        An_30M,
        Yak_40,

        A_50,

        Mi_8MT,

        AirDefence.SAM_SA_10_S_300PS_LN_5P85C, # Standing as HQ-9+
        AirDefence.SAM_SA_6_Kub_LN_2P25,
        AirDefence.HQ_7_Self_Propelled_LN,

        Armor.MBT_T_72B, # Type 99
        Armor.MBT_T_55,
        Armor.ZBD_04A,
        Armor.IFV_BMP_1,

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,
        Infantry.Soldier_AK,

        CV_1143_5_Admiral_Kuznetsov,
        Bulk_cargo_ship_Yakushev,
        Dry_cargo_ship_Ivanov,
        Tanker_Elnya_160
    ],
    "shorad":[
        AirDefence.AAA_ZU_23_Closed,
        AirDefence.Rapier_FSA_Launcher, # Standing as PL-9C Shorad
        AirDefence.HQ_7_Self_Propelled_LN
    ], "aircraft_carrier": [
        CV_1143_5_Admiral_Kuznetsov,
    ], "destroyer": [
        Type_052B_Destroyer,
        Type_052C_Destroyer
    ], "cruiser": [
        Type_054A_Frigate,
    ]
}