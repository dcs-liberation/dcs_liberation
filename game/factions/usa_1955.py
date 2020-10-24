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

USA_1955 = {
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

        Armor.MT_M4A4_Sherman_Firefly,
        Armor.MT_M4_Sherman,
        Armor.MBT_M60A3_Patton,
        Armor.APC_M2A1,
        Armor.M30_Cargo_Carrier,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,

        AirDefence.AAA_Bofors_40mm,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
    ]
}