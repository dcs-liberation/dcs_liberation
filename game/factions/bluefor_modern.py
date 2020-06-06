from dcs.vehicles import *
from dcs.ships import *
from dcs.planes import *
from dcs.helicopters import *

BLUEFOR_MODERN = {
    "country": "USA",
    "side": "blue",
    "units": [

        F_15C,
        F_14B,
        FA_18C_hornet,
        F_16C_50,
        JF_17,
        M_2000C,
        F_5E_3,
        Su_27,

        Su_25T,
        A_10A,
        A_10C,
        AV8BNA,
        AJS37,

        KC_135,
        KC130,
        C_130,
        E_3A,

        UH_1H,
        AH_64D,
        Ka_50,

        Armor.MBT_M1A2_Abrams,
        Armor.MBT_Leopard_2,
        Armor.ATGM_M1134_Stryker,
        Armor.IFV_M2A2_Bradley,
        Armor.IFV_Marder,
        Armor.APC_M1043_HMMWV_Armament,

        Artillery.MLRS_M270,
        Artillery.SPH_M109_Paladin,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.SAM_Hawk_PCP,
        AirDefence.SAM_Patriot_EPP_III,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ], "shorad": [
        AirDefence.SAM_Avenger_M1097,
    ], "aircraft_carrier": [
        CVN_74_John_C__Stennis,
    ], "helicopter_carrier": [
        LHA_1_Tarawa,
    ], "destroyer": [
        Oliver_Hazzard_Perry_class,
        USS_Arleigh_Burke_IIa,
    ], "cruiser": [
        Ticonderoga_class,
    ], "carrier_names": [
        "CVN-71 Theodore Roosevelt",
        "CVN-72 Abraham Lincoln",
        "CVN-73 George Washington",
        "CVN-74 John C. Stennis",
    ], "lhanames": [
        "LHA-1 Tarawa",
        "LHA-2 Saipan",
        "LHA-3 Belleau Wood",
        "LHA-4 Nassau",
        "LHA-5 Peleliu"
    ]
}
