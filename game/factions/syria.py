from dcs.helicopters import (
    Mi_24V,
    Mi_8MT,
    SA342L,
    SA342M,
)
from dcs.planes import (
    A_50,
    An_26B,
    An_30M,
    IL_76MD,
    IL_78M,
    L_39ZA,
    MiG_15bis,
    MiG_19P,
    MiG_21Bis,
    MiG_23MLD,
    MiG_25PD,
    MiG_29S,
    SpitfireLFMkIX,
    SpitfireLFMkIXCW,
    Su_17M4,
    Su_24M,
    Yak_40,
)
from dcs.vehicles import (
    AirDefence,
    Armor,
    Artillery,
    Infantry,
    Unarmed,
)

Syria_2011 = {
    "country": "Syria",
    "side": "red",
    "units": [

        MiG_21Bis,
        MiG_23MLD,
        MiG_25PD,
        MiG_29S,

        Su_17M4,
        Su_24M,

        L_39ZA,

        Mi_24V,
        Mi_8MT,
        SA342M,
        SA342L,

        IL_76MD,
        IL_78M,
        An_26B,
        An_30M,
        Yak_40,
        A_50,

        AirDefence.SAM_SA_6_Kub_LN_2P25,
        AirDefence.SAM_SA_3_S_125_LN_5P73,
        AirDefence.SAM_SA_2_LN_SM_90,
        AirDefence.SAM_SA_8_Osa_9A33,
        AirDefence.SAM_SA_11_Buk_LN_9A310M1,
        AirDefence.SAM_SA_10_S_300PS_LN_5P85C,

        Armor.IFV_BMP_1,
        Armor.IFV_BMP_2,
        Armor.APC_BTR_80,
        Armor.ARV_BRDM_2,
        Armor.APC_MTLB,
        Armor.APC_Cobra,
        Armor.MBT_T_55,
        Armor.MBT_T_72B,
        Armor.MBT_T_90,
        Artillery.MLRS_BM_21_Grad,
        Artillery.MLRS_9K57_Uragan_BM_27,
        Artillery.SPH_2S1_Gvozdika,
        Artillery.SPH_2S9_Nona,

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,

        Infantry.Paratrooper_RPG_16,
        Infantry.Soldier_AK

    ],
    "shorad": [
        AirDefence.SAM_SA_8_Osa_9A33,
        AirDefence.SAM_SA_13_Strela_10M3_9A35M3,
        AirDefence.SAM_SA_9_Strela_1_9P31,
        AirDefence.SAM_SA_19_Tunguska_2S6,
        AirDefence.AAA_ZU_23_on_Ural_375,
    ], "boat": [
        "GrishaGroupGenerator", "MolniyaGroupGenerator"
    ]
}

Syria_1973 = {
    "country": "Syria",
    "side": "red",
    "units": [

        MiG_21Bis,
        MiG_19P,
        MiG_15bis,  # Standing as Mig-17

        Su_17M4,  # Standing as Su-7
        Mi_8MT,

        IL_76MD,
        IL_78M,
        An_26B,
        An_30M,
        Yak_40,

        AirDefence.SAM_SA_6_Kub_LN_2P25,
        AirDefence.SAM_SA_3_S_125_LN_5P73,
        AirDefence.SAM_SA_2_LN_SM_90,

        Armor.IFV_BMP_1,
        Armor.APC_MTLB,
        Armor.MBT_T_55,
        Artillery.MLRS_BM_21_Grad,

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,

        Infantry.Paratrooper_RPG_16,
        Infantry.Soldier_AK

    ],
    "shorad": [
        AirDefence.AAA_ZU_23_on_Ural_375,
    ], "boat": [
        "GrishaGroupGenerator"
    ]
}


Syria_1982 = {
    "country": "Syria",
    "side": "red",
    "units": [

        MiG_21Bis,
        MiG_23MLD,
        MiG_25PD,
        MiG_19P,

        Su_17M4,  # Standing as Su-7
        Mi_8MT,

        IL_76MD,
        IL_78M,
        An_26B,
        An_30M,
        Yak_40,

        AirDefence.SAM_SA_6_Kub_LN_2P25,
        AirDefence.SAM_SA_3_S_125_LN_5P73,
        AirDefence.SAM_SA_2_LN_SM_90,

        Armor.IFV_BMP_1,
        Armor.APC_MTLB,
        Armor.MBT_T_55,
        Armor.MBT_T_72B,
        Artillery.MLRS_BM_21_Grad,

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,

        Infantry.Paratrooper_RPG_16,
        Infantry.Soldier_AK

    ],
    "shorad": [
        AirDefence.AAA_ZU_23_on_Ural_375,
    ], "boat": [
        "GrishaGroupGenerator"
    ]
}


Syria_1967 = {
    "country": "Syria",
    "side": "red",
    "units": [

        MiG_21Bis,
        MiG_19P,
        MiG_15bis,  # Standing as Mig-17

        Su_17M4,  # Standing as Su-7
        Mi_8MT,

        IL_76MD,
        IL_78M,
        An_26B,
        An_30M,
        Yak_40,

        AirDefence.SAM_SA_2_LN_SM_90,

        Armor.ARV_BRDM_2,
        Armor.MBT_T_55,
        Artillery.MLRS_BM_21_Grad,

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,

        Infantry.Paratrooper_RPG_16,
        Infantry.Soldier_AK

    ],
    "shorad": [
        AirDefence.AAA_ZU_23_on_Ural_375,
    ], "boat": [
        "GrishaGroupGenerator"
    ]
}

Syria_1967_WW2_Weapons = {
    "country": "Syria",
    "side": "red",
    "units": [

        MiG_21Bis,
        MiG_19P,
        MiG_15bis,  # Standing as Mig-17

        Su_17M4,  # Standing as Su-7
        Mi_8MT,

        IL_76MD,
        IL_78M,
        An_26B,
        An_30M,
        Yak_40,

        AirDefence.SAM_SA_2_LN_SM_90,

        Armor.ARV_BRDM_2,
        Armor.MBT_T_55,
        Armor.MT_Pz_Kpfw_IV_Ausf_H,
        Armor.StuG_III_Ausf__G,
        Armor.TD_Jagdpanzer_IV,
        Artillery.MLRS_BM_21_Grad,

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,

        Infantry.Soldier_RPG,
        Infantry.Soldier_AK

    ], "requirements": {
        "WW2 Asset Pack": "https://www.digitalcombatsimulator.com/en/products/other/wwii_assets_pack/",
    },
    "shorad": [
        AirDefence.AAA_ZU_23_on_Ural_375,
    ], "boat": [
        "GrishaGroupGenerator"
    ]
}

Arab_Armies_1948 = {
    "country": "Syria",
    "side": "red",
    "units": [
        SpitfireLFMkIX,
        SpitfireLFMkIXCW,

        AirDefence.SAM_SA_2_LN_SM_90,

        Armor.MT_M4_Sherman,
        Armor.MT_Pz_Kpfw_IV_Ausf_H,
        Armor.APC_Sd_Kfz_251,
        Armor.IFV_Sd_Kfz_234_2_Puma,

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,

        Infantry.Infantry_SMLE_No_4_Mk_1,

        AirDefence.AAA_8_8cm_Flak_36,

    ], "requirements": {
        "WW2 Asset Pack": "https://www.digitalcombatsimulator.com/en/products/other/wwii_assets_pack/",
    },
    "shorad": [
        AirDefence.AAA_8_8cm_Flak_36,
    ], "boat": [
        "GrishaGroupGenerator"
    ]
}
