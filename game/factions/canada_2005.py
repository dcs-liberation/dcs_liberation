from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

Canada_2005 = {
    "country": "Canada",
    "side": "blue",
    "units": [
        FA_18C_hornet,

        KC_135,
        KC130,
        C_130,
        E_3A,

        Armor.MBT_Leopard_1A3,
        Armor.MBT_Leopard_2,
        Armor.IFV_LAV_25,
        Armor.APC_M113,
        Armor.IFV_MCV_80,

        UH_1H,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.SAM_Avenger_M1097,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ], "shorad": [
        AirDefence.SAM_Avenger_M1097,
    ], "destroyer": [
        USS_Arleigh_Burke_IIa,
    ], "cruiser": [
        Ticonderoga_class,
    ], "boat":[
        "ArleighBurkeGroupGenerator"
    ], "has_jtac": True
}
