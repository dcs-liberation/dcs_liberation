from __future__ import annotations

from pathlib import Path
import yaml
from typing import Any, ClassVar, Optional

from dataclasses import dataclass
from datetime import timedelta
from dcs.task import OptAAMissileAttackRange
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


@dataclass
class Helicopter:
    #: The altitude used for combat section of a flight, overrides the base combat_altitude parameter for helos
    combat_altitude: Distance

    #: The altitude used for forming up a pacakge. Overrides the base rendezvous_altitude parameter for helos
    rendezvous_altitude: Distance

    #: Altitude of the nav points (cruise section) of air assault missions.
    air_assault_nav_altitude: Distance

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Helicopter:
        return Helicopter(
            combat_altitude=feet(data["combat_altitude_ft_agl"]),
            rendezvous_altitude=feet(data["rendezvous_altitude_ft_agl"]),
            air_assault_nav_altitude=feet(data["air_assault_nav_altitude_ft_agl"]),
        )


@dataclass
class Cas:
    #: The duration that CAP flights will remain on-station.
    duration: timedelta

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Cas:
        return Cas(duration=timedelta(minutes=data["duration_minutes"]))


@dataclass
class Sweep:
    #: Length of the sweep / patrol leg
    distance: Distance

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Sweep:
        return Sweep(
            distance=nautical_miles(data["distance_nm"]),
        )


@dataclass
class Cap:
    #: The duration that CAP flights will remain on-station.
    duration: timedelta

    #: The minimum length of the CAP race track.
    min_track_length: Distance

    #: The maximum length of the CAP race track.
    max_track_length: Distance

    #: The minimum distance between the defended position and the *end* of the
    #: CAP race track.
    min_distance_from_cp: Distance

    #: The maximum distance between the defended position and the *end* of the
    #: CAP race track.
    max_distance_from_cp: Distance

    #: The engagement range of CAP flights. Any enemy aircraft within this range
    #: of the CAP's current position will be engaged by the CAP.
    engagement_range: Distance

    #: Defines the range of altitudes CAP racetracks are planned at.
    min_patrol_altitude: Distance
    max_patrol_altitude: Distance

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Cap:
        return Cap(
            duration=timedelta(minutes=data["duration_minutes"]),
            min_track_length=nautical_miles(data["min_track_length_nm"]),
            max_track_length=nautical_miles(data["max_track_length_nm"]),
            min_distance_from_cp=nautical_miles(data["min_distance_from_cp_nm"]),
            max_distance_from_cp=nautical_miles(data["max_distance_from_cp_nm"]),
            engagement_range=nautical_miles(data["engagement_range_nm"]),
            min_patrol_altitude=feet(data["min_patrol_altitude_ft_msl"]),
            max_patrol_altitude=feet(data["max_patrol_altitude_ft_msl"]),
        )


@dataclass(frozen=True)
class Tactics:

    #: Air-to-air missile attack range options
    air_to_air_missile_attack_range: Optional[OptAAMissileAttackRange.Values]

    #: Air defence units evade ARMs
    air_defence_evades_anti_radiation_missiles: bool

    @staticmethod
    def from_dict(data: dict[str, Any]) -> Tactics:
        return Tactics(
            air_to_air_missile_attack_range=None,
            air_defence_evades_anti_radiation_missiles=data.get(
                "air_defence_evades_anti_radiation_missiles", False
            ),
        )


@dataclass(frozen=True)
class Doctrine:
    #: Name of the doctrine, used to assign a doctrine in a faction.
    name: str

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

    #: The altitude used for combat section of a flight.
    combat_altitude: Distance

    #: The altitude used for forming up a pacakge.
    rendezvous_altitude: Distance

    #: Defines prioritization of ground unit purchases.
    ground_unit_procurement_ratios: GroundUnitProcurementRatios

    #: Helicopter specific doctrines.
    helicopter: Helicopter

    #: Doctrine for CAS missions.
    cas: Cas

    #: Doctrine for CAP missions.
    cap: Cap

    #: Doctrine for Fighter Sweep missions.
    sweep: Sweep

    #: Tactics options
    tactics: Tactics

    _by_name: ClassVar[dict[str, Doctrine]] = {}
    _loaded: ClassVar[bool] = False

    def resolve_combat_altitude(self, is_helo: bool = False) -> Distance:
        if is_helo:
            return self.helicopter.combat_altitude
        return self.combat_altitude

    def resolve_rendezvous_altitude(self, is_helo: bool = False) -> Distance:
        if is_helo:
            return self.helicopter.rendezvous_altitude
        return self.rendezvous_altitude

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
                    combat_altitude=feet(data["combat_altitude_ft_msl"]),
                    ground_unit_procurement_ratios=GroundUnitProcurementRatios.from_dict(
                        data["ground_unit_procurement_ratios"]
                    ),
                    helicopter=Helicopter.from_dict(data["helicopter"]),
                    cas=Cas.from_dict(data["cas"]),
                    cap=Cap.from_dict(data["cap"]),
                    sweep=Sweep.from_dict(data["sweep"]),
                    tactics=Tactics.from_dict(data.get("tactics", {})),
                )
            )
        cls._loaded = True
