from game.db import PRICES
from typing import Dict, List, Type
from dcs.unittype import VehicleType
from gen.ground_forces.ai_ground_planner_db import (
    TYPE_APC,
    TYPE_ARTILLERY,
    TYPE_ATGM,
    TYPE_IFV,
    TYPE_SHORAD,
    TYPE_TANKS,
)


class dic_analyser:
    def get_all_tanks_from_dic(vehicle_list: Dict[Type[VehicleType], int]) -> list:
        vehicles = []
        if not vehicle_list:
            return vehicles

        for unit, count in vehicle_list.items():
            if unit in TYPE_TANKS:
                for _ in range(count):
                    vehicles.append(unit)
        return vehicles

    def get_all_shorad_from_dic(vehicle_list: Dict[Type[VehicleType], int]) -> list:
        vehicles = []
        if not vehicle_list:
            return vehicles

        for unit, count in vehicle_list.items():
            if unit in TYPE_SHORAD:
                for _ in range(count):
                    vehicles.append(unit)
        return vehicles

    def get_all_ifv_from_dic(vehicle_list: Dict[Type[VehicleType], int]) -> list:
        vehicles = []
        if not vehicle_list:
            return vehicles

        for unit, count in vehicle_list.items():
            if unit in TYPE_IFV:
                for _ in range(count):
                    vehicles.append(unit)
        return vehicles

    def get_all_atgm_from_dic(vehicle_list: Dict[Type[VehicleType], int]) -> list:
        vehicles = []
        if not vehicle_list:
            return vehicles

        for unit, count in vehicle_list.items():
            if unit in TYPE_ATGM:
                for _ in range(count):
                    vehicles.append(unit)
        return vehicles

    def get_all_artillery_from_dic(vehicle_list: Dict[Type[VehicleType], int]) -> list:
        vehicles = []
        if not vehicle_list:
            return vehicles

        for unit, count in vehicle_list.items():
            if unit in TYPE_ARTILLERY:
                for _ in range(count):
                    vehicles.append(unit)
        return vehicles

    def get_all_apc_from_dic(vehicle_list: Dict[Type[VehicleType], int]) -> list:
        vehicles = []
        if not vehicle_list:
            return vehicles

        for unit, count in vehicle_list.items():
            if unit in TYPE_APC:
                for _ in range(count):
                    vehicles.append(unit)
        return vehicles

    def get_costs_for_provided_vehicles(vehicle_list: List[Type[VehicleType]]) -> int:
        totalcost: int = 0
        if not vehicle_list:
            return 0
        for vehicle in vehicle_list:
            totalcost += PRICES[vehicle]

        return totalcost
