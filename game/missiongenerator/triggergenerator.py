from __future__ import annotations

from typing import TYPE_CHECKING

from dcs.action import ClearFlag, DoScript, MarkToAll, SetFlag
from dcs.condition import (
    AllOfCoalitionOutsideZone,
    FlagIsFalse,
    FlagIsTrue,
    PartOfCoalitionInZone,
    TimeAfter,
)
from dcs.mission import Mission
from dcs.task import Option
from dcs.translation import String
from dcs.triggers import Event, TriggerCondition, TriggerOnce
from dcs.unit import Skill

from game.theater import Airfield
from game.theater.controlpoint import Fob

if TYPE_CHECKING:
    from game.game import Game

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


class TriggerGenerator:
    capture_zone_types = (Fob, Airfield)
    capture_zone_flag = 600

    def __init__(self, mission: Mission, game: Game) -> None:
        self.mission = mission
        self.game = game

    def _set_allegiances(self, player_coalition: str, enemy_coalition: str) -> None:
        """
        Set airbase initial coalition
        """

        # Empty neutrals airports
        airfields = [
            cp for cp in self.game.theater.controlpoints if isinstance(cp, Airfield)
        ]
        airport_ids = {cp.airport.id for cp in airfields}
        for airport in self.mission.terrain.airport_list():
            if airport.id not in airport_ids:
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

        for airport in self.mission.terrain.airport_list():
            if airport.id not in airport_ids:
                airport.unlimited_fuel = True
                airport.unlimited_munitions = True
                airport.unlimited_aircrafts = True

        for airfield in airfields:
            cp_airport = self.mission.terrain.airport_by_id(airfield.airport.id)
            if cp_airport is None:
                raise RuntimeError(
                    f"Could not find {airfield.airport.name} in the mission"
                )
            cp_airport.set_coalition(
                airfield.captured and player_coalition or enemy_coalition
            )

    def _set_skill(self, player_coalition: str, enemy_coalition: str) -> None:
        """
        Set skill level for all aircraft in the mission
        """
        for coalition_name, coalition in self.mission.coalition.items():
            if coalition_name == player_coalition:
                skill_level = Skill(self.game.settings.player_skill)
            elif coalition_name == enemy_coalition:
                skill_level = Skill(self.game.settings.enemy_vehicle_skill)
            else:
                continue

            for country in coalition.countries.values():
                for vehicle_group in country.vehicle_group:
                    vehicle_group.set_skill(skill_level)

    def _gen_markers(self) -> None:
        """
        Generate markers on F10 map for each existing objective
        """
        if self.game.settings.generate_marks:
            mark_trigger = TriggerOnce(Event.NoEvent, "Marks generator")
            mark_trigger.add_condition(TimeAfter(1))
            v = 10
            for cp in self.game.theater.controlpoints:
                seen = set()
                for ground_object in cp.ground_objects:
                    if ground_object.obj_name in seen:
                        continue

                    seen.add(ground_object.obj_name)
                    for location in ground_object.mark_locations:
                        zone = self.mission.triggers.add_triggerzone(
                            location, radius=10, hidden=True, name="MARK"
                        )
                        if cp.captured:
                            name = ground_object.obj_name + " [ALLY]"
                        else:
                            name = ground_object.obj_name + " [ENEMY]"
                        mark_trigger.add_action(MarkToAll(v, zone.id, String(name)))
                        v += 1
            self.mission.triggerrules.triggers.append(mark_trigger)

    def _generate_capture_triggers(
        self, player_coalition: str, enemy_coalition: str
    ) -> None:
        """Creates a pair of triggers for each control point of `cls.capture_zone_types`.
        One for the initial capture of a control point, and one if it is recaptured.
        Directly appends to the global `base_capture_events` var declared by `dcs_libaration.lua`
        """
        for cp in self.game.theater.controlpoints:
            if isinstance(cp, self.capture_zone_types):
                if cp.captured:
                    attacking_coalition = enemy_coalition
                    attack_coalition_int = 1  # 1 is the Event int for Red
                    defending_coalition = player_coalition
                    defend_coalition_int = 2  # 2 is the Event int for Blue
                else:
                    attacking_coalition = player_coalition
                    attack_coalition_int = 2
                    defending_coalition = enemy_coalition
                    defend_coalition_int = 1

                trigger_zone = self.mission.triggers.add_triggerzone(
                    cp.position, radius=3000, hidden=False, name="CAPTURE"
                )
                flag = self.get_capture_zone_flag()
                capture_trigger = TriggerCondition(Event.NoEvent, "Capture Trigger")
                capture_trigger.add_condition(
                    AllOfCoalitionOutsideZone(
                        defending_coalition, trigger_zone.id, unit_type="GROUND"
                    )
                )
                capture_trigger.add_condition(
                    PartOfCoalitionInZone(
                        attacking_coalition, trigger_zone.id, unit_type="GROUND"
                    )
                )
                capture_trigger.add_condition(FlagIsFalse(flag=flag))
                script_string = String(
                    f'base_capture_events[#base_capture_events + 1] = "{cp.id}||{attack_coalition_int}||{cp.full_name}"'
                )
                capture_trigger.add_action(DoScript(script_string))
                capture_trigger.add_action(SetFlag(flag=flag))
                self.mission.triggerrules.triggers.append(capture_trigger)

                recapture_trigger = TriggerCondition(Event.NoEvent, "Capture Trigger")
                recapture_trigger.add_condition(
                    AllOfCoalitionOutsideZone(
                        attacking_coalition, trigger_zone.id, unit_type="GROUND"
                    )
                )
                recapture_trigger.add_condition(
                    PartOfCoalitionInZone(
                        defending_coalition, trigger_zone.id, unit_type="GROUND"
                    )
                )
                recapture_trigger.add_condition(FlagIsTrue(flag=flag))
                script_string = String(
                    f'base_capture_events[#base_capture_events + 1] = "{cp.id}||{defend_coalition_int}||{cp.full_name}"'
                )
                recapture_trigger.add_action(DoScript(script_string))
                recapture_trigger.add_action(ClearFlag(flag=flag))
                self.mission.triggerrules.triggers.append(recapture_trigger)

    def generate(self) -> None:
        player_coalition = "blue"
        enemy_coalition = "red"

        self._set_skill(player_coalition, enemy_coalition)
        self._set_allegiances(player_coalition, enemy_coalition)
        self._gen_markers()
        self._generate_capture_triggers(player_coalition, enemy_coalition)

    @classmethod
    def get_capture_zone_flag(cls) -> int:
        flag = cls.capture_zone_flag
        cls.capture_zone_flag += 1
        return flag
