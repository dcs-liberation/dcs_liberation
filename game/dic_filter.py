from game.db import PRICES
from typing import Dict, List, Type
from dcs.unittype import VehicleType
import logging


class dic_analyser:
    def get_all_vehicletype_from_dic(
        self, vehicle_list: Dict[Type[VehicleType], int], vehicle_type: list
    ) -> List[Type[VehicleType]]:
        vehicles: List[Type[VehicleType]] = []
        if not vehicle_list:
            return vehicles

        for unit, count in vehicle_list.items():
            if unit in vehicle_type:
                for _ in range(count):
                    vehicles.append(unit)
        return vehicles

    def get_costs_for_provided_vehicles(
        self, vehicle_dic: Dict[Type[VehicleType], int]
    ) -> int:
        total = 0
        if not vehicle_dic:
            return total

        for unit_type, count in vehicle_dic.items():
            try:
                total += PRICES[unit_type] * count
            except KeyError:
                logging.exception(f"No price found for {unit_type.id}")
        return total

    def get_dic_with_numbers_of_vehicles_from_list(
        self, vehicle_list: List[Type[VehicleType]]
    ) -> Dict[Type[VehicleType], int]:
        dic: Dict[Type[VehicleType], int] = {}
        if not vehicle_list:
            return dic
        for unit in vehicle_list:
            if unit in dic.keys():
                dic[unit] += 1
            else:
                dic.update({unit: 1})

        return dic
