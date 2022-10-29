import logging

from dcs.point import MovingPoint
from dcs.task import (
    ActivateBeaconCommand,
    ControlledTask,
    EngageTargets,
    OrbitAction,
    Tanker,
    Targets,
)

from game.ato import FlightType
from game.ato.flightplans.patrolling import PatrollingFlightPlan
from ._helper import create_stop_orbit_trigger
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RaceTrackBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        flight_plan = self.flight.flight_plan

        if not isinstance(flight_plan, PatrollingFlightPlan):
            flight_plan_type = flight_plan.__class__.__name__
            logging.error(
                f"Cannot create race track for {self.flight} because "
                f"{flight_plan_type} does not define a patrol."
            )
            return

        # NB: It's important that the engage task comes before the orbit task.
        # Though they're on the same waypoint, if the orbit task comes first it
        # is their first priority and they will not engage any targets because
        # they're fully focused on orbiting. If the STE task is first, they will
        # engage targets if available and orbit if they find nothing to shoot.
        if self.flight.flight_type is FlightType.REFUELING:
            self.configure_refueling_actions(waypoint)

        # TODO: Move the properties of this task into the flight plan?
        # CAP is the only current user of this so it's not a big deal, but might
        # be good to make this usable for things like BAI when we add that
        # later.
        cap_types = {FlightType.BARCAP, FlightType.TARCAP}
        if self.flight.flight_type in cap_types:
            engagement_distance = int(flight_plan.engagement_distance.meters)
            waypoint.tasks.append(
                EngageTargets(
                    max_distance=engagement_distance, targets=[Targets.All.Air]
                )
            )

        orbit = OrbitAction(
            altitude=waypoint.alt,
            pattern=OrbitAction.OrbitPattern.RaceTrack,
            speed=int(flight_plan.patrol_speed.kph),
        )

        racetrack = ControlledTask(orbit)
        self.set_waypoint_tot(waypoint, flight_plan.patrol_start_time)
        loiter_duration = flight_plan.patrol_end_time - self.elapsed_mission_time
        elapsed = int(loiter_duration.total_seconds())
        racetrack.stop_after_time(elapsed)
        # What follows is some code to cope with the broken 'stop after time' condition
        create_stop_orbit_trigger(racetrack, self.package, self.mission, elapsed)
        # end of hotfix
        waypoint.add_task(racetrack)

    def configure_refueling_actions(self, waypoint: MovingPoint) -> None:
        waypoint.add_task(Tanker())

        if self.flight.unit_type.dcs_unit_type.tacan:
            tanker_info = self.mission_data.tankers[-1]
            tacan = tanker_info.tacan
            tacan_callsign = {
                "Texaco": "TEX",
                "Arco": "ARC",
                "Shell": "SHL",
            }.get(tanker_info.callsign)

            waypoint.add_task(
                ActivateBeaconCommand(
                    tacan.number,
                    tacan.band.value,
                    tacan_callsign,
                    bearing=True,
                    unit_id=self.group.units[0].id,
                    aa=True,
                )
            )
