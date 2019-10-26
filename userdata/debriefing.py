import json
import logging
import os
import re
import threading
import time
import typing

from dcs.lua import parse
from dcs.mission import Mission
from dcs.unit import UnitType

from game import db
from .persistency import base_path

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
        self.base_capture_events = state_data["base_capture_events"]
        self.killed_aircrafts = state_data["killed_aircrafts"]
        self.killed_ground_units = state_data["killed_ground_units"]
        self.weapons_fired = state_data["weapons_fired"]
        self.mission_ended = state_data["mission_ended"]

        print(self.base_capture_events)
        print(self.killed_aircrafts)
        print(self.killed_ground_units)
        print(self.weapons_fired)
        print(self.mission_ended)

        self.player_country_id = db.country_id_from_name(game.player_country)
        self.enemy_country_id = db.country_id_from_name(game.enemy_country)

        self.dead_aircraft = []
        self.dead_units = []

        for aircraft in self.killed_aircrafts:
            try:
                country = int(aircraft.split("|")[1])
                type = db.unit_type_from_name(aircraft.split("|")[4])
                player_unit = (country == self.player_country_id)
                aircraft = DebriefingDeadUnitInfo(country, player_unit, type)
                if type is not None:
                    self.dead_aircraft.append(aircraft)
            except Exception as e:
                print(e)

        for unit in self.killed_ground_units:
            try:
                country = int(unit.split("|")[1])
                type = db.unit_type_from_name(unit.split("|")[4])
                player_unit = (country == self.player_country_id)
                unit = DebriefingDeadUnitInfo(country, player_unit, type)
                if type is not None:
                    self.dead_units.append(unit)
            except Exception as e:
                print(e)

        self.player_dead_aircraft = [a for a in self.dead_aircraft if a.country_id == self.player_country_id]
        self.enemy_dead_aircraft = [a for a in self.dead_aircraft if a.country_id == self.enemy_country_id]
        self.player_dead_units = [a for a in self.dead_units if a.country_id == self.player_country_id]
        self.enemy_dead_units = [a for a in self.dead_units if a.country_id == self.enemy_country_id]

        print(self.player_dead_aircraft)
        print(self.enemy_dead_aircraft)
        print(self.player_dead_units)
        print(self.enemy_dead_units)

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

        print(self.player_dead_aircraft_dict)
        print(self.enemy_dead_aircraft_dict)
        print(self.player_dead_units_dict)
        print(self.enemy_dead_units_dict)


def _poll_new_debriefing_log(callback: typing.Callable, game):
    if os.path.isfile("state.json"):
        last_modified = os.path.getmtime("state.json")
    else:
        last_modified = 0
    while True:
        if os.path.isfile("state.json") and os.path.getmtime("state.json") > last_modified:
            with open("state.json", "r") as json_file:
                json_data = json.load(json_file) #Debriefing.parse(os.path.join(debriefing_directory_location(), file))
                debriefing = Debriefing(json_data, game)
                callback(debriefing)
            break
        time.sleep(5)

def wait_for_debriefing(callback: typing.Callable, game):
    threading.Thread(target=_poll_new_debriefing_log, args=[callback, game]).start()

