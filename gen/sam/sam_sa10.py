import random

from dcs.mapping import Point
from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class SA10Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-10 group
    """

    name = "SA-10/S-300PS Battery"
    price = 550

    def generate(self):
        # Search Radar
        self.add_unit(AirDefence.SAM_SA_10_S_300PS_SR_5N66M, "SR1", self.position.x, self.position.y + 40, self.heading)

        # Search radar for missiles (optionnal)
        self.add_unit(AirDefence.SAM_SA_10_S_300PS_SR_64H6E, "SR2", self.position.x - 40, self.position.y, self.heading)

        # Command Post
        self.add_unit(AirDefence.SAM_SA_10_S_300PS_CP_54K6, "CP", self.position.x, self.position.y, self.heading)

        # 2 Tracking radars
        self.add_unit(AirDefence.SAM_SA_10_S_300PS_TR_30N6, "TR1", self.position.x - 40, self.position.y - 40, self.heading)

        self.add_unit(AirDefence.SAM_SA_10_S_300PS_TR_30N6, "TR2", self.position.x + 40, self.position.y - 40,
                      self.heading)

        # 2 different launcher type (C & D)
        num_launchers = random.randint(6, 8)
        positions = self.get_circular_position(num_launchers, launcher_distance=100, coverage=360)
        for i, position in enumerate(positions):
            if i%2 == 0:
                self.add_unit(AirDefence.SAM_SA_10_S_300PS_LN_5P85C, "LN#" + str(i), position[0], position[1], position[2])
            else:
                self.add_unit(AirDefence.SAM_SA_10_S_300PS_LN_5P85D, "LN#" + str(i), position[0], position[1], position[2])

        self.generate_defensive_groups()

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Long

    def generate_defensive_groups(self) -> None:
        # AAA for defending against close targets.
        aa_group = self.add_auxiliary_group("AA")
        num_launchers = random.randint(6, 8)
        positions = self.get_circular_position(
            num_launchers, launcher_distance=210, coverage=360)
        for i, (x, y, heading) in enumerate(positions):
            self.add_unit_to_group(aa_group, AirDefence.SPAAA_ZSU_23_4_Shilka,
                                   f"AA#{i}", Point(x, y), heading)


class Tier2SA10Generator(SA10Generator):
    def generate_defensive_groups(self) -> None:
        # Create AAA the way the main group does.
        super().generate_defensive_groups()

        # SA-15 for both shorter range targets and point defense.
        pd_group = self.add_auxiliary_group("PD")
        num_launchers = random.randint(2, 4)
        positions = self.get_circular_position(
            num_launchers, launcher_distance=140, coverage=360)
        for i, (x, y, heading) in enumerate(positions):
            self.add_unit_to_group(pd_group, AirDefence.SAM_SA_15_Tor_9A331,
                                   f"PD#{i}", Point(x, y), heading)


class Tier3SA10Generator(SA10Generator):
    def generate_defensive_groups(self) -> None:
        # AAA for defending against close targets.
        aa_group = self.add_auxiliary_group("AA")
        num_launchers = random.randint(6, 8)
        positions = self.get_circular_position(
            num_launchers, launcher_distance=210, coverage=360)
        for i, (x, y, heading) in enumerate(positions):
            self.add_unit_to_group(aa_group, AirDefence.SAM_SA_19_Tunguska_2S6,
                                   f"AA#{i}", Point(x, y), heading)

        # SA-15 for both shorter range targets and point defense.
        pd_group = self.add_auxiliary_group("PD")
        num_launchers = random.randint(2, 4)
        positions = self.get_circular_position(
            num_launchers, launcher_distance=140, coverage=360)
        for i, (x, y, heading) in enumerate(positions):
            self.add_unit_to_group(pd_group, AirDefence.SAM_SA_15_Tor_9A331,
                                   f"PD#{i}", Point(x, y), heading)
