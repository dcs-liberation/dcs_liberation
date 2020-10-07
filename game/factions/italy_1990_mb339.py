from dcs.helicopters import (
    AH_1W,
    UH_1H,
)
from dcs.planes import (
    AV8BNA,
    C_130,
    E_3A,
    KC_135,
    S_3B_Tanker,
    Tornado_IDS,
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

from pydcs_extensions.mb339.mb339 import MB_339PAN

Italy_1990_MB339 = {
     "country": "Italy",
     "side": "blue",
     "units": [
         Tornado_IDS,
         AV8BNA,
         MB_339PAN,

         KC_135,
         S_3B_Tanker,
         C_130,
         E_3A,

         AH_1W,
         UH_1H,

         Armor.MBT_Leopard_1A3,  # OF-40 MBT
         Armor.APC_M113,

         Unarmed.Transport_M818,
         Infantry.Infantry_M4,

         AirDefence.SAM_Hawk_PCP,
         AirDefence.SAM_Avenger_M1097,

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
        "Giuseppe Garibaldi",
        "Cavour",
    ], "boat": [
        "OliverHazardPerryGroupGenerator"
    ], "requirements": {
        "MB-339A": "http://www.freccetricolorivirtuali.net/",
    }, "has_jtac": True
}
