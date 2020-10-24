from dcs.helicopters import (
    UH_1H,
)
from dcs.planes import (
    B_52H,
    C_130,
    E_3A,
    F_86F_Sabre,
    KC130,
    KC_135,
    P_51D,
)
from dcs.ships import (
    Armed_speedboat,
    CVN_74_John_C__Stennis,
    LHA_1_Tarawa,
)
from dcs.vehicles import (
    AirDefence,
    Armor,
    Infantry,
    Unarmed,
)

USA_1960 = {
    "country": "USA",
    "side": "blue",
    "units": [
        F_86F_Sabre,
        P_51D,

        B_52H,

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