from dataclasses import dataclass
from datetime import timedelta

from game.utils import Distance, feet, nautical_miles


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

    cap_duration: timedelta
    cap_min_track_length: Distance
    cap_max_track_length: Distance
    cap_min_distance_from_cp: Distance
    cap_max_distance_from_cp: Distance

    cas_duration: timedelta

    sweep_distance: Distance


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
    cas_duration=timedelta(minutes=30),
    sweep_distance=nautical_miles(60),
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
    cas_duration=timedelta(minutes=30),
    sweep_distance=nautical_miles(40),
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
    cas_duration=timedelta(minutes=30),
    sweep_distance=nautical_miles(10),
)
