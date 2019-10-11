from dcs.helicopters import Mi_8MT, Mi_24V
from dcs.planes import MiG_21Bis, MiG_23MLD, MiG_25PD, MiG_29A, Su_17M4, Su_24M, Su_25, IL_76MD, IL_78M, An_26B, An_30M, \
    Yak_40, A_50
from dcs.ships import CV_1143_5_Admiral_Kuznetsov, Dry_cargo_ship_Ivanov, Bulk_cargo_ship_Yakushev, Tanker_Elnya_160
from dcs.vehicles import AirDefence, Armor, Unarmed, Infantry

Russia_1975 = {
    "country": "Russia",
    "side": "red",
    "units": [

        MiG_21Bis,
        MiG_23MLD,
        MiG_25PD,
        MiG_29A,

        Su_17M4,
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

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,
        Infantry.Soldier_AK,

        CV_1143_5_Admiral_Kuznetsov,
        Bulk_cargo_ship_Yakushev,
        Dry_cargo_ship_Ivanov,
        Tanker_Elnya_160
    ]
}