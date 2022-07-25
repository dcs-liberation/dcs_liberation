from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from game.missiongenerator.aircraft.flightdata import FlightData
    from game.missiongenerator.missiondata import MissionData


class RadioChannelAllocator:
    """Base class for radio channel allocators."""

    def assign_channels_for_flight(
        self, flight: FlightData, mission_data: MissionData
    ) -> None:
        """Assigns mission frequencies to preset channels for the flight."""
        raise NotImplementedError

    @classmethod
    def from_cfg(cls, cfg: dict[str, Any]) -> RadioChannelAllocator:
        return cls()

    @classmethod
    def name(cls) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class CommonRadioChannelAllocator(RadioChannelAllocator):
    """Radio channel allocator suitable for most aircraft.

    Most of the aircraft with preset channels available have one or more radios
    with 20 or more channels available (typically per-radio, but this is not the
    case for the JF-17).
    """

    #: Index of the radio used for intra-flight communications. Matches the
    #: index of the panel_radio field of the pydcs.dcs.planes object.
    inter_flight_radio_index: Optional[int]

    #: Index of the radio used for intra-flight communications. Matches the
    #: index of the panel_radio field of the pydcs.dcs.planes object.
    intra_flight_radio_index: Optional[int]

    def assign_channels_for_flight(
        self, flight: FlightData, mission_data: MissionData
    ) -> None:
        if self.intra_flight_radio_index is not None:
            flight.assign_channel(
                self.intra_flight_radio_index, 1, flight.intra_flight_channel
            )

        if self.inter_flight_radio_index is None:
            return

        # For cases where the inter-flight and intra-flight radios share presets
        # (the JF-17 only has one set of channels, even though it can use two
        # channels simultaneously), start assigning inter-flight channels at 2.
        radio_id = self.inter_flight_radio_index
        if self.intra_flight_radio_index == radio_id:
            first_channel = 2
        else:
            first_channel = 1

        last_channel = flight.num_radio_channels(radio_id)
        channel_alloc = iter(range(first_channel, last_channel + 1))

        if flight.departure.atc is not None:
            flight.assign_channel(radio_id, next(channel_alloc), flight.departure.atc)

        # TODO: If there ever are multiple AWACS, limit to mission relevant.
        for awacs in mission_data.awacs:
            flight.assign_channel(radio_id, next(channel_alloc), awacs.freq)

        for jtac in mission_data.jtacs:
            flight.assign_channel(radio_id, next(channel_alloc), jtac.freq)

        if flight.arrival != flight.departure and flight.arrival.atc is not None:
            flight.assign_channel(radio_id, next(channel_alloc), flight.arrival.atc)

        try:
            # TODO: Skip incompatible tankers.
            for tanker in mission_data.tankers:
                flight.assign_channel(radio_id, next(channel_alloc), tanker.freq)

            if flight.divert is not None and flight.divert.atc is not None:
                flight.assign_channel(radio_id, next(channel_alloc), flight.divert.atc)
        except StopIteration:
            # Any remaining channels are nice-to-haves, but not necessary for
            # the few aircraft with a small number of channels available.
            pass

    @classmethod
    def from_cfg(cls, cfg: dict[str, Any]) -> CommonRadioChannelAllocator:
        return CommonRadioChannelAllocator(
            inter_flight_radio_index=cfg["inter_flight_radio_index"],
            intra_flight_radio_index=cfg["intra_flight_radio_index"],
        )

    @classmethod
    def name(cls) -> str:
        return "common"


@dataclass(frozen=True)
class NoOpChannelAllocator(RadioChannelAllocator):
    """Channel allocator for aircraft that don't support preset channels."""

    def assign_channels_for_flight(
        self, flight: FlightData, mission_data: MissionData
    ) -> None:
        pass

    @classmethod
    def name(cls) -> str:
        return "noop"


@dataclass(frozen=True)
class FarmerRadioChannelAllocator(RadioChannelAllocator):
    """Preset channel allocator for the MiG-19P."""

    def assign_channels_for_flight(
        self, flight: FlightData, mission_data: MissionData
    ) -> None:
        # The Farmer only has 6 preset channels. It also only has a VHF radio,
        # and currently our ATC data and AWACS are only in the UHF band.
        radio_id = 1
        flight.assign_channel(radio_id, 1, flight.intra_flight_channel)
        # TODO: Assign 4-6 to VHF frequencies of departure, arrival, and divert.
        # TODO: Assign 2 and 3 to AWACS if it is VHF.

    @classmethod
    def name(cls) -> str:
        return "farmer"


@dataclass(frozen=True)
class ViggenRadioChannelAllocator(RadioChannelAllocator):
    """Preset channel allocator for the AJS37."""

    def assign_channels_for_flight(
        self, flight: FlightData, mission_data: MissionData
    ) -> None:
        # The Viggen's preset channels are handled differently from other
        # aircraft. Since 2.7.9 the group channels will not be generated automatically
        # anymore. So we have to set AWACS and JTAC manually. There are also seven
        # special channels we can modify. We'll set the first channel of the main radio
        # to the intra-flight channel, and the first three emergency channels to each
        # of the flight plan's airfields. The fourth emergency channel is always
        # the guard channel.
        radio_id = 1

        # Possible Group Channels (100-139)
        channel_alloc = iter(range(1, 40))

        # Intra-Flight channel on Special 1 and Group 100 (required by module)
        flight.assign_channel(radio_id, 41, flight.intra_flight_channel)  # Special 1
        flight.assign_channel(
            radio_id, next(channel_alloc), flight.intra_flight_channel
        )

        for awacs in mission_data.awacs:
            flight.assign_channel(radio_id, next(channel_alloc), awacs.freq)

        for jtac in mission_data.jtacs:
            flight.assign_channel(radio_id, next(channel_alloc), jtac.freq)

        if flight.departure.atc is not None:
            flight.assign_channel(radio_id, 44, flight.departure.atc)  # FR24 E
        if flight.arrival.atc is not None:
            flight.assign_channel(radio_id, 45, flight.arrival.atc)  # FR24 F
        if flight.divert is not None and flight.divert.atc is not None:
            flight.assign_channel(radio_id, 46, flight.divert.atc)  # FR24 G

    @classmethod
    def name(cls) -> str:
        return "viggen"


@dataclass(frozen=True)
class SCR522RadioChannelAllocator(RadioChannelAllocator):
    """Preset channel allocator for the SCR522 WW2 radios. (4 channels)"""

    def assign_channels_for_flight(
        self, flight: FlightData, mission_data: MissionData
    ) -> None:
        radio_id = 1
        flight.assign_channel(radio_id, 1, flight.intra_flight_channel)
        if flight.departure.atc is not None:
            flight.assign_channel(radio_id, 2, flight.departure.atc)
        if flight.arrival.atc is not None:
            flight.assign_channel(radio_id, 3, flight.arrival.atc)

        # TODO : Some GCI on Channel 4 ?

    @classmethod
    def name(cls) -> str:
        return "SCR-522"


class ChannelNamer:
    """Base class allowing channel name customization per-aircraft.

    Most aircraft will want to customize this behavior, but the default is
    reasonable for any aircraft with numbered radios.
    """

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        """Returns the name of the channel for the given radio and channel."""
        return f"COMM{radio_id} Ch {channel_id}"

    @classmethod
    def name(cls) -> str:
        return "default"


class SingleRadioChannelNamer(ChannelNamer):
    """Channel namer for the aircraft with only a single radio.

    Aircraft like the MiG-19P and the MiG-21bis only have a single radio, so
    it's not necessary for us to name the radio when naming the channel.
    """

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        return f"Ch {channel_id}"

    @classmethod
    def name(cls) -> str:
        return "single"


class HueyChannelNamer(ChannelNamer):
    """Channel namer for the UH-1H."""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        return f"COM3 Ch {channel_id}"

    @classmethod
    def name(cls) -> str:
        return "huey"


class MirageChannelNamer(ChannelNamer):
    """Channel namer for the M-2000."""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        radio_name = ["V/UHF", "UHF"][radio_id - 1]
        return f"{radio_name} Ch {channel_id}"

    @classmethod
    def name(cls) -> str:
        return "mirage"


class MirageF1CEChannelNamer(ChannelNamer):
    """Channel namer for the Mirage-F1CE."""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        radio_name = ["V/UHF", "UHF"][radio_id - 1]
        return f"{radio_name} Ch {channel_id}"

    @classmethod
    def name(cls) -> str:
        return "mirage-f1CE"


class ApacheChannelNamer(ChannelNamer):
    """Channel namer for the AH-64D Apache"""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        # From the manual: Radio identifier (“VHF” for ARC-186, “UHF” for ARC-164,
        # “FM1” for first ARC-201D, “FM2” for second ARC-201D, or “HF” for ARC-220).
        radio_name = [
            "VHF",  # ARC-186
            "UHF",  # ARC-164
            "FM1",  # first ARC-201D
            "FM2",  # second ARC-201D
            "HF",  # ARC-220
        ][radio_id - 1]
        return f"{radio_name} Ch {channel_id}"

    @classmethod
    def name(cls) -> str:
        return "apache"


class TomcatChannelNamer(ChannelNamer):
    """Channel namer for the F-14."""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        radio_name = ["UHF", "VHF/UHF"][radio_id - 1]
        return f"{radio_name} Ch {channel_id}"

    @classmethod
    def name(cls) -> str:
        return "tomcat"


class ViggenChannelNamer(ChannelNamer):
    """Channel namer for the AJS37."""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        special_channels = [
            "FR 22 Special 1",
            "FR 22 Special 2",
            "FR 22 Special 3",
            "FR 24 E",
            "FR 24 F",
            "FR 24 G",
            "FR 24 H",
        ]
        if channel_id >= 41:  # Special channels are 41-47
            return special_channels[channel_id - 41]
        return f"FR 22 Group {99 + channel_id}"

    @classmethod
    def name(cls) -> str:
        return "viggen"


class ViperChannelNamer(ChannelNamer):
    """Channel namer for the F-16."""

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        return f"COM{radio_id} Ch {channel_id}"

    @classmethod
    def name(cls) -> str:
        return "viper"


class SCR522ChannelNamer(ChannelNamer):
    """
    Channel namer for P-51 & P-47D
    """

    @staticmethod
    def channel_name(radio_id: int, channel_id: int) -> str:
        if channel_id > 3:
            return "?"
        else:
            return f"Button " + "ABCD"[channel_id - 1]

    @classmethod
    def name(cls) -> str:
        return "SCR-522"
