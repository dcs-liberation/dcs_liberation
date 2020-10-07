from dcs.helicopters import (
    AH_64A,
    UH_1H,
)
from dcs.planes import (
    AV8BNA,
    A_10A,
    C_130,
    E_3A,
    FA_18C_hornet,
    F_14B,
    F_15C,
    F_15E,
    F_16C_50,
    KC130,
    KC_135,
)
from dcs.ships import (
    Armed_speedboat,
    CVN_74_John_C__Stennis,
    LHA_1_Tarawa,
    Oliver_Hazzard_Perry_class,
    Ticonderoga_class,
    USS_Arleigh_Burke_IIa,
)
from dcs.vehicles import (
    AirDefence,
    Armor,
    Infantry,
    Unarmed,
)

USA_1990 = {
    "country": "USA",
    "side": "blue",
    "units": [
        F_15C,
        F_15E,
        F_14B,
        FA_18C_hornet,
        F_16C_50,

        A_10A,
        AV8BNA,

        KC_135,
        KC130,
        C_130,
        E_3A,

        UH_1H,
        AH_64A,

        Armor.MBT_M1A2_Abrams,
        Armor.IFV_LAV_25,
        Armor.APC_M1043_HMMWV_Armament,
        Armor.ATGM_M1045_HMMWV_TOW,
        Armor.ATGM_M1134_Stryker,
        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.SAM_Hawk_PCP,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ], "shorad":[
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
        "CVN-72 Abraham Lincoln",
        "CVN-73 Georges Washington",
        "CVN-74 John C. Stennis",
    ], "lhanames": [
        "LHA-1 Tarawa",
        "LHA-2 Saipan",
        "LHA-3 Belleau Wood",
        "LHA-4 Nassau",
        "LHA-5 Peleliu"
    ], "boat":[
        "ArleighBurkeGroupGenerator", "OliverHazardPerryGroupGenerator"
    ], "has_jtac": True
}