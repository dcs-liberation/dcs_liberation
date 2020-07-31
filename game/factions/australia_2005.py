from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

AUSTRALIA_2005 = {
    "country": "Australia",
    "side": "blue",
    "units": [
        FA_18C_hornet,

        KC_135,
        KC130,
        C_130,
        E_3A,

        Armor.MBT_M1A2_Abrams,
        Armor.MBT_Leopard_1A3,
        Armor.APC_M113,
        Armor.IFV_LAV_25,

        UH_1H,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.SAM_Hawk_PCP,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ], "shorad": [
        AirDefence.Rapier_FSA_Launcher,
    ], "aircraft_carrier": [
    ], "helicopter_carrier": [
        LHA_1_Tarawa,
    ], "destroyer": [
        USS_Arleigh_Burke_IIa,
    ], "cruiser": [
        Ticonderoga_class,
    ], "carrier_names": [
    ], "lhanames": [
    ], "boat":[
        "ArleighBurkeGroupGenerator"
    ]
}
