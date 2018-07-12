import typing
import re
import threading
import time
import os

from dcs.lua import parse
from dcs.mission import Mission

from dcs.unit import Vehicle, Ship
from dcs.vehicles import vehicle_map
from dcs.ships import ship_map
from dcs.planes import plane_map
from dcs.unit import UnitType

from game import db

from .persistency import base_path

DEBRIEFING_LOG_EXTENSION = "log"


def parse_mutliplayer_debriefing(contents: str):
    result = []

    for line in [x.strip() for x in contents.splitlines()]:
        key = None
        if line.startswith("initiator"):
            key = "initiator"
            result.append({})
        if line.startswith("type"):
            key = "type"
        else:
            continue
        value = re.findall(r"=\s*\"(.*?)\",", line)[0]
        result[-1][key] = value
    return {"debriefing": {"events": result}}


class Debriefing:
    def __init__(self, dead_units):
        self.destroyed_units = {}  # type: typing.Dict[str, typing.Dict[UnitType, int]]
        self.alive_units = {}  # type: typing.Dict[str, typing.Dict[UnitType, int]]

        self._dead_units = dead_units

    @classmethod
    def parse(cls, path: str):
        with open(path, "r") as f:
            table_string = f.read()
            try:
                table = parse.loads(table_string)
            except Exception as e:
                table = parse_mutliplayer_debriefing(table_string)

            events = table.get("debriefing", {}).get("events", {})
            dead_units = {}

            for event in events:
                if event["type"] != "crashed" and event["type"] != "dead":
                    continue

                try:
                    components = event["initiator"].split("|")
                    country_id, group_id, unit_type = int(components[0]), int(components[1]), db.unit_type_from_name(components[2])
                    if unit_type is None:
                        continue
                except Exception as e:
                    continue

                if country_id not in dead_units:
                    dead_units[country_id] = {}

                if unit_type not in dead_units[country_id]:
                    dead_units[country_id][unit_type] = 0

                dead_units[country_id][unit_type] += 1

        return Debriefing(dead_units)

    def calculate_units(self, mission: Mission, player_name: str, enemy_name: str):
        def count_groups(groups: typing.List[UnitType]) -> typing.Dict[UnitType, int]:
            result = {}
            for group in groups:
                for unit in group.units:
                    unit_type = None
                    if isinstance(unit, Vehicle):
                        unit_type = vehicle_map[unit.type]
                    elif isinstance(unit, Ship):
                        unit_type = ship_map[unit.type]
                    else:
                        unit_type = unit.unit_type

                    if unit_type in db.EXTRA_AA.values():
                        continue

                    result[unit_type] = result.get(unit_type, 0) + 1

            return result

        player = mission.country(player_name)
        enemy = mission.country(enemy_name)
        
        player_units = count_groups(player.plane_group + player.vehicle_group + player.ship_group)
        enemy_units = count_groups(enemy.plane_group + enemy.vehicle_group + enemy.ship_group)

        self.destroyed_units = {
            player.name: self._dead_units[player.id],
            enemy.name: self._dead_units[enemy.id],
        }

        self.alive_units = {
            player.name: {k: v - self._dead_units[player.id].get(k, 0) for k, v in player_units.items()},
            enemy.name: {k: v - self._dead_units[enemy.id].get(k, 0) for k, v in enemy_units.items()},
        }


def debriefing_directory_location() -> str:
    return os.path.join(base_path(), "liberation_debriefings")


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
                debriefing = Debriefing.parse(os.path.join(debriefing_directory_location(), file))
                callback(debriefing)
                should_run = False
                break

        time.sleep(3)


def wait_for_debriefing(callback: typing.Callable):
    if not os.path.exists(debriefing_directory_location()):
        os.mkdir(debriefing_directory_location())

    threading.Thread(target=_poll_new_debriefing_log, args=(_logfiles_snapshot(), callback)).start()

