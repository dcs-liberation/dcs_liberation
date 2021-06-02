from dataclasses import dataclass
from datetime import timedelta
from dcs.task import Reconnaissance

from game.utils import Distance, feet, nautical_miles
from game.data.groundunitclass import GroundUnitClass


@dataclass
class GroundUnitProcurementRatios:
    ratios: dict[GroundUnitClass, float]

    def for_unit_class(self, unit_class: GroundUnitClass) -> float:
        try:
            return self.ratios[unit_class] / sum(self.ratios.values())
        except KeyError:
            return 0.0


@dataclass(frozen=True)
class Doctrine:
    cas: bool
    cap: bool
    sead: bool
    strike: bool
    antiship: bool

    rendezvous_altitude: Distance
    hold_distance: Distance
    push_distance: Distance
    join_distance: Distance
    split_distance: Distance
    ingress_egress_distance: Distance
    ingress_altitude: Distance
    egress_altitude: Distance

    min_patrol_altitude: Distance
    max_patrol_altitude: Distance
    pattern_altitude: Distance

    #: The duration that CAP flights will remain on-station.
    cap_duration: timedelta

    #: The minimum length of the CAP race track.
    cap_min_track_length: Distance

    #: The maximum length of the CAP race track.
    cap_max_track_length: Distance

    #: The minimum distance between the defended position and the *end* of the
    #: CAP race track.
    cap_min_distance_from_cp: Distance

    #: The maximum distance between the defended position and the *end* of the
    #: CAP race track.
    cap_max_distance_from_cp: Distance

    #: The engagement range of CAP flights. Any enemy aircraft within this range
    #: of the CAP's current position will be engaged by the CAP.
    cap_engagement_range: Distance

    cas_duration: timedelta

    sweep_distance: Distance

    ground_unit_procurement_ratios: GroundUnitProcurementRatios


MODERN_DOCTRINE = Doctrine(
    cap=True,
    cas=True,
    sead=True,
    strike=True,
    antiship=True,
    rendezvous_altitude=feet(25000),
    hold_distance=nautical_miles(15),
    push_distance=nautical_miles(20),
    join_distance=nautical_miles(20),
    split_distance=nautical_miles(20),
    ingress_egress_distance=nautical_miles(45),
    ingress_altitude=feet(20000),
    egress_altitude=feet(20000),
    min_patrol_altitude=feet(15000),
    max_patrol_altitude=feet(33000),
    pattern_altitude=feet(5000),
    cap_duration=timedelta(minutes=30),
    cap_min_track_length=nautical_miles(15),
    cap_max_track_length=nautical_miles(40),
    cap_min_distance_from_cp=nautical_miles(10),
    cap_max_distance_from_cp=nautical_miles(40),
    cap_engagement_range=nautical_miles(50),
    cas_duration=timedelta(minutes=30),
    sweep_distance=nautical_miles(60),
    ground_unit_procurement_ratios=GroundUnitProcurementRatios(
        {
            GroundUnitClass.Tank: 3,
            GroundUnitClass.Atgm: 2,
            GroundUnitClass.Apc: 2,
            GroundUnitClass.Ifv: 3,
            GroundUnitClass.Artillery: 1,
            GroundUnitClass.Shorads: 2,
            GroundUnitClass.Recon: 2,
        }
    ),
)

COLDWAR_DOCTRINE = Doctrine(
    cap=True,
    cas=True,
    sead=True,
    strike=True,
    antiship=True,
    rendezvous_altitude=feet(22000),
    hold_distance=nautical_miles(10),
    push_distance=nautical_miles(10),
    join_distance=nautical_miles(10),
    split_distance=nautical_miles(10),
    ingress_egress_distance=nautical_miles(30),
    ingress_altitude=feet(18000),
    egress_altitude=feet(18000),
    min_patrol_altitude=feet(10000),
    max_patrol_altitude=feet(24000),
    pattern_altitude=feet(5000),
    cap_duration=timedelta(minutes=30),
    cap_min_track_length=nautical_miles(12),
    cap_max_track_length=nautical_miles(24),
    cap_min_distance_from_cp=nautical_miles(8),
    cap_max_distance_from_cp=nautical_miles(25),
    cap_engagement_range=nautical_miles(35),
    cas_duration=timedelta(minutes=30),
    sweep_distance=nautical_miles(40),
    ground_unit_procurement_ratios=GroundUnitProcurementRatios(
        {
            GroundUnitClass.Tank: 3,
            GroundUnitClass.Atgm: 2,
            GroundUnitClass.Apc: 3,
            GroundUnitClass.Ifv: 2,
            GroundUnitClass.Artillery: 1,
            GroundUnitClass.Shorads: 2,
            GroundUnitClass.Recon: 1,
        }
    ),
)

WWII_DOCTRINE = Doctrine(
    cap=True,
    cas=True,
    sead=False,
    strike=True,
    antiship=True,
    hold_distance=nautical_miles(5),
    push_distance=nautical_miles(5),
    join_distance=nautical_miles(5),
    split_distance=nautical_miles(5),
    rendezvous_altitude=feet(10000),
    ingress_egress_distance=nautical_miles(7),
    ingress_altitude=feet(8000),
    egress_altitude=feet(8000),
    min_patrol_altitude=feet(4000),
    max_patrol_altitude=feet(15000),
    pattern_altitude=feet(5000),
    cap_duration=timedelta(minutes=30),
    cap_min_track_length=nautical_miles(8),
    cap_max_track_length=nautical_miles(18),
    cap_min_distance_from_cp=nautical_miles(0),
    cap_max_distance_from_cp=nautical_miles(5),
    cap_engagement_range=nautical_miles(20),
    cas_duration=timedelta(minutes=30),
    sweep_distance=nautical_miles(10),
    ground_unit_procurement_ratios=GroundUnitProcurementRatios(
        {
            GroundUnitClass.Tank: 3,
            GroundUnitClass.Atgm: 3,
            GroundUnitClass.Apc: 3,
            GroundUnitClass.Artillery: 1,
            GroundUnitClass.Shorads: 3,
            GroundUnitClass.Recon: 1,
        }
    ),
)
