from dcs.helicopters import (
    UH_1H,
)
from dcs.planes import (
    C_130,
    E_3A,
    FA_18C_hornet,
    KC130,
    KC_135,
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
    Infantry,
    Unarmed,
)

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
