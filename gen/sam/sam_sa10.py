from dcs.mapping import Point
from dcs.vehicles import AirDefence

from game import Game
from game.theater import SamGroundObject
from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
    SkynetRole,
)
from pydcs_extensions.highdigitsams import highdigitsams


class SA10Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-10 group
    """

    name = "SA-10/S-300PS Battery - With ZSU-23"

    def __init__(self, game: Game, ground_object: SamGroundObject):
        super().__init__(game, ground_object)
        self.sr1 = AirDefence.S_300PS_40B6MD_sr
        self.sr2 = AirDefence.S_300PS_64H6E_sr
        self.cp = AirDefence.S_300PS_54K6_cp
        self.tr1 = AirDefence.S_300PS_40B6M_tr
        self.tr2 = AirDefence.S_300PS_40B6M_tr
        self.ln1 = AirDefence.S_300PS_5P85C_ln
        self.ln2 = AirDefence.S_300PS_5P85D_ln

    def generate(self) -> None:
        # Search Radar
        self.add_unit(
            self.sr1, "SR1", self.position.x, self.position.y + 40, self.heading
        )

        # Search radar for missiles (optionnal)
        self.add_unit(
            self.sr2, "SR2", self.position.x - 40, self.position.y, self.heading
        )

        # Command Post
        self.add_unit(self.cp, "CP", self.position.x, self.position.y, self.heading)

        # 1 Tracking radar
        self.add_unit(
            self.tr1, "TR1", self.position.x - 40, self.position.y - 40, self.heading
        )

        # 2 different launcher type (C & D)
        num_launchers = 6
        positions = self.get_circular_position(
            num_launchers, launcher_distance=100, coverage=360
        )
        for i, position in enumerate(positions):
            if i % 2 == 0:
                self.add_unit(
                    self.ln1, "LN#" + str(i), position[0], position[1], position[2]
                )
            else:
                self.add_unit(
                    self.ln2, "LN#" + str(i), position[0], position[1], position[2]
                )

        self.generate_defensive_groups()

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Long

    def generate_defensive_groups(self) -> None:
        # AAA for defending against close targets.
        aa_group = self.add_auxiliary_group(SkynetRole.NoSkynetBehavior)
        num_launchers = 2
        positions = self.get_circular_position(
            num_launchers, launcher_distance=210, coverage=360
        )
        for i, (x, y, heading) in enumerate(positions):
            self.add_unit_to_group(
                aa_group,
                AirDefence.ZSU_23_4_Shilka,
                f"AA#{i}",
                Point(x, y),
                heading,
            )


class Tier2SA10Generator(SA10Generator):

    name = "SA-10/S-300PS Battery - With SA-15 PD"

    def generate_defensive_groups(self) -> None:
        # Create AAA the way the main group does.
        super().generate_defensive_groups()

        # SA-15 for both shorter range targets and point defense.
        pd_group = self.add_auxiliary_group(SkynetRole.PointDefense)
        num_launchers = 2
        positions = self.get_circular_position(
            num_launchers, launcher_distance=140, coverage=360
        )
        for i, (x, y, heading) in enumerate(positions):
            self.add_unit_to_group(
                pd_group,
                AirDefence.Tor_9A331,
                f"PD#{i}",
                Point(x, y),
                heading,
            )


class Tier3SA10Generator(SA10Generator):

    name = "SA-10/S-300PS Battery - With SA-15 PD & SA-19 SHORAD"

    def generate_defensive_groups(self) -> None:
        # AAA for defending against close targets.
        aa_group = self.add_auxiliary_group(SkynetRole.NoSkynetBehavior)
        num_launchers = 2
        positions = self.get_circular_position(
            num_launchers, launcher_distance=210, coverage=360
        )
        for i, (x, y, heading) in enumerate(positions):
            self.add_unit_to_group(
                aa_group,
                AirDefence._2S6_Tunguska,
                f"AA#{i}",
                Point(x, y),
                heading,
            )

        # SA-15 for both shorter range targets and point defense.
        pd_group = self.add_auxiliary_group(SkynetRole.PointDefense)
        num_launchers = 2
        positions = self.get_circular_position(
            num_launchers, launcher_distance=140, coverage=360
        )
        for i, (x, y, heading) in enumerate(positions):
            self.add_unit_to_group(
                pd_group,
                AirDefence.Tor_9A331,
                f"PD#{i}",
                Point(x, y),
                heading,
            )


class SA10BGenerator(Tier3SA10Generator):

    name = "SA-10B/S-300PS Battery"

    def __init__(self, game: Game, ground_object: SamGroundObject):
        super().__init__(game, ground_object)
        self.sr1 = highdigitsams.SAM_SA_10B_S_300PS_40B6MD_SR
        self.sr2 = highdigitsams.SAM_SA_10B_S_300PS_64H6E_SR
        self.cp = highdigitsams.SAM_SA_10B_S_300PS_54K6_CP
        self.tr1 = highdigitsams.SAM_SA_10B_S_300PS_30N6_TR
        self.tr2 = highdigitsams.SAM_SA_10B_S_300PS_40B6M_TR
        self.ln1 = highdigitsams.SAM_SA_10B_S_300PS_5P85SE_LN
        self.ln2 = highdigitsams.SAM_SA_10B_S_300PS_5P85SU_LN


class SA12Generator(Tier3SA10Generator):

    name = "SA-12/S-300V Battery"

    def __init__(self, game: Game, ground_object: SamGroundObject):
        super().__init__(game, ground_object)
        self.sr1 = highdigitsams.SAM_SA_12_S_300V_9S15_SR
        self.sr2 = highdigitsams.SAM_SA_12_S_300V_9S19_SR
        self.cp = highdigitsams.SAM_SA_12_S_300V_9S457_CP
        self.tr1 = highdigitsams.SAM_SA_12_S_300V_9S32_TR
        self.tr2 = highdigitsams.SAM_SA_12_S_300V_9S32_TR
        self.ln1 = highdigitsams.SAM_SA_12_S_300V_9A82_LN
        self.ln2 = highdigitsams.SAM_SA_12_S_300V_9A83_LN


class SA20Generator(Tier3SA10Generator):

    name = "SA-20/S-300PMU-1 Battery"

    def __init__(self, game: Game, ground_object: SamGroundObject):
        super().__init__(game, ground_object)
        self.sr1 = highdigitsams.SAM_SA_20_S_300PMU1_SR_5N66E
        self.sr2 = highdigitsams.SAM_SA_20_S_300PMU1_SR_64N6E
        self.cp = highdigitsams.SAM_SA_20_S_300PMU1_CP_54K6
        self.tr1 = highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E
        self.tr2 = highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E_truck
        self.ln1 = highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85CE
        self.ln2 = highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85DE


class SA20BGenerator(Tier3SA10Generator):

    name = "SA-20B/S-300PMU-2 Battery"

    def __init__(self, game: Game, ground_object: SamGroundObject):
        super().__init__(game, ground_object)
        self.sr1 = highdigitsams.SAM_SA_20_S_300PMU1_SR_5N66E
        self.sr2 = highdigitsams.SAM_SA_20_S_300PMU1_SR_64N6E
        self.cp = highdigitsams.SAM_SA_20B_S_300PMU2_CP_54K6E2
        self.tr1 = highdigitsams.SAM_SA_20B_S_300PMU2_TR_92H6E_truck
        self.tr2 = highdigitsams.SAM_SA_20B_S_300PMU2_TR_92H6E_truck
        self.ln1 = highdigitsams.SAM_SA_20B_S_300PMU2_LN_5P85SE2
        self.ln2 = highdigitsams.SAM_SA_20B_S_300PMU2_LN_5P85SE2


class SA23Generator(Tier3SA10Generator):

    name = "SA-23/S-300VM Battery"

    def __init__(self, game: Game, ground_object: SamGroundObject):
        super().__init__(game, ground_object)
        self.sr1 = highdigitsams.SAM_SA_23_S_300VM_9S15M2_SR
        self.sr2 = highdigitsams.SAM_SA_23_S_300VM_9S19M2_SR
        self.cp = highdigitsams.SAM_SA_23_S_300VM_9S457ME_CP
        self.tr1 = highdigitsams.SAM_SA_23_S_300VM_9S32ME_TR
        self.tr2 = highdigitsams.SAM_SA_23_S_300VM_9S32ME_TR
        self.ln1 = highdigitsams.SAM_SA_23_S_300VM_9A82ME_LN
        self.ln2 = highdigitsams.SAM_SA_23_S_300VM_9A83ME_LN
