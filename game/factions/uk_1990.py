from dcs.helicopters import (
    AH_64A,
    SA342M,
)
from dcs.planes import (
    AV8BNA,
    C_130,
    E_3A,
    F_4E,
    KC130,
    KC_135,
    Tornado_GR4,
)
from dcs.ships import (
    Armed_speedboat,
    CVN_74_John_C__Stennis,
    LHA_1_Tarawa,
    Oliver_Hazzard_Perry_class,
    Ticonderoga_class,
)
from dcs.vehicles import (
    AirDefence,
    Armor,
    Infantry,
    Unarmed,
)

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
    ], "helicopter_carrier_names": [
        "HMS Invincible",
        "HMS Illustrious",
        "HMS Ark Royal",
    ], "boat":[
        "ArleighBurkeGroupGenerator", "OliverHazardPerryGroupGenerator"
    ], "has_jtac": True
}