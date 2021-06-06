from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Optional, Type

import dcs
import yaml
from dcs.helicopters import (
    AH_1W,
    AH_64A,
    AH_64D,
    Ka_50,
    Mi_24V,
    Mi_28N,
    Mi_8MT,
    OH_58D,
    SA342L,
    SA342M,
    SA342Minigun,
    SA342Mistral,
    SH_60B,
    UH_1H,
    UH_60A,
    helicopter_map,
)

from dcs.planes import (
    AV8BNA,
    A_10A,
    A_10C,
    A_10C_2,
    A_20G,
    Bf_109K_4,
    E_2C,
    FA_18C_hornet,
    FW_190A8,
    FW_190D9,
    F_14A_135_GR,
    F_14B,
    F_86F_Sabre,
    Ju_88A4,
    MiG_15bis,
    MiG_19P,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    P_51D,
    P_51D_30_NA,
    S_3B,
    S_3B_Tanker,
    SpitfireLFMkIX,
    SpitfireLFMkIXCW,
    Su_25,
    Su_25T,
    Su_33,
    plane_map,
)
from dcs.unittype import FlyingType

from game.db import PRICES
from game.factions.faction import unit_loader
from game.radio.channels import (
    RadioChannelAllocator,
    ChannelNamer,
    NoOpChannelAllocator,
    ViggenRadioChannelAllocator,
    ViggenChannelNamer,
    CommonRadioChannelAllocator,
    TomcatChannelNamer,
    ViperChannelNamer,
    MirageChannelNamer,
    FarmerRadioChannelAllocator,
    SingleRadioChannelNamer,
    SCR522ChannelNamer,
    HueyChannelNamer,
)
from gen.radios import get_radio, Radio
from pydcs_extensions.a4ec.a4ec import A_4E_C
from pydcs_extensions.mod_units import MODDED_AIRPLANES

THIS_DIR = Path(__file__).resolve().parent
SRC_ROOT = THIS_DIR.parent.parent
UNIT_DATA_DIR = SRC_ROOT / "resources/units"
FACTIONS_DIR = SRC_ROOT / "resources/factions"


# List of airframes that rely on their gun as a primary weapon. We confiscate bullets
# from most AI air-to-ground missions since they aren't smart enough to RTB when they're
# out of everything other than bullets (DCS does not have an all-but-gun winchester
# option) and we don't want to be attacking fully functional Tors with a Vulcan.
#
# These airframes are the exceptions. They probably should be using their gun regardless
# of the mission type.
GUN_RELIANT_AIRFRAMES: list[Type[FlyingType]] = [
    AH_1W,
    AH_64A,
    AH_64D,
    A_10A,
    A_10C,
    A_10C_2,
    A_20G,
    Bf_109K_4,
    FW_190A8,
    FW_190D9,
    F_86F_Sabre,
    Ju_88A4,
    Ka_50,
    MiG_15bis,
    MiG_19P,
    Mi_24V,
    Mi_28N,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    P_51D,
    P_51D_30_NA,
    SpitfireLFMkIX,
    SpitfireLFMkIXCW,
    Su_25,
    Su_25T,
]

CARRIER_CAPABLE = [
    FA_18C_hornet,
    F_14A_135_GR,
    F_14B,
    AV8BNA,
    Su_33,
    A_4E_C,
    S_3B,
    S_3B_Tanker,
    E_2C,
    UH_1H,
    Mi_8MT,
    Ka_50,
    AH_1W,
    OH_58D,
    UH_60A,
    SH_60B,
    SA342L,
    SA342M,
    SA342Minigun,
    SA342Mistral,
]

LHA_CAPABLE = [
    AV8BNA,
    UH_1H,
    Mi_8MT,
    Ka_50,
    AH_1W,
    OH_58D,
    UH_60A,
    SH_60B,
    SA342L,
    SA342M,
    SA342Minigun,
    SA342Mistral,
]


@dataclass(frozen=True)
class AircraftData:
    """Additional aircraft data not exposed by pydcs."""

    #: The type of radio used for inter-flight communications.
    inter_flight_radio: Radio

    #: The type of radio used for intra-flight communications.
    intra_flight_radio: Radio

    #: The radio preset channel allocator, if the aircraft supports channel
    #: presets. If the aircraft does not support preset channels, this will be
    #: None.
    channel_allocator: Optional[RadioChannelAllocator]

    #: Defines how channels should be named when printed in the kneeboard.
    channel_namer: Type[ChannelNamer] = ChannelNamer


# Indexed by the id field of the pydcs PlaneType.
AIRCRAFT_DATA: dict[str, AircraftData] = {
    "A-10C": AircraftData(
        inter_flight_radio=get_radio("AN/ARC-164"),
        # VHF for intraflight is not accepted anymore by DCS
        # (see https://forums.eagle.ru/showthread.php?p=4499738).
        intra_flight_radio=get_radio("AN/ARC-164"),
        channel_allocator=NoOpChannelAllocator(),
    ),
    "AJS37": AircraftData(
        # The AJS37 has somewhat unique radio configuration. Two backup radio
        # (FR 24) can only operate simultaneously with the main radio in guard
        # mode. As such, we only use the main radio for both inter- and intra-
        # flight communication.
        inter_flight_radio=get_radio("FR 22"),
        intra_flight_radio=get_radio("FR 22"),
        channel_allocator=ViggenRadioChannelAllocator(),
        channel_namer=ViggenChannelNamer,
    ),
    "AV8BNA": AircraftData(
        inter_flight_radio=get_radio("AN/ARC-210"),
        intra_flight_radio=get_radio("AN/ARC-210"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=2, intra_flight_radio_index=1
        ),
    ),
    "F-14B": AircraftData(
        inter_flight_radio=get_radio("AN/ARC-159"),
        intra_flight_radio=get_radio("AN/ARC-182"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=2
        ),
        channel_namer=TomcatChannelNamer,
    ),
    "F-16C_50": AircraftData(
        inter_flight_radio=get_radio("AN/ARC-164"),
        intra_flight_radio=get_radio("AN/ARC-222"),
        # COM2 is the AN/ARC-222, which is the VHF radio we want to use for
        # intra-flight communication to leave COM1 open for UHF inter-flight.
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=2
        ),
        channel_namer=ViperChannelNamer,
    ),
    "JF-17": AircraftData(
        inter_flight_radio=get_radio("R&S M3AR UHF"),
        intra_flight_radio=get_radio("R&S M3AR VHF"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=1
        ),
        # Same naming pattern as the Viper, so just reuse that.
        channel_namer=ViperChannelNamer,
    ),
    "Ka-50": AircraftData(
        inter_flight_radio=get_radio("R-800L1"),
        intra_flight_radio=get_radio("R-800L1"),
        # The R-800L1 doesn't have preset channels, and the other radio is for
        # communications with FAC and ground units, which don't currently have
        # radios assigned, so no channels to configure.
        channel_allocator=NoOpChannelAllocator(),
    ),
    "M-2000C": AircraftData(
        inter_flight_radio=get_radio("TRT ERA 7000 V/UHF"),
        intra_flight_radio=get_radio("TRT ERA 7200 UHF"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=2
        ),
        channel_namer=MirageChannelNamer,
    ),
    "MiG-15bis": AircraftData(
        inter_flight_radio=get_radio("RSI-6K HF"),
        intra_flight_radio=get_radio("RSI-6K HF"),
        channel_allocator=NoOpChannelAllocator(),
    ),
    "MiG-19P": AircraftData(
        inter_flight_radio=get_radio("RSIU-4V"),
        intra_flight_radio=get_radio("RSIU-4V"),
        channel_allocator=FarmerRadioChannelAllocator(),
        channel_namer=SingleRadioChannelNamer,
    ),
    "MiG-21Bis": AircraftData(
        inter_flight_radio=get_radio("RSIU-5V"),
        intra_flight_radio=get_radio("RSIU-5V"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=1
        ),
        channel_namer=SingleRadioChannelNamer,
    ),
    "P-51D": AircraftData(
        inter_flight_radio=get_radio("SCR522"),
        intra_flight_radio=get_radio("SCR522"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=1
        ),
        channel_namer=SCR522ChannelNamer,
    ),
    "UH-1H": AircraftData(
        inter_flight_radio=get_radio("AN/ARC-51BX"),
        # Ideally this would use the AN/ARC-131 because that radio is supposed
        # to be used for flight comms, but DCS won't allow it as the flight's
        # frequency, nor will it allow the AN/ARC-134.
        intra_flight_radio=get_radio("AN/ARC-51BX"),
        channel_allocator=CommonRadioChannelAllocator(
            inter_flight_radio_index=1, intra_flight_radio_index=1
        ),
        channel_namer=HueyChannelNamer,
    ),
    "F-22A": AircraftData(
        inter_flight_radio=get_radio("SCR-522"),
        intra_flight_radio=get_radio("SCR-522"),
        channel_allocator=None,
        channel_namer=SCR522ChannelNamer,
    ),
    "JAS39Gripen": AircraftData(
        inter_flight_radio=get_radio("R&S Series 6000"),
        intra_flight_radio=get_radio("R&S Series 6000"),
        channel_allocator=None,
    ),
}
AIRCRAFT_DATA["A-10C_2"] = AIRCRAFT_DATA["A-10C"]
AIRCRAFT_DATA["P-51D-30-NA"] = AIRCRAFT_DATA["P-51D"]
AIRCRAFT_DATA["P-47D-30"] = AIRCRAFT_DATA["P-51D"]
AIRCRAFT_DATA["JAS39Gripen_AG"] = AIRCRAFT_DATA["JAS39Gripen"]


class Converter:
    def __init__(self) -> None:
        self.all_variants: set[str] = set()
        self.variant_map: dict[str, dict[str, str]] = {}
        self.unconverted: set[Type[FlyingType]] = set(
            k for k in PRICES if issubclass(k, FlyingType)
        )

    @staticmethod
    def find_unit_id_for_faction_name(name: str) -> str:
        unit_type = unit_loader(name, [dcs.planes, dcs.helicopters, MODDED_AIRPLANES])
        if unit_type is None:
            raise KeyError(f"Found no unit named {name}")
        return unit_type.id

    def convert(self) -> None:
        data_path = UNIT_DATA_DIR / "unit_info_text.json"
        with data_path.open(encoding="utf-8") as unit_data_file:
            unit_data = json.load(unit_data_file)

        for unit_name, data in dict(unit_data).items():
            if self.convert_unit(unit_name, data):
                unit_data.pop(unit_name)

        with data_path.open("w", encoding="utf-8") as unit_data_file:
            json.dump(unit_data, unit_data_file, indent=2)

        for unconverted in self.unconverted:
            self.generate_basic_info(unconverted)

        for faction_path in FACTIONS_DIR.glob("*.json"):
            self.update_faction(faction_path)

    def update_faction(self, faction_path: Path) -> None:
        with faction_path.open() as faction_file:
            data = json.load(faction_file)

        self.update_aircraft_list(data, "aircrafts")
        self.update_aircraft_list(data, "awacs")
        self.update_aircraft_list(data, "tankers")
        self.update_aircraft_item(data, "jtac_unit")

        if "liveries_overrides" in data:
            new_liveries = {}
            for aircraft, liveries in data["liveries_overrides"].items():
                name = self.new_name_for(aircraft, data["country"])
                new_liveries[name] = sorted(liveries)
            data["liveries_overrides"] = new_liveries

        with faction_path.open("w") as faction_file:
            json.dump(data, faction_file, indent=2)

    def new_name_for(self, old_name: str, country: str) -> str:
        if old_name in self.all_variants:
            return old_name
        aircraft_id = self.find_unit_id_for_faction_name(old_name)
        return self.variant_map[aircraft_id][country]

    def update_aircraft_list(self, data: dict[str, Any], field: str) -> None:
        if field not in data:
            return

        new_aircraft = []
        for aircraft in data[field]:
            new_aircraft.append(self.new_name_for(aircraft, data["country"]))
        data[field] = sorted(new_aircraft)

    def update_aircraft_item(self, data: dict[str, Any], field: str) -> None:
        if field in data:
            aircraft_name = data[field]
            data[field] = self.new_name_for(aircraft_name, data["country"])

    def generate_basic_info(self, unit_type: Type[FlyingType]) -> None:
        self.all_variants.add(unit_type.id)
        output_path = UNIT_DATA_DIR / "aircraft" / f"{unit_type.id}.yaml"
        if output_path.exists():
            # Already have data for this, don't clobber it, but do register the
            # variant names.
            with output_path.open() as unit_info_file:
                data = yaml.safe_load(unit_info_file)
                self.all_variants.update(data["variants"].keys())
            return
        with output_path.open("w") as output_file:
            yaml.safe_dump(
                {
                    "price": PRICES[unit_type],
                    "variants": {unit_type.id: None},
                },
                output_file,
            )

        self.variant_map[unit_type.id] = defaultdict(lambda: unit_type.id)

    def convert_unit(
        self, pydcs_name: str, data: list[dict[str, dict[str, str]]]
    ) -> bool:
        if len(data) != 1:
            raise ValueError(f"Unexpected data format for {pydcs_name}")

        unit_type: Type[FlyingType]
        if pydcs_name in plane_map:
            unit_type = plane_map[pydcs_name]
        elif pydcs_name in helicopter_map:
            unit_type = helicopter_map[pydcs_name]
        else:
            return False

        self.unconverted.remove(unit_type)

        variants_dict = data[0]
        default = variants_dict.pop("default")

        default_name = default["name"]
        self.all_variants.add(default_name)
        country_to_variant = defaultdict(lambda: default_name)

        variants = {default_name: {}}
        for country, variant_dict in variants_dict.items():
            variant_name = variant_dict["name"]
            self.all_variants.add(variant_name)
            country_to_variant[country] = variant_name
            variants[variant_name] = self.get_variant_data(variant_dict)

        output_dict: dict[str, Any] = {"variants": variants, "price": PRICES[unit_type]}
        output_dict.update(self.get_variant_data(default))

        if unit_type in CARRIER_CAPABLE:
            output_dict["carrier_capable"] = True
        if unit_type in LHA_CAPABLE:
            output_dict["lha_capable"] = True
        if unit_type in GUN_RELIANT_AIRFRAMES:
            output_dict["always_keeps_gun"] = True

        try:
            aircraft_data = AIRCRAFT_DATA[unit_type.id]
            radio_dict: dict[str, Any] = {
                "intra_flight": aircraft_data.intra_flight_radio.name,
                "inter_flight": aircraft_data.inter_flight_radio.name,
            }
            channels_dict: dict[str, Any] = {}
            if type(aircraft_data.channel_namer) != ChannelNamer:
                channels_dict["namer"] = aircraft_data.channel_namer.name()
            if aircraft_data.channel_allocator is not None:
                alloc = aircraft_data.channel_allocator
                if alloc.name() != "noop":
                    channels_dict["type"] = alloc.name()
                    if isinstance(alloc, CommonRadioChannelAllocator):
                        channels_dict[
                            "intra_flight_radio_index"
                        ] = alloc.intra_flight_radio_index
                        channels_dict[
                            "inter_flight_radio_index"
                        ] = alloc.inter_flight_radio_index
            if channels_dict:
                radio_dict["channels"] = channels_dict
        except KeyError:
            pass

        output_path = UNIT_DATA_DIR / "aircraft" / f"{unit_type.id}.yaml"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w") as output_file:
            yaml.safe_dump(output_dict, output_file)

        self.variant_map[pydcs_name] = country_to_variant
        return True

    @staticmethod
    def get_variant_data(variant: dict[str, Any]) -> dict[str, Any]:
        result = {}

        try:
            result["manufacturer"] = variant["manufacturer"]
        except KeyError:
            pass

        try:
            result["origin"] = variant["country-of-origin"]
        except KeyError:
            pass
        try:
            result["role"] = variant["role"]
        except KeyError:
            pass

        try:
            as_str = variant["year-of-variant-introduction"]
            if as_str == "N/A":
                result["introduced"] = None
            else:
                result["introduced"] = int(as_str)
        except KeyError:
            pass

        try:
            result["description"] = variant["text"]
        except KeyError:
            pass

        return result


if __name__ == "__main__":
    Converter().convert()
