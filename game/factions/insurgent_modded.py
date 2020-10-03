from dcs.ships import (
    Bulk_cargo_ship_Yakushev,
    Dry_cargo_ship_Ivanov,
    Tanker_Elnya_160,
)
from dcs.vehicles import (
    AirDefence,
    Armor,
    Infantry,
    Unarmed,
)

from pydcs_extensions.frenchpack.frenchpack import (
    DIM__KAMIKAZE,
    DIM__TOYOTA_BLUE,
    DIM__TOYOTA_DESERT,
    DIM__TOYOTA_GREEN,
)

Insurgent_modded = {
    "country": "Insurgents",
    "side": "red",
    "units": [

        AirDefence.AAA_ZU_23_Insurgent_Closed,
        AirDefence.AAA_ZU_23_Insurgent_on_Ural_375,

        DIM__TOYOTA_BLUE,
        DIM__TOYOTA_DESERT,
        DIM__TOYOTA_GREEN,
        DIM__KAMIKAZE,
        Armor.ARV_BRDM_2,
        Armor.APC_Cobra,

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,
        Infantry.Soldier_AK,
        Infantry.Infantry_Soldier_Insurgents,

        Bulk_cargo_ship_Yakushev,
        Dry_cargo_ship_Ivanov,
        Tanker_Elnya_160
    ], "requirements": {
        "frenchpack V3.5": "https://forums.eagle.ru/showthread.php?t=279974",
    }
}