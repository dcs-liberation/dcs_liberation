from dataclasses import dataclass
from datetime import timedelta

from game.utils import nm_to_meter, feet_to_meter


@dataclass(frozen=True)
class Doctrine:
    cas: bool
    cap: bool
    sead: bool
    strike: bool
    antiship: bool

    strike_max_range: int
    sead_max_range: int

    rendezvous_altitude: int
    join_distance: int
    split_distance: int
    ingress_egress_distance: int
    ingress_altitude: int
    egress_altitude: int

    min_patrol_altitude: int
    max_patrol_altitude: int
    pattern_altitude: int

    cap_duration: timedelta
    cap_min_track_length: int
    cap_max_track_length: int
    cap_min_distance_from_cp: int
    cap_max_distance_from_cp: int

    cas_duration: timedelta


MODERN_DOCTRINE = Doctrine(
    cap=True,
    cas=True,
    sead=True,
    strike=True,
    antiship=True,
    strike_max_range=1500000,
    sead_max_range=1500000,
    rendezvous_altitude=feet_to_meter(25000),
    join_distance=nm_to_meter(20),
    split_distance=nm_to_meter(20),
    ingress_egress_distance=nm_to_meter(45),
    ingress_altitude=feet_to_meter(20000),
    egress_altitude=feet_to_meter(20000),
    min_patrol_altitude=feet_to_meter(15000),
    max_patrol_altitude=feet_to_meter(33000),
    pattern_altitude=feet_to_meter(5000),
    cap_duration=timedelta(minutes=30),
    cap_min_track_length=nm_to_meter(15),
    cap_max_track_length=nm_to_meter(40),
    cap_min_distance_from_cp=nm_to_meter(10),
    cap_max_distance_from_cp=nm_to_meter(40),
    cas_duration=timedelta(minutes=30),
)

COLDWAR_DOCTRINE = Doctrine(
    cap=True,
    cas=True,
    sead=True,
    strike=True,
    antiship=True,
    strike_max_range=1500000,
    sead_max_range=1500000,
    rendezvous_altitude=feet_to_meter(22000),
    join_distance=nm_to_meter(10),
    split_distance=nm_to_meter(10),
    ingress_egress_distance=nm_to_meter(30),
    ingress_altitude=feet_to_meter(18000),
    egress_altitude=feet_to_meter(18000),
    min_patrol_altitude=feet_to_meter(10000),
    max_patrol_altitude=feet_to_meter(24000),
    pattern_altitude=feet_to_meter(5000),
    cap_duration=timedelta(minutes=30),
    cap_min_track_length=nm_to_meter(12),
    cap_max_track_length=nm_to_meter(24),
    cap_min_distance_from_cp=nm_to_meter(8),
    cap_max_distance_from_cp=nm_to_meter(25),
    cas_duration=timedelta(minutes=30),
)

WWII_DOCTRINE = Doctrine(
    cap=True,
    cas=True,
    sead=False,
    strike=True,
    antiship=True,
    strike_max_range=1500000,
    sead_max_range=1500000,
    join_distance=nm_to_meter(5),
    split_distance=nm_to_meter(5),
    rendezvous_altitude=feet_to_meter(10000),
    ingress_egress_distance=nm_to_meter(7),
    ingress_altitude=feet_to_meter(8000),
    egress_altitude=feet_to_meter(8000),
    min_patrol_altitude=feet_to_meter(4000),
    max_patrol_altitude=feet_to_meter(15000),
    pattern_altitude=feet_to_meter(5000),
    cap_duration=timedelta(minutes=30),
    cap_min_track_length=nm_to_meter(8),
    cap_max_track_length=nm_to_meter(18),
    cap_min_distance_from_cp=nm_to_meter(0),
    cap_max_distance_from_cp=nm_to_meter(5),
    cas_duration=timedelta(minutes=30),
)
