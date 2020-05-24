from dcs.vehicles import *
from dcs.ships import *
from dcs.planes import *
from dcs.helicopters import *

Russia_1990 = {
    "country": "Russia",
    "side": "red",
    "units": [

        MiG_23MLD,
        MiG_25PD,
        MiG_29A,
        MiG_29S,
        MiG_31,
        Su_27,

        Su_24M,
        Su_25,

        IL_76MD,
        IL_78M,
        An_26B,
        An_30M,
        Yak_40,

        A_50,

        Mi_8MT,
        Mi_24V,

        AirDefence.AAA_ZU_23_Closed,
        AirDefence.SAM_SA_6_Kub_LN_2P25,
        AirDefence.SAM_SA_3_S_125_LN_5P73,

        Armor.ARV_BRDM_2,
        Armor.APC_BTR_80,
        Armor.IFV_BMD_1,
        Armor.IFV_BMP_1,
        Armor.MBT_T_55,
        Artillery.MLRS_9K57_Uragan_BM_27,
        Artillery.SPH_2S19_Msta,

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,

        CV_1143_5_Admiral_Kuznetsov,
        Bulk_cargo_ship_Yakushev,
        Dry_cargo_ship_Ivanov,
        Tanker_Elnya_160,

        # Infantry squad
        Infantry.Paratrooper_AKS,
        Infantry.Infantry_Soldier_Rus,
        Infantry.Paratrooper_RPG_16,
    ],
    "shorad":[
        AirDefence.SAM_SA_9_Strela_1_9P31,
        AirDefence.SAM_SA_13_Strela_10M3_9A35M3,
        AirDefence.SPAAA_ZSU_23_4_Shilka
    ], "aircraft_carrier": [
        CV_1143_5_Admiral_Kuznetsov,
    ], "destroyer": [
        FF_1135M_Rezky,
    ], "cruiser": [
        FSG_1241_1MP_Molniya,
    ]
}