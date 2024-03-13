from typing import Optional, Type

from dcs.helicopters import helicopter_map
from dcs.planes import plane_map
from dcs.ships import ship_map
from dcs.unittype import UnitType
from dcs.vehicles import vehicle_map
from dcs.statics import fortification_map, groundobject_map, warehouse_map, cargo_map


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
        # Try statics
        return static_type_from_name(name)


def static_type_from_name(name: str) -> Optional[Type[UnitType]]:
    if name in fortification_map:
        return fortification_map[name]
    elif name in groundobject_map:
        return groundobject_map[name]
    elif name in warehouse_map:
        return warehouse_map[name]
    if name in cargo_map:
        return cargo_map[name]
    else:
        return None
