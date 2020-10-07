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
    MiG_21Bis,
    MiG_23MLD,
    MiG_25PD,
    MiG_29A,
    Su_17M4,
    Su_24M,
    Su_25,
    Yak_40,
)
from dcs.ships import (
    Bulk_cargo_ship_Yakushev,
    CGN_1144_2_Pyotr_Velikiy,
    CV_1143_5_Admiral_Kuznetsov,
    Dry_cargo_ship_Ivanov,
    FF_1135M_Rezky,
    Tanker_Elnya_160,
)
from dcs.vehicles import AirDefence, Armor, Artillery, Infantry, Unarmed

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

        Artillery.SPH_2S9_Nona,
        Artillery.SPH_2S1_Gvozdika,

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
    "shorad": [
        AirDefence.AAA_ZU_23_Emplacement,
        AirDefence.SPAAA_ZSU_23_4_Shilka
    ], "aircraft_carrier": [
        CV_1143_5_Admiral_Kuznetsov,
    ], "destroyer": [
        FF_1135M_Rezky,
    ], "cruiser": [
        CGN_1144_2_Pyotr_Velikiy,
    ], "boat": [
        "RussianNavyGroupGenerator", "KiloSubGroupGenerator", "MolniyaGroupGenerator"
    ]
}