from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

India_2010 = {
    "country": "India",
    "side": "blue",
    "units": [
        Mirage_2000_5,
        M_2000C,
        MiG_27K,
        MiG_21Bis,
        MiG_29S,
        Su_30,

        KC_135,
        KC130,
        C_130,
        E_3A,

        AH_64A,
        Mi_8MT,

        Armor.MBT_T_90,
        Armor.MBT_T_72B,
        Armor.IFV_BMP_2,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,

        AirDefence.SAM_SA_6_Kub_LN_2P25,
        AirDefence.SAM_SA_3_S_125_LN_5P73,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ],
    "shorad":[
        AirDefence.SAM_SA_8_Osa_9A33,
        AirDefence.AAA_ZU_23_Emplacement,
        AirDefence.SPAAA_ZSU_23_4_Shilka,
        AirDefence.SAM_SA_13_Strela_10M3_9A35M3,
        AirDefence.SAM_SA_8_Osa_9A33,
        AirDefence.SAM_SA_19_Tunguska_2S6
    ], "aircraft_carrier": [
        CV_1143_5_Admiral_Kuznetsov,
    ], "destroyer": [
        FSG_1241_1MP_Molniya,
    ], "carrier_names": [
        "INS Vikramaditya"
    ], "boat":[
        "ArleighBurkeGroupGenerator", "OliverHazardPerryGroupGenerator", "MolniyaGroupGenerator"
    ]
}