import logging

from dcs.point import MovingPoint
from dcs.task import (
    Bombing,
    BombingRunway,
    OptFormation,
    WeaponType as DcsWeaponType,
)

from game.data.weapons import WeaponType
from game.theater import Airfield
from .pydcswaypointbuilder import PydcsWaypointBuilder


class OcaRunwayIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        target = self.package.target
        if not isinstance(target, Airfield):
            logging.error(
                "Unexpected target type for runway bombing mission: %s",
                target.__class__.__name__,
            )
            return

        # The BombingRunway task in DCS does not use LGBs, which necessitates special handling
        # by using the Bombing task instead. See https://github.com/dcs-liberation/dcs_liberation/issues/894
        # for more details.
        # The LGB work around assumes the Airfield position in DCS is on a runway, which seems
        # to be the case for most if not all airfields.
        if self.flight.loadout.has_weapon_of_type(WeaponType.LGB):
            waypoint.tasks.append(
                Bombing(
                    position=target.position,
                    group_attack=True,
                    weapon_type=DcsWeaponType.Guided,
                )
            )
        else:  # Use BombingRunway task for all other weapon types
            waypoint.tasks.append(
                BombingRunway(airport_id=target.airport.id, group_attack=True)
            )
        waypoint.tasks.append(OptFormation.trail_open())
