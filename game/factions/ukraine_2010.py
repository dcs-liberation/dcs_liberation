from dcs.helicopters import (
    Mi_24V,
    Mi_8MT,
)
from dcs.planes import (
    A_50,
    An_26B,
    An_30M,
    IL_76MD,
    IL_78M,
    L_39ZA,
    MiG_29S,
    Su_24M,
    Su_25,
    Su_25T,
    Su_27,
    Yak_40,
)
from dcs.ships import (
    Bulk_cargo_ship_Yakushev,
    CV_1143_5_Admiral_Kuznetsov,
    Dry_cargo_ship_Ivanov,
    Tanker_Elnya_160,
)
from dcs.vehicles import (
    AirDefence,
    Armor,
    Infantry,
    Unarmed,
)

Ukraine_2010 = {
    "country": "Ukraine",
    "side": "blue",
    "units": [
        Su_25,
        Su_25T,
        Su_24M,
        Su_27,
        MiG_29S,
        L_39ZA,

        IL_76MD,
        IL_78M,
        An_26B,
        An_30M,
        Yak_40,
        A_50,

        Mi_8MT,
        Mi_24V,

        AirDefence.SAM_SA_3_S_125_LN_5P73,
        AirDefence.SAM_SA_11_Buk_LN_9A310M1,
        AirDefence.SAM_SA_10_S_300PS_LN_5P85C,

        Armor.APC_M1043_HMMWV_Armament,
        Armor.IFV_BMP_3,
        Armor.IFV_BMP_2,
        Armor.APC_BTR_80,
        Armor.MBT_T_80U,
        Armor.MBT_T_72B,

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,
        Infantry.Soldier_AK,
        CV_1143_5_Admiral_Kuznetsov,
        Bulk_cargo_ship_Yakushev,
        Dry_cargo_ship_Ivanov,
        Tanker_Elnya_160,
    ],
    "shorad":[
        AirDefence.SAM_SA_19_Tunguska_2S6,
        AirDefence.SAM_SA_13_Strela_10M3_9A35M3,
        AirDefence.AAA_ZU_23_on_Ural_375
    ], "boat":[
        "GrishaGroupGenerator"
    ]
}