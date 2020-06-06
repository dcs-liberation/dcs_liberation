from dcs.vehicles import *
from dcs.ships import *
from dcs.planes import *
from dcs.helicopters import *

USA_1960 = {
    "country": "USA",
    "side": "blue",
    "units": [
        F_86F_Sabre,
        P_51D,

        KC_135,
        KC130,
        C_130,
        E_3A,

        UH_1H,

        Armor.MBT_M60A3_Patton,
        Armor.APC_M113,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.AAA_Vulcan_M163,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ],
    "shorad":[
        AirDefence.AAA_Vulcan_M163
    ]
}