import logging

from dcs.point import MovingPoint
from dcs.task import AttackGroup, OptFormation, WeaponType

from game.theater import NavalControlPoint, TheaterGroundObject
from game.transfers import MultiGroupTransport
from .pydcswaypointbuilder import PydcsWaypointBuilder


class BaiIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        # TODO: Add common "UnitGroupTarget" base type.
        group_names = []
        target = self.package.target
        if isinstance(target, TheaterGroundObject):
            for group in target.groups:
                group_names.append(group.group_name)
        elif isinstance(target, MultiGroupTransport):
            group_names.append(target.name)
        elif isinstance(target, NavalControlPoint):
            carrier_name = target.get_carrier_group_name()
            if carrier_name:
                group_names.append(carrier_name)
        else:
            logging.error(
                "Unexpected target type for BAI mission: %s",
                target.__class__.__name__,
            )
            return

        for group_name in group_names:
            miz_group = self.mission.find_group(group_name)
            if miz_group is None:
                logging.error("Could not find group for BAI mission %s", group_name)
                continue

            task = AttackGroup(miz_group.id, weapon_type=WeaponType.Auto)
            waypoint.tasks.append(task)

        waypoint.tasks.append(OptFormation.trail_open())
