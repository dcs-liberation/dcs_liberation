from typing import Type

from dcs.unittype import VehicleType
from dcs.vehicles import AirDefence

from game import Game
from game.theater import SamGroundObject
from game.theater.theatergroundobject import AirDefenseRange
from gen.to_remove.airdefensegroupgenerator import (
    AirDefenseGroupGenerator,
)


class NasamCGenerator(AirDefenseGroupGenerator):
    """
    This generate a Nasams group with AIM-120C missiles
    """

    name = "NASAMS AIM-120C"

    def __init__(self, game: Game, ground_object: SamGroundObject):
        super().__init__(game, ground_object)
        self.launcherType: Type[VehicleType] = AirDefence.NASAMS_LN_C

    def generate(self) -> None:
        # Command Post
        self.add_unit(
            AirDefence.NASAMS_Command_Post,
            "CP",
            self.position.x + 30,
            self.position.y + 30,
            self.heading,
        )
        # Radar
        self.add_unit(
            AirDefence.NASAMS_Radar_MPQ64F1,
            "RADAR",
            self.position.x - 30,
            self.position.y - 30,
            self.heading,
        )

        positions = self.get_circular_position(4, launcher_distance=120, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(
                self.launcherType,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium


class NasamBGenerator(NasamCGenerator):
    """
    This generate a Nasams group with AIM-120B missiles
    """

    name = "NASAMS AIM-120B"

    def __init__(self, game: Game, ground_object: SamGroundObject):
        super().__init__(game, ground_object)
        self.launcherType: Type[VehicleType] = AirDefence.NASAMS_LN_B
