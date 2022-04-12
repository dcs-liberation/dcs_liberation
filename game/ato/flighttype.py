from __future__ import annotations

from enum import Enum

from game.sidc import AirEntity


class FlightType(Enum):
    """Enumeration of mission types.

    The value of each enumeration is the name that will be shown in the UI.

    These values are persisted to the save game as well since they are a part of
    each flight and thus a part of the ATO, so changing these values will break
    save compat.

    When adding new mission types to this list, you will also need to update:

    * flightplan.py: Add waypoint population in generate_flight_plan. Add a new flight
      plan type if necessary, though most are a subclass of StrikeFlightPlan.
    * aircraftgenerator.py: Add a configuration method and call it in setup_flight_group. This is
      responsible for configuring waypoint 0 actions like setting ROE, threat reaction,
      and mission abort parameters (winchester, bingo, etc).
    * Implementations of MissionTarget.mission_types: A mission type can only be planned
      against compatible targets. The mission_types method of each target class defines
      which missions may target it.
    * ai_flight_planner_db.py: Add the new mission type to aircraft_for_task that
      returns the list of compatible aircraft in order of preference.

    You may also need to update:

    * flightwaypointtype.py: Add a new waypoint type if necessary. Most mission types
      will need these, as aircraftgenerator.py uses the ingress point type to specialize AI
      tasks, and non-strike-like missions will need more specialized control.
    * ai_flight_planner.py: Use the new mission type in propose_missions so the AI will
      plan the new mission type.
    * FlightType.is_air_to_air and FlightType.is_air_to_ground: If the new mission type
      fits either of these categories, update those methods accordingly.
    """

    TARCAP = "TARCAP"
    BARCAP = "BARCAP"
    CAS = "CAS"
    INTERCEPTION = "Intercept"
    STRIKE = "Strike"
    ANTISHIP = "Anti-ship"
    SEAD = "SEAD"
    DEAD = "DEAD"
    ESCORT = "Escort"
    BAI = "BAI"
    SWEEP = "Fighter sweep"
    OCA_RUNWAY = "OCA/Runway"
    OCA_AIRCRAFT = "OCA/Aircraft"
    AEWC = "AEW&C"
    TRANSPORT = "Transport"
    SEAD_ESCORT = "SEAD Escort"
    REFUELING = "Refueling"
    FERRY = "Ferry"
    AIR_ASSAULT = "Air Assault"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_name(cls, name: str) -> FlightType:
        for entry in cls:
            if name == entry.value:
                return entry
        raise KeyError(f"No FlightType with name {name}")

    @property
    def is_air_to_air(self) -> bool:
        return self in {
            FlightType.TARCAP,
            FlightType.BARCAP,
            FlightType.INTERCEPTION,
            FlightType.ESCORT,
            FlightType.SWEEP,
        }

    @property
    def is_air_to_ground(self) -> bool:
        return self in {
            FlightType.CAS,
            FlightType.STRIKE,
            FlightType.ANTISHIP,
            FlightType.SEAD,
            FlightType.DEAD,
            FlightType.BAI,
            FlightType.OCA_RUNWAY,
            FlightType.OCA_AIRCRAFT,
            FlightType.SEAD_ESCORT,
            FlightType.AIR_ASSAULT,
        }

    @property
    def entity_type(self) -> AirEntity:
        return {
            FlightType.AEWC: AirEntity.AIRBORNE_EARLY_WARNING,
            FlightType.ANTISHIP: AirEntity.ANTISURFACE_WARFARE,
            FlightType.BAI: AirEntity.ATTACK_STRIKE,
            FlightType.BARCAP: AirEntity.FIGHTER,
            FlightType.CAS: AirEntity.ATTACK_STRIKE,
            FlightType.DEAD: AirEntity.ATTACK_STRIKE,
            FlightType.ESCORT: AirEntity.ESCORT,
            FlightType.FERRY: AirEntity.UNSPECIFIED,
            FlightType.INTERCEPTION: AirEntity.FIGHTER,
            FlightType.OCA_AIRCRAFT: AirEntity.ATTACK_STRIKE,
            FlightType.OCA_RUNWAY: AirEntity.ATTACK_STRIKE,
            FlightType.REFUELING: AirEntity.TANKER,
            FlightType.SEAD: AirEntity.SUPPRESSION_OF_ENEMY_AIR_DEFENCE,
            FlightType.SEAD_ESCORT: AirEntity.SUPPRESSION_OF_ENEMY_AIR_DEFENCE,
            FlightType.STRIKE: AirEntity.ATTACK_STRIKE,
            FlightType.SWEEP: AirEntity.FIGHTER,
            FlightType.TARCAP: AirEntity.FIGHTER,
            FlightType.TRANSPORT: AirEntity.UTILITY,
            FlightType.AIR_ASSAULT: AirEntity.ROTARY_WING,
        }.get(self, AirEntity.UNSPECIFIED)
