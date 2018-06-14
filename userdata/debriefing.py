import typing
import threading
import time
import os

from dcs.lua import parse
from dcs.mission import Mission

from dcs.unitgroup import FlyingGroup
from dcs.unit import Vehicle, VehicleType
from dcs.vehicles import vehicle_map
from dcs.unit import UnitType

from game import db

DEBRIEFING_LOG_EXTENSION = "log"


class Debriefing:
    def __init__(self, alive_units):
        self.destroyed_units = {}  # type: typing.Dict[str, typing.Dict[str, int]]
        self.alive_units = alive_units  # type: typing.Dict[str, typing.Dict[str, int]]

    @classmethod
    def parse(cls, path: str):
        with open(path, "r") as f:
            table_string = f.read()
            table = parse.loads(table_string)
            units = table.get("debriefing", {}).get("world_state", {})
            alive_units = {}

            for unit in units.values():
                unit_type = unit["type"]  # type: str
                country_id = int(unit["country"])

                if type(unit_type) == str:
                    country_dict = alive_units.get(country_id, {})
                    country_dict[unit_type] = country_dict.get(unit_type, 0) + 1
                    alive_units[country_id] = country_dict

        return Debriefing(alive_units)

    def calculate_destroyed_units(self, mission: Mission, player_name: str, enemy_name: str):
        def count_groups(groups: typing.List[UnitType]) -> typing.Dict[UnitType, int]:
            result = {}
            for group in groups:
                for unit in group.units:
                    unit_type = None
                    if isinstance(unit, Vehicle):
                        unit_type = vehicle_map[unit.type]
                    else:
                        unit_type = unit.unit_type

                    result[unit_type] = result.get(unit_type, 0) + 1

            return result

        def calculate_losses(all_units: typing.Dict[UnitType, int], alive_units: typing.Dict[str, int]) -> typing.Dict[UnitType, int]:
            result = {}
            for t, count in all_units.items():
                result[t] = max(count - alive_units.get(db.unit_type_name(t), 0), 0)
            return result

        player = mission.country(player_name)
        enemy = mission.country(enemy_name)
        
        player_units = count_groups(player.plane_group + player.vehicle_group)
        enemy_units = count_groups(enemy.plane_group + enemy.vehicle_group)

        self.destroyed_units = {
            player.name: calculate_losses(player_units, self.alive_units.get(player.id, {})),
            enemy.name: calculate_losses(enemy_units, self.alive_units.get(enemy.id, {})),
        }

def debriefing_directory_location() -> str:
    return "build/debriefing"


def _logfiles_snapshot() -> typing.Dict[str, float]:
    result = {}
    for file in os.listdir(debriefing_directory_location()):
        fullpath = os.path.join(debriefing_directory_location(), file)
        result[file] = os.path.getmtime(fullpath)

    return result


def _poll_new_debriefing_log(snapshot: typing.Dict[str, float], callback: typing.Callable):
    should_run = True
    while should_run:
        for file, timestamp in _logfiles_snapshot().items():
            if file not in snapshot or timestamp != snapshot[file]:
                callback(Debriefing.parse(os.path.join(debriefing_directory_location(), file)))
                should_run = False
                break

        time.sleep(1)


def wait_for_debriefing(callback: typing.Callable):
    threading.Thread(target=_poll_new_debriefing_log, args=(_logfiles_snapshot(), callback)).start()

