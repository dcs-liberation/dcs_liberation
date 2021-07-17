from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from game.data.groundunitclass import GroundUnitClass
from game.savecompat import has_save_compat_for
from game.utils import Distance, feet, nautical_miles


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

    #: The minimum distance between the departure airfield and the hold point.
    hold_distance: Distance

    #: The minimum distance between the hold point and the join point.
    push_distance: Distance

    #: The distance between the join point and the ingress point. Only used for the
    #: fallback flight plan layout (when the departure airfield is near a threat zone).
    join_distance: Distance

    #: The maximum distance between the ingress point (beginning of the attack) and
    #: target.
    max_ingress_distance: Distance

    #: The minimum distance between the ingress point (beginning of the attack) and
    #: target.
    min_ingress_distance: Distance

    ingress_altitude: Distance

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

    @has_save_compat_for(5)
    def __setstate__(self, state: dict[str, Any]) -> None:
        if "max_ingress_distance" not in state:
            try:
                state["max_ingress_distance"] = state["ingress_distance"]
                del state["ingress_distance"]
            except KeyError:
                state["max_ingress_distance"] = state["ingress_egress_distance"]
                del state["ingress_egress_distance"]

        max_ip: Distance = state["max_ingress_distance"]
        if "min_ingress_distance" not in state:
            if max_ip < nautical_miles(10):
                min_ip = nautical_miles(5)
            else:
                min_ip = nautical_miles(10)
            state["min_ingress_distance"] = min_ip

        self.__dict__.update(state)


class MissionPlannerMaxRanges:
    @has_save_compat_for(5)
    def __init__(self) -> None:
        pass


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
    max_ingress_distance=nautical_miles(45),
    min_ingress_distance=nautical_miles(10),
    ingress_altitude=feet(20000),
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
            GroundUnitClass.Recon: 1,
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
    max_ingress_distance=nautical_miles(30),
    min_ingress_distance=nautical_miles(10),
    ingress_altitude=feet(18000),
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
            GroundUnitClass.Tank: 4,
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
    rendezvous_altitude=feet(10000),
    max_ingress_distance=nautical_miles(7),
    min_ingress_distance=nautical_miles(5),
    ingress_altitude=feet(8000),
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
