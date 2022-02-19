from typing import Optional, Type

from dcs.helicopters import helicopter_map
from dcs.planes import plane_map
from dcs.ships import ship_map
from dcs.unittype import UnitType
from dcs.vehicles import vehicle_map


def unit_type_from_name(name: str) -> Optional[Type[UnitType]]:
    if name in vehicle_map:
        return vehicle_map[name]
    elif name in plane_map:
        return plane_map[name]
    elif name in ship_map:
        return ship_map[name]
    if name in helicopter_map:
        return helicopter_map[name]
    else:
        return None
