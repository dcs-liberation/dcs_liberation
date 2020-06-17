from dcs.helicopters import Mi_8MT
from dcs.planes import MiG_15bis, MiG_19P, MiG_21Bis, IL_76MD, IL_78M, An_26B, An_30M, Yak_40, A_50
from dcs.ships import CV_1143_5_Admiral_Kuznetsov, Bulk_cargo_ship_Yakushev, Dry_cargo_ship_Ivanov, Tanker_Elnya_160
from dcs.vehicles import AirDefence, Armor, Unarmed, Infantry, Artillery

Russia_1965 = {
    "country": "Russia",
    "side": "red",
    "units": [
        MiG_15bis,
        MiG_19P,
        MiG_21Bis,

        IL_76MD,
        IL_78M,
        An_26B,
        An_30M,
        Yak_40,

        A_50,

        Mi_8MT,

        AirDefence.SAM_SA_6_Kub_LN_2P25,
        AirDefence.SAM_SA_2_LN_SM_90,
        AirDefence.SAM_SA_3_S_125_LN_5P73,

        Armor.ARV_BRDM_2,
        Armor.APC_BTR_80,
        Armor.ARV_BTR_RD,
        Armor.IFV_BMD_1,
        Armor.IFV_BMP_1,
        Armor.MBT_T_55,
        Artillery.MLRS_BM_21_Grad,

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
        AirDefence.AAA_ZU_23_Closed
    ], "boat": [
        "GrishaGroupGenerator"
    ]
}