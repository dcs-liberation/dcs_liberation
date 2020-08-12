from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

USA_1965 = {
    "country": "USA",
    "side": "blue",
    "units": [

        F_5E_3,
        F_4E,

        KC_135,
        KC130,
        C_130,
        E_3A,

        B_52H,

        UH_1H,

        Armor.MBT_M60A3_Patton,
        Armor.APC_M113,
        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.SAM_Chaparral_M48,
        AirDefence.SAM_Hawk_PCP,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ],
    "shorad":[
        AirDefence.AAA_Vulcan_M163,
        AirDefence.SAM_Chaparral_M48
    ], "boat":[
    ]
}