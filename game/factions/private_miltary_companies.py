from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

from pydcs_extensions.mb339.mb339 import MB_339PAN

PMC_WESTERN_A = {
     "country": "USA",
     "side": "blue",
     "units": [
         C_101CC,

         UH_1H,
         Mi_8MT,
         OH_58D,
         SA342M,

         Armor.APC_M1043_HMMWV_Armament,
         Armor.IFV_MCV_80,

         Unarmed.Transport_M818,
         Infantry.Infantry_M4,
         Infantry.Soldier_M249,

         AirDefence.SAM_Avenger_M1097,

         Armed_speedboat,
    ], "shorad":[
        AirDefence.SAM_Avenger_M1097,
    ], "has_jtac": True
}

PMC_WESTERN_B = {
     "country": "USA",
     "side": "blue",
     "units": [
         MB_339PAN,
         C_101CC,

         UH_1H,
         Mi_8MT,
         OH_58D,
         SA342M,

         Armor.APC_M1043_HMMWV_Armament,
         Armor.IFV_MCV_80,

         Unarmed.Transport_M818,
         Infantry.Infantry_M4,
         Infantry.Soldier_M249,

         AirDefence.SAM_Avenger_M1097,

         Armed_speedboat,
    ], "shorad":[
        AirDefence.SAM_Avenger_M1097,
    ], "has_jtac": True,
    "requirements": {
        "MB-339A": "http://www.freccetricolorivirtuali.net/",
    }
}

PMC_RUSSIAN = {
     "country": "Russia",
     "side": "blue",
     "units": [
         L_39C,
         L_39ZA,

         Mi_8MT,
         Mi_24V,
         Ka_50,

         Armor.APC_Cobra,
         Armor.APC_BTR_80,
         Armor.ARV_BRDM_2,

         Unarmed.Transport_Ural_375,
         Infantry.Paratrooper_AKS,
         Infantry.Paratrooper_RPG_16,

         AirDefence.AAA_ZU_23_on_Ural_375,

         Armed_speedboat,
    ], "shorad":[
        AirDefence.AAA_ZU_23_on_Ural_375,
        AirDefence.AAA_ZU_23_Closed,
    ], "has_jtac": True
}

