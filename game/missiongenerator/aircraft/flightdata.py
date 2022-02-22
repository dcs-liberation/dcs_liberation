from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional, TYPE_CHECKING

from dcs.flyingunit import FlyingUnit

from game.callsigns import create_group_callsign_from_unit

if TYPE_CHECKING:
    from game.ato import FlightType, FlightWaypoint, Package
    from game.dcs.aircrafttype import AircraftType
    from game.radio.radios import RadioFrequency
    from game.runways import RunwayData


@dataclass(frozen=True)
class ChannelAssignment:
    radio_id: int
    channel: int


@dataclass
class FlightData:
    """Details of a planned flight."""

    #: The package that the flight belongs to.
    package: Package

    flight_type: FlightType

    aircraft_type: AircraftType

    #: All units in the flight.
    units: list[FlyingUnit]

    #: Total number of aircraft in the flight.
    size: int

    #: True if this flight belongs to the player's coalition.
    friendly: bool

    #: Number of seconds after mission start the flight is set to depart.
    departure_delay: timedelta

    #: Arrival airport.
    arrival: RunwayData

    #: Departure airport.
    departure: RunwayData

    #: Diver airport.
    divert: Optional[RunwayData]

    #: Waypoints of the flight plan.
    waypoints: list[FlightWaypoint]

    #: Radio frequency for intra-flight communications.
    intra_flight_channel: RadioFrequency

    #: Bingo fuel value in lbs.
    bingo_fuel: Optional[int]

    joker_fuel: Optional[int]

    laser_codes: list[Optional[int]]

    custom_name: Optional[str]

    callsign: str = field(init=False)

    #: Map of radio frequencies to their assigned radio and channel, if any.
    frequency_to_channel_map: dict[RadioFrequency, ChannelAssignment] = field(
        init=False, default_factory=dict
    )

    def __post_init__(self) -> None:
        self.callsign = create_group_callsign_from_unit(self.units[0])

    @property
    def client_units(self) -> list[FlyingUnit]:
        """List of playable units in the flight."""
        return [u for u in self.units if u.is_human()]

    def num_radio_channels(self, radio_id: int) -> int:
        """Returns the number of preset channels for the given radio."""
        # Note: pydcs only initializes the radio presets for client slots.
        return self.client_units[0].num_radio_channels(radio_id)

    def channel_for(self, frequency: RadioFrequency) -> Optional[ChannelAssignment]:
        """Returns the radio and channel number for the given frequency."""
        return self.frequency_to_channel_map.get(frequency, None)

    def assign_channel(
        self, radio_id: int, channel_id: int, frequency: RadioFrequency
    ) -> None:
        """Assigns a preset radio channel to the given frequency."""
        for unit in self.client_units:
            unit.set_radio_channel_preset(radio_id, channel_id, frequency.mhz)

        # One frequency could be bound to multiple channels. Prefer the first,
        # since with the current implementation it will be the lowest numbered
        # channel.
        if frequency not in self.frequency_to_channel_map:
            self.frequency_to_channel_map[frequency] = ChannelAssignment(
                radio_id, channel_id
            )
