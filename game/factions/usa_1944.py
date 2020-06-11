from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

from game.data.building_data import WW2_ALLIES_BUILDINGS

USA_1944 = {
    "country": "USA",
    "side": "blue",
    "units": [
        P_51D,
        P_51D_30_NA,
        P_47D_30,
        SpitfireLFMkIX,
        SpitfireLFMkIXCW,
        A_20G,

        Armor.MT_M4_Sherman,
        Armor.MT_M4A4_Sherman_Firefly,
        Armor.CT_Cromwell_IV,
        Armor.M30_Cargo_Carrier,
        Armor.APC_M2A1,
        Armor.CT_Cromwell_IV,
        Armor.ST_Centaur_IV,
        Armor.HIT_Churchill_VII,
        Armor.LAC_M8_Greyhound,
        Armor.TD_M10_GMC,
        Artillery.M12_GMC,

        Infantry.Infantry_M1_Garand,
        Infantry.Infantry_SMLE_No_4_Mk_1,

        LS_Samuel_Chase,
        LST_Mk_II,
        LCVP__Higgins_boat,

        Unarmed.CCKW_353,
        AirDefence.AAA_Bofors_40mm,
    ], "shorad":[
        AirDefence.AAA_Bofors_40mm,
    ], "objects": WW2_ALLIES_BUILDINGS
}