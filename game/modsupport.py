from typing import Type

from dcs.helicopters import HelicopterType, helicopter_map
from dcs.planes import PlaneType, plane_map
from dcs.unittype import VehicleType
from dcs.vehicles import vehicle_map


def helicoptermod(helicopter: Type[HelicopterType]) -> Type[HelicopterType]:
    helicopter_map[helicopter.id] = helicopter
    return helicopter


def planemod(plane: Type[PlaneType]) -> Type[PlaneType]:
    plane_map[plane.id] = plane
    return plane


def vehiclemod(vehicle: Type[VehicleType]) -> Type[VehicleType]:
    vehicle_map[vehicle.id] = vehicle
    return vehicle
