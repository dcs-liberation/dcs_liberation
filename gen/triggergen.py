from __future__ import annotations

from dcs.action import MarkToAll
from dcs.condition import TimeAfter
from dcs.mission import Mission
from dcs.task import Option
from dcs.translation import String
from dcs.triggers import Event, TriggerOnce
from dcs.unit import Skill
from dcs.unitgroup import FlyingGroup
from .conflictgen import Conflict

PUSH_TRIGGER_SIZE = 3000
PUSH_TRIGGER_ACTIVATION_AGL = 25

REGROUP_ZONE_DISTANCE = 12000
REGROUP_ALT = 5000

TRIGGER_WAYPOINT_OFFSET = 2
TRIGGER_MIN_DISTANCE_FROM_START = 10000
# modified since we now have advanced SAM units
TRIGGER_RADIUS_MINIMUM = 3000000

TRIGGER_RADIUS_SMALL = 50000
TRIGGER_RADIUS_MEDIUM = 100000
TRIGGER_RADIUS_LARGE = 150000
TRIGGER_RADIUS_ALL_MAP = 3000000


class Silence(Option):
    Key = 7


class TriggersGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.mission = mission
        self.conflict = conflict
        self.game = game

    def _set_allegiances(self, player_coalition: str, enemy_coalition: str):
        """
        Set airbase initial coalition
        """

        # Empty neutrals airports
        cp_ids = [cp.id for cp in self.game.theater.controlpoints]
        for airport in self.mission.terrain.airport_list():
            if airport.id not in cp_ids:
                airport.unlimited_fuel = False
                airport.unlimited_munitions = False
                airport.unlimited_aircrafts = False
                airport.gasoline_init = 0
                airport.methanol_mixture_init = 0
                airport.diesel_init = 0
                airport.jet_init = 0
                airport.operating_level_air = 0
                airport.operating_level_equipment = 0
                airport.operating_level_fuel = 0

        for cp in self.game.theater.controlpoints:
            if cp.is_global:
                continue
            self.mission.terrain.airport_by_id(cp.at.id).set_coalition(cp.captured and player_coalition or enemy_coalition)

    def _set_skill(self, player_coalition: str, enemy_coalition: str):
        """
        Set skill level for all aircraft in the mission
        """
        for coalition_name, coalition in self.mission.coalition.items():
            if coalition_name == player_coalition:
                skill_level = self.game.settings.player_skill, self.game.settings.player_skill
            elif coalition_name == enemy_coalition:
                skill_level = self.game.settings.enemy_skill, self.game.settings.enemy_vehicle_skill
            else:
                continue

            for country in coalition.countries.values():
                flying_groups = country.plane_group + country.helicopter_group  # type: FlyingGroup
                for flying_group in flying_groups:
                    for plane_unit in flying_group.units:
                        if plane_unit.skill != Skill.Client and plane_unit.skill != Skill.Player:
                            plane_unit.skill = Skill(skill_level[0])

                for vehicle_group in country.vehicle_group:
                    vehicle_group.set_skill(Skill(skill_level[1]))

    def _gen_markers(self):
        """
        Generate markers on F10 map for each existing objective
        """
        if self.game.settings.generate_marks:
            mark_trigger = TriggerOnce(Event.NoEvent, "Marks generator")
            mark_trigger.add_condition(TimeAfter(1))
            v = 10
            for cp in self.game.theater.controlpoints:
                added = []
                for ground_object in cp.ground_objects:
                    if ground_object.obj_name not in added:
                        zone = self.mission.triggers.add_triggerzone(ground_object.position, radius=10, hidden=True, name="MARK")
                        if cp.captured:
                            name = ground_object.obj_name + " [ALLY]"
                        else:
                            name = ground_object.obj_name + " [ENEMY]"
                        mark_trigger.add_action(MarkToAll(v, zone.id, String(name)))
                        v = v + 1
                    added.append(ground_object.obj_name)
            self.mission.triggerrules.triggers.append(mark_trigger)

    def generate(self):
        player_coalition = "blue"
        enemy_coalition = "red"

        self.mission.coalition["blue"].bullseye = {"x": self.conflict.position.x,
                                                   "y": self.conflict.position.y}
        self.mission.coalition["red"].bullseye = {"x": self.conflict.position.x,
                                                  "y": self.conflict.position.y}

        self._set_skill(player_coalition, enemy_coalition)
        self._set_allegiances(player_coalition, enemy_coalition)
        self._gen_markers()

