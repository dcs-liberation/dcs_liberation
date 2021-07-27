from typing import Type

from dcs.unittype import VehicleType
from dcs.vehicles import AirDefence

from game.theater.theatergroundobject import EwrGroundObject
from gen.sam.group_generator import VehicleGroupGenerator


class EwrGenerator(VehicleGroupGenerator[EwrGroundObject]):
    unit_type: Type[VehicleType]

    @classmethod
    def name(cls) -> str:
        return cls.unit_type.name

    def generate(self) -> None:
        self.add_unit(
            self.unit_type, "EWR", self.position.x, self.position.y, self.heading
        )


class BoxSpringGenerator(EwrGenerator):
    """1L13 "Box Spring" EWR."""

    unit_type = AirDefence._1L13_EWR


class TallRackGenerator(EwrGenerator):
    """55G6 "Tall Rack" EWR."""

    unit_type = AirDefence._55G6_EWR


class DogEarGenerator(EwrGenerator):
    """9S80M1 "Dog Ear" EWR.

    This is the SA-8 search radar, but used as an early warning radar.
    """

    unit_type = AirDefence.Dog_Ear_radar


class RolandEwrGenerator(EwrGenerator):
    """Roland EWR.

    This is the Roland search radar, but used as an early warning radar.
    """

    unit_type = AirDefence.Roland_Radar


class FlatFaceGenerator(EwrGenerator):
    """P-19 "Flat Face" EWR.

    This is the SA-3 search radar, but used as an early warning radar.
    """

    unit_type = AirDefence.P_19_s_125_sr


class PatriotEwrGenerator(EwrGenerator):
    """Patriot EWR.

    This is the Patriot search/track radar, but used as an early warning radar.
    """

    unit_type = AirDefence.Patriot_str


class BigBirdGenerator(EwrGenerator):
    """64H6E "Big Bird" EWR.

    This is the SA-10 track radar, but used as an early warning radar.
    """

    unit_type = AirDefence.S_300PS_64H6E_sr


class SnowDriftGenerator(EwrGenerator):
    """9S18M1 "Snow Drift" EWR.

    This is the SA-11 search radar, but used as an early warning radar.
    """

    unit_type = AirDefence.SA_11_Buk_SR_9S18M1


class StraightFlushGenerator(EwrGenerator):
    """1S91 "Straight Flush" EWR.

    This is the SA-6 search/track radar, but used as an early warning radar.
    """

    unit_type = AirDefence.Kub_1S91_str


class HawkEwrGenerator(EwrGenerator):
    """Hawk EWR.

    This is the Hawk search radar, but used as an early warning radar.
    """

    unit_type = AirDefence.Hawk_sr


class TinShieldGenerator(EwrGenerator):
    """19ZH6 "Tin Shield" EWR."""

    unit_type = AirDefence.RLS_19J6
