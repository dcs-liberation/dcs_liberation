from dcs.helicopters import (
    SA342L,
    SA342M,
    UH_1H,
)
from dcs.planes import (
    C_130,
    E_3A,
    F_4E,
    KC130,
    KC_135,
    MiG_29G,
    Tornado_IDS,
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