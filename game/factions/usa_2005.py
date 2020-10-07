from dcs.helicopters import (
    AH_64D,
    UH_1H,
)
from dcs.planes import (
    AV8BNA,
    A_10C,
    A_10C_2,
    C_130,
    E_3A,
    FA_18C_hornet,
    F_14B,
    F_15C,
    F_15E,
    F_16C_50,
    KC130,
    KC_135,
    MQ_9_Reaper,
)
from dcs.ships import (
    Armed_speedboat,
    CVN_74_John_C__Stennis,
    LHA_1_Tarawa,
    Ticonderoga_class,
    USS_Arleigh_Burke_IIa,
)
from dcs.vehicles import (
    AirDefence,
    Armor,
    Artillery,
    Infantry,
    Unarmed,
)

USA_2005 = {
    "country": "USA",
    "side": "blue",
    "units": [
        F_15C,
        F_15E,
        F_14B,
        FA_18C_hornet,
        F_16C_50,
        A_10C,
        A_10C_2,
        AV8BNA,
        MQ_9_Reaper,

        KC_135,
        KC130,
        C_130,
        E_3A,

        UH_1H,
        AH_64D,

        Armor.MBT_M1A2_Abrams,
        Armor.ATGM_M1134_Stryker,
        Armor.APC_M1126_Stryker_ICV,
        Armor.IFV_M2A2_Bradley,
        Armor.IFV_LAV_25,
        Armor.APC_M1043_HMMWV_Armament,
        Armor.ATGM_M1045_HMMWV_TOW,

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
    ], "boat":[
        "ArleighBurkeGroupGenerator"
    ], "has_jtac": True
}
