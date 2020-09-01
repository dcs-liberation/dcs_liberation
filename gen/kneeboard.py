"""Generates kneeboard pages relevant to the player's mission.

The player kneeboard includes the following information:

* Airfield (departure, arrival, divert) info.
* Flight plan (waypoint numbers, names, altitudes).
* Comm channels.
* AWACS info.
* Tanker info.
* JTAC info.

Things we should add:

* Flight plan ToT and fuel ladder (current have neither available).
* Support for planning an arrival/divert airfield separate from departure.
* Mission package infrastructure to include information about the larger
  mission, i.e. information about the escort flight for a strike package.
* Target information. Steerpoints, preplanned objectives, ToT, etc.

For multiplayer missions, a kneeboard will be generated per flight.
https://forums.eagle.ru/showthread.php?t=206360 claims that kneeboard pages can
only be added per airframe, so PvP missions where each side have the same
aircraft will be able to see the enemy's kneeboard for the same airframe.
"""
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
from tabulate import tabulate

from pydcs.dcs.mission import Mission
from pydcs.dcs.terrain.terrain import Airport
from pydcs.dcs.unittype import FlyingType
from .airfields import AIRFIELD_DATA
from .flights.flight import Flight
from . import units


class KneeboardPageWriter:
    """Creates kneeboard images."""

    def __init__(self, page_margin: int = 24, line_spacing: int = 12) -> None:
        self.image = Image.new('RGB', (768, 1024), (0xff, 0xff, 0xff))
        # These font sizes create a relatively full page for current sorties. If
        # we start generating more complicated flight plans, or start including
        # more information in the comm ladder (the latter of which we should
        # probably do), we'll need to split some of this information off into a
        # second page.
        self.title_font = ImageFont.truetype("arial.ttf", 32)
        self.heading_font = ImageFont.truetype("arial.ttf", 24)
        self.content_font = ImageFont.truetype("arial.ttf", 20)
        self.table_font = ImageFont.truetype(
            "resources/fonts/Inconsolata.otf", 20)
        self.draw = ImageDraw.Draw(self.image)
        self.x = page_margin
        self.y = page_margin
        self.line_spacing = line_spacing

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    def text(self, text: str, font=None,
             fill: Tuple[int, int, int] = (0, 0, 0)) -> None:
        if font is None:
            font = self.content_font

        self.draw.text(self.position, text, font=font, fill=fill)
        width, height = self.draw.textsize(text, font=font)
        self.y += height + self.line_spacing

    def title(self, title: str) -> None:
        self.text(title, font=self.title_font)

    def heading(self, text: str) -> None:
        self.text(text, font=self.heading_font)

    def table(self, cells: List[List[str]],
              headers: Optional[List[str]] = None) -> None:
        table = tabulate(cells, headers=headers, numalign="right")
        self.text(table, font=self.table_font)

    def write(self, path: Path) -> None:
        self.image.save(path)


class KneeboardPage:
    """Base class for all kneeboard pages."""

    def write(self, path: Path) -> None:
        """Writes the kneeboard page to the given path."""
        raise NotImplementedError


class AirfieldInfo:
    def __init__(self, airfield: Airport) -> None:
        self.airport = airfield
        # TODO: Implement logic for picking preferred runway.
        runway = airfield.runways[0]
        runway_side = ["", "L", "R"][runway.leftright]
        self.runway = f"{runway.heading}{runway_side}"
        try:
            extra_data = AIRFIELD_DATA[airfield.name]
            self.atc = extra_data.atc.uhf or ""
            self.tacan = extra_data.tacan or ""
            self.ils = extra_data.ils_freq(self.runway) or ""
        except KeyError:
            self.atc = ""
            self.ils = ""
            self.tacan = ""


@dataclass
class CommInfo:
    """Communications information for the kneeboard."""
    name: str
    freq: str


@dataclass
class AwacsInfo:
    """AWACS information for the kneeboard."""
    callsign: str
    freq: str


@dataclass
class TankerInfo:
    """Tanker information for the kneeboard."""
    callsign: str
    variant: str
    freq: str
    tacan: str


@dataclass
class JtacInfo:
    """JTAC information for the kneeboard."""
    callsign: str
    region: str
    code: str


class BriefingPage(KneeboardPage):
    """A kneeboard page containing briefing information."""
    def __init__(self, flight: Flight, comms: List[CommInfo],
                 awacs: List[AwacsInfo], tankers: List[TankerInfo],
                 jtacs: List[JtacInfo]) -> None:
        self.flight = flight
        self.comms = comms
        self.awacs = awacs
        self.tankers = tankers
        self.jtacs = jtacs
        self.departure = flight.from_cp.airport
        self.arrival = flight.from_cp.airport
        self.divert: Optional[Airport] = None

    def write(self, path: Path) -> None:
        writer = KneeboardPageWriter()
        # TODO: Assign callsigns to flights and include that info.
        # https://github.com/Khopa/dcs_liberation/issues/113
        writer.title(f"Mission Info")

        # TODO: Handle carriers.
        writer.heading("Airfield Info")
        writer.table([
            self.airfield_info_row("Departure", self.departure),
            self.airfield_info_row("Arrival", self.arrival),
            self.airfield_info_row("Divert", self.divert),
        ], headers=["", "Airbase", "ATC", "TCN", "ILS", "RWY"])

        writer.heading("Flight Plan")
        flight_plan = []
        for num, waypoint in enumerate(self.flight.points):
            alt = int(units.meters_to_feet(waypoint.alt))
            flight_plan.append([num, waypoint.pretty_name, str(alt)])
        writer.table(flight_plan, headers=["STPT", "Action", "Alt"])

        writer.heading("Comm Ladder")
        comms = []
        for comm in self.comms:
            comms.append([comm.name, comm.freq])
        writer.table(comms, headers=["Name", "UHF"])

        writer.heading("AWACS")
        awacs = []
        for a in self.awacs:
            awacs.append([a.callsign, a.freq])
        writer.table(awacs, headers=["Callsign", "UHF"])

        writer.heading("Tankers")
        tankers = []
        for tanker in self.tankers:
            tankers.append([
                tanker.callsign,
                tanker.variant,
                tanker.tacan,
                tanker.freq,
            ])
        writer.table(tankers, headers=["Callsign", "Type", "TACAN", "UHF"])

        writer.heading("JTAC")
        jtacs = []
        for jtac in self.jtacs:
            jtacs.append([jtac.callsign, jtac.region, jtac.code])
        writer.table(jtacs, headers=["Callsign", "Region", "Laser Code"])

        writer.write(path)

    def airfield_info_row(self, row_title: str,
                          airfield: Optional[Airport]) -> List[str]:
        """Creates a table row for a given airfield.

        Args:
            row_title: Purpose of the airfield. e.g. "Departure", "Arrival" or
                "Divert".
            airfield: The airfield described by this row.

        Returns:
            A list of strings to be used as a row of the airfield table.
        """
        if airfield is None:
            return [row_title, "", "", "", "", ""]
        info = AirfieldInfo(airfield)
        return [
            row_title,
            airfield.name,
            info.atc,
            info.tacan,
            info.ils,
            info.runway,
        ]


class KneeboardGenerator:
    """Creates kneeboard pages for each client flight in the mission."""

    def __init__(self, mission: Mission, game) -> None:
        self.mission = mission
        self.game = game
        self.comms: List[CommInfo] = []
        self.awacs: List[AwacsInfo] = []
        self.tankers: List[TankerInfo] = []
        self.jtacs: List[JtacInfo] = []

    def add_comm(self, name: str, freq: str) -> None:
        """Adds communications info to the kneeboard.

        Args:
            name: Name of the radio channel.
            freq: Frequency of the radio channel.
        """
        self.comms.append(CommInfo(name, freq))

    def add_awacs(self, callsign: str, freq: str) -> None:
        """Adds an AWACS/GCI to the kneeboard.

        Args:
            callsign: Callsign of the AWACS/GCI.
            freq: Radio frequency used by the AWACS/GCI.
        """
        self.awacs.append(AwacsInfo(callsign, freq))

    def add_tanker(self, callsign: str, variant: str, freq: str,
                   tacan: str) -> None:
        """Adds a tanker to the kneeboard.

        Args:
            callsign: Callsign of the tanker.
            variant: Aircraft type.
            freq: Radio frequency used by the tanker.
            tacan: TACAN channel of the tanker.
        """
        self.tankers.append(TankerInfo(callsign, variant, freq, tacan))

    def add_jtac(self, callsign: str, region: str, code: str) -> None:
        """Adds a JTAC to the kneeboard.

        Args:
            callsign: Callsign of the JTAC.
            region: JTAC's area of responsibility.
            code: Laser code used by the JTAC.
        """
        # TODO: Radio info? Type?
        self.jtacs.append(JtacInfo(callsign, region, code))

    def generate(self) -> None:
        """Generates a kneeboard per client flight."""
        temp_dir = Path("kneeboards")
        temp_dir.mkdir(exist_ok=True)
        for aircraft, pages in self.pages_by_airframe().items():
            aircraft_dir = temp_dir / aircraft.id
            aircraft_dir.mkdir(exist_ok=True)
            for idx, page in enumerate(pages):
                page_path = aircraft_dir / f"page{idx:02}.png"
                page.write(page_path)
                self.mission.add_aircraft_kneeboard(aircraft, page_path)

    def pages_by_airframe(self) -> Dict[FlyingType, List[KneeboardPage]]:
        """Returns a list of kneeboard pages per airframe in the mission.

        Only client flights will be included, but because DCS does not support
        group-specific kneeboard pages, flights (possibly from opposing sides)
        will be able to see the kneeboards of all aircraft of the same type.

        Returns:
            A dict mapping aircraft types to the list of kneeboard pages for
            that aircraft.
        """
        all_flights: Dict[FlyingType, List[KneeboardPage]] = defaultdict(list)
        for cp in self.game.theater.controlpoints:
            if cp.id in self.game.planners.keys():
                for flight in self.game.planners[cp.id].flights:
                    if flight.client_count > 0:
                        all_flights[flight.unit_type].extend(
                            self.generate_flight_kneeboard(flight))
        return all_flights

    def generate_flight_kneeboard(self, flight: Flight) -> List[KneeboardPage]:
        """Returns a list of kneeboard pages for the given flight."""
        return [
            BriefingPage(
                flight, self.comms, self.awacs, self.tankers, self.jtacs
            ),
        ]
