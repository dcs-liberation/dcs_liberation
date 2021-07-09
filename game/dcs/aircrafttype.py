from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import ClassVar, Type, Iterator, TYPE_CHECKING, Optional, Any

import yaml
from dcs.helicopters import helicopter_map
from dcs.planes import plane_map
from dcs.unittype import FlyingType

from game.dcs.unittype import UnitType
from game.radio.channels import (
    ChannelNamer,
    RadioChannelAllocator,
    CommonRadioChannelAllocator,
    HueyChannelNamer,
    SCR522ChannelNamer,
    ViggenChannelNamer,
    ViperChannelNamer,
    TomcatChannelNamer,
    MirageChannelNamer,
    SingleRadioChannelNamer,
    FarmerRadioChannelAllocator,
    SCR522RadioChannelAllocator,
    ViggenRadioChannelAllocator,
    NoOpChannelAllocator,
)
from game.utils import Distance, Speed, feet, kph, knots

if TYPE_CHECKING:
    from gen.aircraft import FlightData
    from gen import AirSupport, RadioFrequency, RadioRegistry
    from gen.radios import Radio


@dataclass(frozen=True)
class RadioConfig:
    inter_flight: Optional[Radio]
    intra_flight: Optional[Radio]
    channel_allocator: Optional[RadioChannelAllocator]
    channel_namer: Type[ChannelNamer]

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> RadioConfig:
        return RadioConfig(
            cls.make_radio(data.get("inter_flight", None)),
            cls.make_radio(data.get("intra_flight", None)),
            cls.make_allocator(data.get("channels", {})),
            cls.make_namer(data.get("channels", {})),
        )

    @classmethod
    def make_radio(cls, name: Optional[str]) -> Optional[Radio]:
        from gen.radios import get_radio

        if name is None:
            return None
        return get_radio(name)

    @classmethod
    def make_allocator(cls, data: dict[str, Any]) -> Optional[RadioChannelAllocator]:
        try:
            alloc_type = data["type"]
        except KeyError:
            return None
        allocator_type: Type[RadioChannelAllocator] = {
            "SCR-522": SCR522RadioChannelAllocator,
            "common": CommonRadioChannelAllocator,
            "farmer": FarmerRadioChannelAllocator,
            "noop": NoOpChannelAllocator,
            "viggen": ViggenRadioChannelAllocator,
        }[alloc_type]
        return allocator_type.from_cfg(data)

    @classmethod
    def make_namer(cls, config: dict[str, Any]) -> Type[ChannelNamer]:
        return {
            "SCR-522": SCR522ChannelNamer,
            "default": ChannelNamer,
            "huey": HueyChannelNamer,
            "mirage": MirageChannelNamer,
            "single": SingleRadioChannelNamer,
            "tomcat": TomcatChannelNamer,
            "viggen": ViggenChannelNamer,
            "viper": ViperChannelNamer,
        }[config.get("namer", "default")]


@dataclass(frozen=True)
class PatrolConfig:
    altitude: Optional[Distance]
    speed: Optional[Speed]

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> PatrolConfig:
        altitude = data.get("altitude", None)
        speed = data.get("altitude", None)
        return PatrolConfig(
            feet(altitude) if altitude is not None else None,
            knots(speed) if speed is not None else None,
        )


@dataclass(frozen=True)
class AircraftType(UnitType[Type[FlyingType]]):
    carrier_capable: bool
    lha_capable: bool
    always_keeps_gun: bool

    # If true, the aircraft does not use the guns as the last resort weapons, but as a main weapon.
    # It'll RTB when it doesn't have gun ammo left.
    gunfighter: bool

    max_group_size: int
    patrol_altitude: Optional[Distance]
    patrol_speed: Optional[Speed]
    intra_flight_radio: Optional[Radio]
    channel_allocator: Optional[RadioChannelAllocator]
    channel_namer: Type[ChannelNamer]

    _by_name: ClassVar[dict[str, AircraftType]] = {}
    _by_unit_type: ClassVar[dict[Type[FlyingType], list[AircraftType]]] = defaultdict(
        list
    )
    _loaded: ClassVar[bool] = False

    def __str__(self) -> str:
        return self.name

    @property
    def dcs_id(self) -> str:
        return self.dcs_unit_type.id

    @property
    def flyable(self) -> bool:
        return self.dcs_unit_type.flyable

    @cached_property
    def max_speed(self) -> Speed:
        return kph(self.dcs_unit_type.max_speed)

    def alloc_flight_radio(self, radio_registry: RadioRegistry) -> RadioFrequency:
        from gen.radios import ChannelInUseError, MHz

        if self.intra_flight_radio is not None:
            return radio_registry.alloc_for_radio(self.intra_flight_radio)

        freq = MHz(self.dcs_unit_type.radio_frequency)
        try:
            radio_registry.reserve(freq)
        except ChannelInUseError:
            pass
        return freq

    def assign_channels_for_flight(
        self, flight: FlightData, air_support: AirSupport
    ) -> None:
        if self.channel_allocator is not None:
            self.channel_allocator.assign_channels_for_flight(flight, air_support)

    def channel_name(self, radio_id: int, channel_id: int) -> str:
        return self.channel_namer.channel_name(radio_id, channel_id)

    def __setstate__(self, state: dict[str, Any]) -> None:
        # Update any existing models with new data on load.
        updated = AircraftType.named(state["name"])
        state.update(updated.__dict__)
        self.__dict__.update(state)

    @classmethod
    def register(cls, aircraft_type: AircraftType) -> None:
        cls._by_name[aircraft_type.name] = aircraft_type
        cls._by_unit_type[aircraft_type.dcs_unit_type].append(aircraft_type)

    @classmethod
    def named(cls, name: str) -> AircraftType:
        if not cls._loaded:
            cls._load_all()
        return cls._by_name[name]

    @classmethod
    def for_dcs_type(cls, dcs_unit_type: Type[FlyingType]) -> Iterator[AircraftType]:
        if not cls._loaded:
            cls._load_all()
        yield from cls._by_unit_type[dcs_unit_type]

    @staticmethod
    def _each_unit_type() -> Iterator[Type[FlyingType]]:
        yield from helicopter_map.values()
        yield from plane_map.values()

    @classmethod
    def _load_all(cls) -> None:
        for unit_type in cls._each_unit_type():
            for data in cls._each_variant_of(unit_type):
                cls.register(data)
        cls._loaded = True

    @classmethod
    def _each_variant_of(cls, aircraft: Type[FlyingType]) -> Iterator[AircraftType]:
        data_path = Path("resources/units/aircraft") / f"{aircraft.id}.yaml"
        if not data_path.exists():
            logging.warning(f"No data for {aircraft.id}; it will not be available")
            return

        with data_path.open() as data_file:
            data = yaml.safe_load(data_file)

        try:
            price = data["price"]
        except KeyError as ex:
            raise KeyError(f"Missing required price field: {data_path}") from ex

        radio_config = RadioConfig.from_data(data.get("radios", {}))
        patrol_config = PatrolConfig.from_data(data.get("patrol", {}))

        try:
            introduction = data["introduced"]
            if introduction is None:
                introduction = "N/A"
        except KeyError:
            introduction = "No data."

        for variant in data.get("variants", [aircraft.id]):
            yield AircraftType(
                dcs_unit_type=aircraft,
                name=variant,
                description=data.get(
                    "description",
                    f"No data. <a href=\"https://google.com/search?q=DCS+{variant.replace(' ', '+')}\"><span style=\"color:#FFFFFF\">Google {variant}</span></a>",
                ),
                year_introduced=introduction,
                country_of_origin=data.get("origin", "No data."),
                manufacturer=data.get("manufacturer", "No data."),
                role=data.get("role", "No data."),
                price=price,
                carrier_capable=data.get("carrier_capable", False),
                lha_capable=data.get("lha_capable", False),
                always_keeps_gun=data.get("always_keeps_gun", False),
                gunfighter=data.get("gunfighter", False),
                max_group_size=data.get("max_group_size", aircraft.group_size_max),
                patrol_altitude=patrol_config.altitude,
                patrol_speed=patrol_config.speed,
                intra_flight_radio=radio_config.intra_flight,
                channel_allocator=radio_config.channel_allocator,
                channel_namer=radio_config.channel_namer,
            )
