from typing import Type

from dcs.unittype import VehicleType
from dcs.vehicles import AirDefence, Unarmed

from game import Game
from game.theater import SamGroundObject
from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class SA5Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-5 group using the TinShield SR
    """

    name = "SA-5/S-200 Site"

    def __init__(self, game: Game, ground_object: SamGroundObject):
        super().__init__(game, ground_object)
        self.sr: Type[VehicleType] = AirDefence.RLS_19J6

    def generate(self) -> None:
        self.add_unit(
            self.sr,
            "SR",
            self.position.x,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.RPC_5N62V,
            "TR",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            Unarmed.Ural_375,
            "LOGI",
            self.position.x - 20,
            self.position.y,
            self.heading,
        )

        num_launchers = 6
        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=360
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.S_200_Launcher,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Long


# TODO Replace this legacy handling once the Generators can be faction sensitive #1903
class SA5FlatFaceGenerator(SA5Generator):
    """
    This generate a SA-5 group using the P-19 FlatFace SR
    """

    def __init__(self, game: Game, ground_object: SamGroundObject):
        super().__init__(game, ground_object)
        self.sr: Type[VehicleType] = AirDefence.P_19_s_125_sr
