from __future__ import annotations

from pathlib import Path
import yaml
from typing import ClassVar

from dataclasses import dataclass
from datetime import timedelta

from game.data.units import UnitClass
from game.utils import Distance, feet, nautical_miles


@dataclass
class GroundUnitProcurementRatios:
    ratios: dict[UnitClass, float]

    def for_unit_class(self, unit_class: UnitClass) -> float:
        try:
            return self.ratios[unit_class] / sum(self.ratios.values())
        except KeyError:
            return 0.0

    @staticmethod
    def from_dict(data: dict[str, float]) -> GroundUnitProcurementRatios:
        unit_class_enum_from_name = {unit.value: unit for unit in UnitClass}
        r = {}
        for unit_class in data:
            if unit_class not in unit_class_enum_from_name:
                raise ValueError(f"Could not find unit type {unit_class}")
            r[unit_class_enum_from_name[unit_class]] = float(data[unit_class])
        return GroundUnitProcurementRatios(r)


@dataclass(frozen=True)
class Doctrine:
    name: str

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

    _by_name: ClassVar[dict[str, Doctrine]] = {}
    _loaded: ClassVar[bool] = False

    @classmethod
    def register(cls, doctrine: Doctrine) -> None:
        if doctrine.name in cls._by_name:
            duplicate = cls._by_name[doctrine.name]
            raise ValueError(f"Doctrine {doctrine.name} is already loaded")
        cls._by_name[doctrine.name] = doctrine

    @classmethod
    def named(cls, name: str) -> Doctrine:
        if not cls._loaded:
            cls.load_all()
        return cls._by_name[name]

    @classmethod
    def all_doctrines(cls) -> list[Doctrine]:
        if not cls._loaded:
            cls.load_all()
        return list(cls._by_name.values())

    @classmethod
    def load_all(cls) -> None:
        if cls._loaded:
            return
        for doctrine_file_path in Path("resources/doctrines").glob("**/*.yaml"):
            with doctrine_file_path.open(encoding="utf8") as doctrine_file:
                data = yaml.safe_load(doctrine_file)
            cls.register(
                Doctrine(
                    name=data["name"],
                    cap=data["cap"],
                    cas=data["cas"],
                    sead=data["sead"],
                    strike=data["strike"],
                    antiship=data["antiship"],
                    rendezvous_altitude=feet(data["rendezvous_altitude_ft_msl"]),
                    hold_distance=nautical_miles(data["hold_distance_nm"]),
                    push_distance=nautical_miles(data["push_distance_nm"]),
                    join_distance=nautical_miles(data["join_distance_nm"]),
                    max_ingress_distance=nautical_miles(
                        data["max_ingress_distance_nm"]
                    ),
                    min_ingress_distance=nautical_miles(
                        data["min_ingress_distance_nm"]
                    ),
                    ingress_altitude=feet(data["ingress_altitude_ft_msl"]),
                    min_patrol_altitude=feet(data["min_patrol_altitude_ft_msl"]),
                    max_patrol_altitude=feet(data["max_patrol_altitude_ft_msl"]),
                    pattern_altitude=feet(data["pattern_altitude_ft_msl"]),
                    cap_duration=timedelta(minutes=data["cap_duration_minutes"]),
                    cap_min_track_length=nautical_miles(
                        data["cap_min_track_length_nm"]
                    ),
                    cap_max_track_length=nautical_miles(
                        data["cap_max_track_length_nm"]
                    ),
                    cap_min_distance_from_cp=nautical_miles(
                        data["cap_min_distance_from_cp_nm"]
                    ),
                    cap_max_distance_from_cp=nautical_miles(
                        data["cap_max_distance_from_cp_nm"]
                    ),
                    cap_engagement_range=nautical_miles(
                        data["cap_engagement_range_nm"]
                    ),
                    cas_duration=timedelta(minutes=data["cas_duration_minutes"]),
                    sweep_distance=nautical_miles(data["sweep_distance_nm"]),
                    ground_unit_procurement_ratios=GroundUnitProcurementRatios.from_dict(
                        data["ground_unit_procurement_ratios"]
                    ),
                )
            )
        cls._loaded = True
