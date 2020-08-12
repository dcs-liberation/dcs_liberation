from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

UnitedKingdom_1990 = {
    "country": "UK",
    "side": "blue",
    "units":[
        AV8BNA, # Standing as BAE Harrier 2
        Tornado_GR4,
        F_4E,

        KC_135,
        KC130,
        C_130,
        E_3A,

        SA342M,
        AH_64A,

        Armor.MBT_Challenger_II,
        Armor.IFV_MCV_80,
        Armor.APC_M1043_HMMWV_Armament,
        Armor.ATGM_M1045_HMMWV_TOW,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.Rapier_FSA_Launcher,
        AirDefence.SAM_Avenger_M1097, # Standing as Starstreak

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ], "shorad":[
        AirDefence.SAM_Avenger_M1097,
    ], "helicopter_carrier": [
        LHA_1_Tarawa,
    ], "destroyer": [
        Oliver_Hazzard_Perry_class,
    ], "cruiser": [
        Ticonderoga_class,
    ], "lhanames": [
        "HMS Invincible",
        "HMS Illustrious",
        "HMS Ark Royal",
    ], "boat":[
        "ArleighBurkeGroupGenerator", "OliverHazardPerryGroupGenerator"
    ], "has_jtac": True
}