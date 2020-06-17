from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

NorthKorea_2000 = {
    "country": "North Korea",
    "side": "red",
    "units":[
        MiG_29A,
        Su_25,
        MiG_15bis,
        MiG_21Bis,
        MiG_23MLD,
        MiG_19P,

        IL_76MD,
        IL_78M,
        An_26B,
        An_30M,
        Yak_40,

        A_50,

        Mi_8MT,
        Mi_24V,

        Armor.MBT_T_55,
        Armor.MBT_T_72B,
        Armor.MBT_T_80U,
        Armor.IFV_BMP_1,
        Armor.APC_BTR_80,
        Armor.ARV_BRDM_2,

        Unarmed.Transport_M818,
        Infantry.Soldier_AK,

        AirDefence.SAM_SA_2_LN_SM_90,
        AirDefence.SAM_SA_3_S_125_LN_5P73,

        CV_1143_5_Admiral_Kuznetsov,
        Bulk_cargo_ship_Yakushev,
        Dry_cargo_ship_Ivanov,
        Tanker_Elnya_160
    ],
    "shorad":[
        AirDefence.AAA_ZU_23_Emplacement,
        AirDefence.SPAAA_ZSU_23_4_Shilka
    ],
    "boat": [
        "GrishaGroupGenerator", "MolniyaGroupGenerator"
    ]
}