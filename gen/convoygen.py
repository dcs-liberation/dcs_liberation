from __future__ import annotations

import itertools
from typing import Dict, TYPE_CHECKING, Type

from dcs import Mission
from dcs.mapping import Point
from dcs.point import PointAction
from dcs.unit import Vehicle
from dcs.unitgroup import VehicleGroup
from dcs.unittype import VehicleType

from game.transfers import Convoy
from game.unitmap import UnitMap
from game.utils import kph

if TYPE_CHECKING:
    from game import Game


class ConvoyGenerator:
    def __init__(self, mission: Mission, game: Game, unit_map: UnitMap) -> None:
        self.mission = mission
        self.game = game
        self.unit_map = unit_map
        self.count = itertools.count()

    def generate(self) -> None:
        # Reset the count to make generation deterministic.
        for convoy in self.game.transfers.convoys:
            self.generate_convoy(convoy)

    def generate_convoy(self, convoy: Convoy) -> VehicleGroup:
        group = self._create_mixed_unit_group(
            convoy.name,
            convoy.route_start,
            convoy.units,
            convoy.player_owned,
        )
        group.add_waypoint(
            convoy.route_end,
            speed=kph(40).kph,
            move_formation=PointAction.OnRoad,
        )
        self.make_drivable(group)
        self.unit_map.add_convoy_units(group, convoy)
        return group

    def _create_mixed_unit_group(
        self,
        name: str,
        position: Point,
        units: Dict[Type[VehicleType], int],
        for_player: bool,
    ) -> VehicleGroup:
        country = self.mission.country(
            self.game.player_country if for_player else self.game.enemy_country
        )

        unit_types = list(units.items())
        main_unit_type, main_unit_count = unit_types[0]

        group = self.mission.vehicle_group(
            country,
            name,
            main_unit_type,
            position=position,
            group_size=main_unit_count,
            move_formation=PointAction.OnRoad,
        )

        unit_name_counter = itertools.count(main_unit_count + 1)
        # pydcs spreads units out by 20 in the Y axis by default. Pick up where it left
        # off.
        y = itertools.count(position.y + main_unit_count * 20, 20)
        for unit_type, count in unit_types[1:]:
            for i in range(count):
                v = self.mission.vehicle(
                    f"{name} Unit #{next(unit_name_counter)}", unit_type
                )
                v.position.x = position.x
                v.position.y = next(y)
                v.heading = 0
                group.add_unit(v)

        return group

    @staticmethod
    def make_drivable(group: VehicleGroup) -> None:
        for v in group.units:
            if isinstance(v, Vehicle):
                v.player_can_drive = True
