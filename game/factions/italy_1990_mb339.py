from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

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
    ], "lha_names": [
        "Giuseppe Garibaldi",
        "Cavour",
    ], "boat":[
        "OliverHazardPerryGroupGenerator"
    ]
}
