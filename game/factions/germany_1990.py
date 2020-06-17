from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

Germany_1990 = {
    "country": "Germany",
    "side": "blue",
    "units":[
        MiG_29G,
        Tornado_IDS,
        F_4E,

        KC_135,
        KC130,
        C_130,
        E_3A,

        UH_1H,
        SA342M,
        SA342L,

        Armor.TPz_Fuchs,
        Armor.MBT_Leopard_1A3,
        Armor.MBT_Leopard_2,
        Armor.IFV_Marder,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.SAM_Roland_ADS,
        AirDefence.SAM_Hawk_PCP,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ],
    "shorad":[
        AirDefence.SPAAA_Gepard,
        AirDefence.SAM_Roland_ADS,
    ], "boat":[
        "OliverHazardPerryGroupGenerator"
    ]
}