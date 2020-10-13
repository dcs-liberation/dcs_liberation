from dcs.helicopters import (
    AH_64D,
    Ka_50,
    SA342L,
    SA342M,
    UH_1H,
)
from dcs.planes import (
    B_1B,
    B_52H,
    C_130,
    E_3A,
    FA_18C_hornet,
    F_15C,
    F_15E,
    F_16C_50,
    F_5E_3,
    KC130,
    KC_135,
    Su_27,
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
    Artillery,
    Infantry,
    Unarmed,
)

US_Aggressors = {
    "country": "USAF Aggressors",
    "side": "red",
    "units": [

        F_15C,
        F_15E,
        F_5E_3,
        FA_18C_hornet,
        F_16C_50,
        Su_27,

        B_1B,
        B_52H,

        KC_135,
        KC130,
        C_130,
        E_3A,

        UH_1H,
        AH_64D,
        Ka_50,
        SA342M,
        SA342L,

        Armor.MBT_M1A2_Abrams,
        Armor.MBT_Leopard_2,
        Armor.ATGM_M1134_Stryker,
        Armor.IFV_M2A2_Bradley,
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
    ], "boat":[
        "ArleighBurkeGroupGenerator", "OliverHazardPerryGroupGenerator"
    ]
}
