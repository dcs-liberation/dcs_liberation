from typing import List, Type

from dcs.point import MovingPoint
from dcs.task import (
    ControlledTask,
    EngageTargets,
    OptECMUsing,
    OptFormation,
    TargetType,
    Targets,
)

from game.ato import FlightType
from game.utils import nautical_miles
from .pydcswaypointbuilder import PydcsWaypointBuilder


class JoinPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if self.flight.flight_type == FlightType.ESCORT:
            self.configure_escort_tasks(
                waypoint,
                [
                    Targets.All.Air.Planes.Fighters,
                    Targets.All.Air.Planes.MultiroleFighters,
                ],
            )

            if self.flight.count < 4:
                waypoint.tasks.append(OptFormation.line_abreast_open())
            else:
                waypoint.tasks.append(OptFormation.spread_four_open())

        elif self.flight.flight_type == FlightType.SEAD_ESCORT:
            self.configure_escort_tasks(
                waypoint, [Targets.All.GroundUnits.AirDefence.AAA.SAMRelated]
            )

            # Let the AI use ECM to preemptively defend themselves.
            ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfDetectedLockByRadar)
            waypoint.tasks.append(ecm_option)

            if self.flight.count < 4:
                waypoint.tasks.append(OptFormation.line_abreast_open())
            else:
                waypoint.tasks.append(OptFormation.spread_four_open())

        elif not self.flight.flight_type.is_air_to_air:
            # Capture any non A/A type to avoid issues with SPJs that use the primary radar such as the F/A-18C.
            # You can bully them with STT to not be able to fire radar guided missiles at you,
            # so best choice is to not let them perform jamming for now.

            # Let the AI use ECM to defend themselves.
            ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfOnlyLockByRadar)
            waypoint.tasks.append(ecm_option)

            waypoint.tasks.append(OptFormation.finger_four_open())

    @staticmethod
    def configure_escort_tasks(
        waypoint: MovingPoint, target_types: List[Type[TargetType]]
    ) -> None:
        # Ideally we would use the escort mission type and escort task to have
        # the AI automatically but the AI only escorts AI flights while they are
        # traveling between waypoints. When an AI flight performs an attack
        # (such as attacking the mission target), AI escorts wander aimlessly
        # until the escorted group resumes its flight plan.
        #
        # As such, we instead use the Search Then Engage task, which is an
        # enroute task that causes the AI to follow their flight plan and engage
        # enemies of the set type within a certain distance. The downside to
        # this approach is that AI escorts are no longer related to the group
        # they are escorting, aside from the fact that they fly a similar flight
        # plan at the same time. With Escort, the escorts will follow the
        # escorted group out of the area. The strike element may or may not fly
        # directly over the target, and they may or may not require multiple
        # attack runs. For the escort flight we must just assume a flight plan
        # for the escort to fly. If the strike flight doesn't need to overfly
        # the target, the escorts are needlessly going in harms way. If the
        # strike flight needs multiple passes, the escorts may leave before the
        # escorted aircraft do.
        #
        # Another possible option would be to use Search Then Engage for join ->
        # ingress and egress -> split, but use a Search Then Engage in Zone task
        # for the target area that is set to end on a flag flip that occurs when
        # the strike aircraft finish their attack task.
        #
        # https://forums.eagle.ru/topic/251798-options-for-alternate-ai-escort-behavior
        waypoint.add_task(
            ControlledTask(
                EngageTargets(
                    # TODO: From doctrine.
                    max_distance=int(nautical_miles(30).meters),
                    targets=target_types,
                )
            )
        )

        # We could set this task to end at the split point. pydcs doesn't
        # currently support that task end condition though, and we don't really
        # need it.
