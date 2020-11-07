import json
import logging
import os
import threading
import time
import typing

from game import db

DEBRIEFING_LOG_EXTENSION = "log"

class DebriefingDeadUnitInfo:
    country_id = -1
    player_unit = False
    type = None

    def __init__(self, country_id, player_unit , type):
        self.country_id = country_id
        self.player_unit = player_unit
        self.type = type

    def __repr__(self):
        return str(self.country_id) + " " + str(self.player_unit) + " " + str(self.type)

class Debriefing:
    def __init__(self, state_data, game):
        self.state_data = state_data
        self.killed_aircrafts = state_data["killed_aircrafts"]
        self.killed_ground_units = state_data["killed_ground_units"]
        self.weapons_fired = state_data["weapons_fired"]
        self.mission_ended = state_data["mission_ended"]
        self.destroyed_units = state_data["destroyed_objects_positions"]

        self.__destroyed_units = []
        logging.info("--------------------------------")
        logging.info("Starting Debriefing preprocessing")
        logging.info("--------------------------------")
        logging.info(self.base_capture_events)
        logging.info(self.killed_aircrafts)
        logging.info(self.killed_ground_units)
        logging.info(self.weapons_fired)
        logging.info(self.mission_ended)
        logging.info(self.destroyed_units)
        logging.info("--------------------------------")

        self.player_country_id = db.country_id_from_name(game.player_country)
        self.enemy_country_id = db.country_id_from_name(game.enemy_country)

        self.dead_aircraft = []
        self.dead_units = []
        self.dead_aaa_groups = []
        self.dead_buildings = []

        for aircraft in self.killed_aircrafts:
            try:
                country = int(aircraft.split("|")[1])
                type = db.unit_type_from_name(aircraft.split("|")[4])
                player_unit = (country == self.player_country_id)
                aircraft = DebriefingDeadUnitInfo(country, player_unit, type)
                if type is not None:
                    self.dead_aircraft.append(aircraft)
            except Exception as e:
                logging.error(e)

        for unit in self.killed_ground_units:
            try:
                country = int(unit.split("|")[1])
                type = db.unit_type_from_name(unit.split("|")[4])
                player_unit = (country == self.player_country_id)
                unit = DebriefingDeadUnitInfo(country, player_unit, type)
                if type is not None:
                    self.dead_units.append(unit)
            except Exception as e:
                logging.error(e)

        for unit in self.killed_ground_units:
            for cp in game.theater.controlpoints:

                logging.info(cp.name)
                logging.info(cp.captured)

                if cp.captured:
                    country = self.player_country_id
                else:
                    country = self.enemy_country_id
                player_unit = (country == self.player_country_id)

                for i, ground_object in enumerate(cp.ground_objects):
                    logging.info(unit)
                    logging.info(ground_object.group_name)
                    if ground_object.is_same_group(unit):
                        unit = DebriefingDeadUnitInfo(country, player_unit, ground_object.dcs_identifier)
                        self.dead_buildings.append(unit)
                    elif ground_object.dcs_identifier in ["AA", "CARRIER", "LHA"]:
                        for g in ground_object.groups:
                            for u in g.units:
                                if u.name == unit:
                                    unit = DebriefingDeadUnitInfo(country, player_unit, db.unit_type_from_name(u.type))
                                    self.dead_units.append(unit)

        self.player_dead_aircraft = [a for a in self.dead_aircraft if a.country_id == self.player_country_id]
        self.enemy_dead_aircraft = [a for a in self.dead_aircraft if a.country_id == self.enemy_country_id]
        self.player_dead_units = [a for a in self.dead_units if a.country_id == self.player_country_id]
        self.enemy_dead_units = [a for a in self.dead_units if a.country_id == self.enemy_country_id]
        self.player_dead_buildings = [a for a in self.dead_buildings if a.country_id == self.player_country_id]
        self.enemy_dead_buildings = [a for a in self.dead_buildings if a.country_id == self.enemy_country_id]

        logging.info(self.player_dead_aircraft)
        logging.info(self.enemy_dead_aircraft)
        logging.info(self.player_dead_units)
        logging.info(self.enemy_dead_units)

        self.player_dead_aircraft_dict = {}
        for a in self.player_dead_aircraft:
            if a.type in self.player_dead_aircraft_dict.keys():
                self.player_dead_aircraft_dict[a.type] = self.player_dead_aircraft_dict[a.type] + 1
            else:
                self.player_dead_aircraft_dict[a.type] = 1

        self.enemy_dead_aircraft_dict = {}
        for a in self.enemy_dead_aircraft:
            if a.type in self.enemy_dead_aircraft_dict.keys():
                self.enemy_dead_aircraft_dict[a.type] = self.enemy_dead_aircraft_dict[a.type] + 1
            else:
                self.enemy_dead_aircraft_dict[a.type] = 1

        self.player_dead_units_dict = {}
        for a in self.player_dead_units:
            if a.type in self.player_dead_units_dict.keys():
                self.player_dead_units_dict[a.type] = self.player_dead_units_dict[a.type] + 1
            else:
                self.player_dead_units_dict[a.type] = 1

        self.enemy_dead_units_dict = {}
        for a in self.enemy_dead_units:
            if a.type in self.enemy_dead_units_dict.keys():
                self.enemy_dead_units_dict[a.type] = self.enemy_dead_units_dict[a.type] + 1
            else:
                self.enemy_dead_units_dict[a.type] = 1

        self.player_dead_buildings_dict = {}
        for a in self.player_dead_buildings:
            if a.type in self.player_dead_buildings_dict.keys():
                self.player_dead_buildings_dict[a.type] = self.player_dead_buildings_dict[a.type] + 1
            else:
                self.player_dead_buildings_dict[a.type] = 1

        self.enemy_dead_buildings_dict = {}
        for a in self.enemy_dead_buildings:
            if a.type in self.enemy_dead_buildings_dict.keys():
                self.enemy_dead_buildings_dict[a.type] = self.enemy_dead_buildings_dict[a.type] + 1
            else:
                self.enemy_dead_buildings_dict[a.type] = 1

        logging.info("--------------------------------")
        logging.info("Debriefing pre process results :")
        logging.info("--------------------------------")
        logging.info(self.player_dead_aircraft_dict)
        logging.info(self.enemy_dead_aircraft_dict)
        logging.info(self.player_dead_units_dict)
        logging.info(self.enemy_dead_units_dict)
        logging.info(self.player_dead_buildings_dict)
        logging.info(self.enemy_dead_buildings_dict)

    @property
    def base_capture_events(self):
        """Keeps only the last instance of a base capture event for each base ID"""
        reversed_captures = [i for i in self.state_data["base_capture_events"][::-1]]
        last_base_cap_indexes = []
        for idx, base in enumerate(i.split("||")[0] for i in reversed_captures):
            if base in [x[1] for x in last_base_cap_indexes]:
                continue
            else:
                last_base_cap_indexes.append((idx, base))
        return [reversed_captures[idx[0]] for idx in last_base_cap_indexes]        


class PollDebriefingFileThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  callback: typing.Callable, game):
        super(PollDebriefingFileThread, self).__init__()
        self._stop_event = threading.Event()
        self.callback = callback
        self.game = game

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        if os.path.isfile("state.json"):
            last_modified = os.path.getmtime("state.json")
        else:
            last_modified = 0
        while not self.stopped():
            if os.path.isfile("state.json") and os.path.getmtime("state.json") > last_modified:
                with open("state.json", "r") as json_file:
                    json_data = json.load(json_file)
                    debriefing = Debriefing(json_data, self.game)
                    self.callback(debriefing)
                break
            time.sleep(5)


def wait_for_debriefing(callback: typing.Callable, game)->PollDebriefingFileThread:
    thread = PollDebriefingFileThread(callback, game)
    thread.start()
    return thread

