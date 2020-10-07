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

Insurgent = {
    "country": "Insurgents",
    "side": "red",
    "units": [

        AirDefence.AAA_ZU_23_Insurgent_Closed,
        AirDefence.AAA_ZU_23_Insurgent_on_Ural_375,

        Armor.APC_Cobra,
        Armor.APC_MTLB,
        Armor.ARV_BRDM_2,

        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,
        Infantry.Infantry_Soldier_Insurgents,
        Infantry.Soldier_RPG,

        Bulk_cargo_ship_Yakushev,
        Dry_cargo_ship_Ivanov,
        Tanker_Elnya_160
    ]
}