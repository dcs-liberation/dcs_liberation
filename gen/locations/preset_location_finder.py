from pathlib import Path
from typing import List

from dcs import Mission, ships
from dcs.vehicles import MissilesSS

from gen.locations.preset_control_point_locations import PresetControlPointLocations
from gen.locations.preset_locations import PresetLocation


class PresetLocationFinder:

    @staticmethod
    def compute_possible_locations(terrain_name: str, cp_name: str) -> PresetControlPointLocations:
        """
        Extract the list of preset locations from miz data
        :param terrain_name: Terrain/Map name
        :param cp_name: Control Point / Airbase name
        :return:
        """

        miz_file = Path("./resources/mizdata/", terrain_name.lower(), cp_name + ".miz")

        offshore_locations: List[PresetLocation] = []
        ashore_locations: List[PresetLocation] = []
        powerplants_locations: List[PresetLocation] = []
        antiship_locations: List[PresetLocation] = []

        if miz_file.exists():
            m = Mission()
            m.load_file(miz_file.absolute())

            for vehicle_group in m.country("USA").vehicle_group:
                if len(vehicle_group.units) > 0:
                    ashore_locations.append(PresetLocation(vehicle_group.position,
                                                           vehicle_group.units[0].heading,
                                                           vehicle_group.name))

            for ship_group in m.country("USA").ship_group:
                if len(ship_group.units) > 0 and ship_group.units[0].type == ships.Oliver_Hazzard_Perry_class.id:
                    offshore_locations.append(PresetLocation(ship_group.position,
                                                             ship_group.units[0].heading,
                                                             ship_group.name))

            for static_group in m.country("USA").static_group:
                if len(static_group.units) > 0:
                    powerplants_locations.append(PresetLocation(static_group.position,
                                                                static_group.units[0].heading,
                                                                static_group.name))

            if m.country("Iran") is not None:
                for vehicle_group in m.country("Iran").vehicle_group:
                    if len(vehicle_group.units) > 0 and vehicle_group.units[0].type == MissilesSS.SS_N_2_Silkworm.id:
                        antiship_locations.append(PresetLocation(vehicle_group.position,
                                                                 vehicle_group.units[0].heading,
                                                                 vehicle_group.name))

        return PresetControlPointLocations(ashore_locations, offshore_locations,
                                           antiship_locations, powerplants_locations)
