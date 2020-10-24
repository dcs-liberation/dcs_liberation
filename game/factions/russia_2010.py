from dcs.helicopters import (
    Ka_50,
    Mi_24V,
    Mi_28N,
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
    MiG_31,
    Su_24M,
    Su_25,
    Su_25T,
    Su_27,
    Su_30,
    Su_33,
    Su_34,
    Tu_160,
    Tu_22M3,
    Tu_95MS,
    Yak_40,
)
from dcs.ships import (
    Bulk_cargo_ship_Yakushev,
    CV_1143_5_Admiral_Kuznetsov,
    Dry_cargo_ship_Ivanov,
    FF_1135M_Rezky,
    FSG_1241_1MP_Molniya,
    Tanker_Elnya_160,
)
from dcs.vehicles import (
    AirDefence,
    Armor,
    Artillery,
    Infantry,
    Unarmed,
)

Russia_2010 = {
    "country": "Russia",
    "side": "red",
    "units": [

        Su_27,
        Su_30,
        Su_33,
        MiG_29S,
        MiG_31,

        Su_25,
        Su_25T,
        Su_34,
        Su_24M,
        L_39ZA,

        Tu_160,
        Tu_22M3,
        Tu_95MS,

        IL_76MD,
        IL_78M,
        An_26B,
        An_30M,
        Yak_40,
        A_50,

        Ka_50,
        Mi_8MT,
        Mi_24V,
        Mi_28N,

        AirDefence.SAM_SA_19_Tunguska_2S6,
        AirDefence.SAM_SA_11_Buk_LN_9A310M1,
        AirDefence.SAM_SA_10_S_300PS_LN_5P85C,

        Armor.APC_BTR_80,
        Armor.MBT_T_90,
        Armor.MBT_T_80U,
        Armor.MBT_T_72B,
        Armor.IFV_BMP_1,
        Armor.IFV_BMP_2,
        Armor.IFV_BMP_3,

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
        AirDefence.SAM_SA_19_Tunguska_2S6,
        AirDefence.SAM_SA_13_Strela_10M3_9A35M3
    ], "aircraft_carrier": [
        CV_1143_5_Admiral_Kuznetsov,
    ], "carrier_names": [
        "Admiral Kuznetov"
    ], "destroyer": [
        FF_1135M_Rezky,
    ], "cruiser": [
        FSG_1241_1MP_Molniya,
    ], "boat": [
        "RussianNavyGroupGenerator", "KiloSubGroupGenerator"
    ]
}
