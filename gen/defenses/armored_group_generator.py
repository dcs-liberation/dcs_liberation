import random

from game import Game
from game.dcs.groundunittype import GroundUnitType
from game.theater.theatergroundobject import VehicleGroupGroundObject
from gen.sam.group_generator import VehicleGroupGenerator


class ArmoredGroupGenerator(VehicleGroupGenerator[VehicleGroupGroundObject]):
    def __init__(
        self,
        game: Game,
        ground_object: VehicleGroupGroundObject,
        unit_type: GroundUnitType,
    ) -> None:
        super().__init__(game, ground_object)
        self.unit_type = unit_type

    def generate(self) -> None:
        grid_x = random.randint(2, 3)
        grid_y = random.randint(1, 2)

        spacing = random.randint(30, 80)

        index = 0
        for i in range(grid_x):
            for j in range(grid_y):
                index = index + 1
                self.add_unit(
                    self.unit_type.dcs_unit_type,
                    "Armor#" + str(index),
                    self.position.x + spacing * i,
                    self.position.y + spacing * j,
                    self.heading,
                )


class FixedSizeArmorGroupGenerator(VehicleGroupGenerator[VehicleGroupGroundObject]):
    def __init__(
        self,
        game: Game,
        ground_object: VehicleGroupGroundObject,
        unit_type: GroundUnitType,
        size: int,
    ) -> None:
        super().__init__(game, ground_object)
        self.unit_type = unit_type
        self.size = size

    def generate(self) -> None:
        spacing = random.randint(20, 70)

        index = 0
        for i in range(self.size):
            index = index + 1
            self.add_unit(
                self.unit_type.dcs_unit_type,
                "Armor#" + str(index),
                self.position.x + spacing * i,
                self.position.y,
                self.heading,
            )
