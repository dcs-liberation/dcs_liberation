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
from dcs.mission import Mission
from dcs.unittype import FlyingType
from tabulate import tabulate

from . import units
from .aircraft import FlightData
from .airfields import RunwayData
from .airsupportgen import AwacsInfo, TankerInfo
from .briefinggen import CommInfo, JtacInfo, MissionInfoGenerator
from .flights.flight import FlightWaypoint, FlightWaypointType
from .radios import RadioFrequency


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


@dataclass(frozen=True)
class NumberedWaypoint:
    number: int
    waypoint: FlightWaypoint


class FlightPlanBuilder:
    def __init__(self) -> None:
        self.rows: List[List[str]] = []
        self.target_points: List[NumberedWaypoint] = []

    def add_waypoint(self, waypoint_num: int, waypoint: FlightWaypoint) -> None:
        if waypoint.waypoint_type == FlightWaypointType.TARGET_POINT:
            self.target_points.append(NumberedWaypoint(waypoint_num, waypoint))
            return

        if self.target_points:
            self.coalesce_target_points()
            self.target_points = []

        self.add_waypoint_row(NumberedWaypoint(waypoint_num, waypoint))

    def coalesce_target_points(self) -> None:
        if len(self.target_points) <= 4:
            for steerpoint in self.target_points:
                self.add_waypoint_row(steerpoint)
            return

        first_waypoint_num = self.target_points[0].number
        last_waypoint_num = self.target_points[-1].number

        self.rows.append([
            f"{first_waypoint_num}-{last_waypoint_num}",
            "Target points",
            "0"
        ])

    def add_waypoint_row(self, waypoint: NumberedWaypoint) -> None:
        self.rows.append([
            waypoint.number,
            waypoint.waypoint.pretty_name,
            str(int(units.meters_to_feet(waypoint.waypoint.alt)))
        ])

    def build(self) -> List[List[str]]:
        return self.rows


class BriefingPage(KneeboardPage):
    """A kneeboard page containing briefing information."""
    def __init__(self, flight: FlightData, comms: List[CommInfo],
                 awacs: List[AwacsInfo], tankers: List[TankerInfo],
                 jtacs: List[JtacInfo]) -> None:
        self.flight = flight
        self.comms = list(comms)
        self.awacs = awacs
        self.tankers = tankers
        self.jtacs = jtacs
        self.comms.append(CommInfo("Flight", self.flight.intra_flight_channel))

    def write(self, path: Path) -> None:
        writer = KneeboardPageWriter()
        writer.title(f"{self.flight.callsign} Mission Info")

        # TODO: Handle carriers.
        writer.heading("Airfield Info")
        writer.table([
            self.airfield_info_row("Departure", self.flight.departure),
            self.airfield_info_row("Arrival", self.flight.arrival),
            self.airfield_info_row("Divert", self.flight.divert),
        ], headers=["", "Airbase", "ATC", "TCN", "I(C)LS", "RWY"])

        writer.heading("Flight Plan")
        flight_plan_builder = FlightPlanBuilder()
        for num, waypoint in enumerate(self.flight.waypoints):
            flight_plan_builder.add_waypoint(num, waypoint)
        writer.table(flight_plan_builder.build(),
                     headers=["STPT", "Action", "Alt"])

        writer.heading("Comm Ladder")
        comms = []
        for comm in self.comms:
            comms.append([comm.name, self.format_frequency(comm.freq)])
        writer.table(comms, headers=["Name", "UHF"])

        writer.heading("AWACS")
        awacs = []
        for a in self.awacs:
            awacs.append([a.callsign, self.format_frequency(a.freq)])
        writer.table(awacs, headers=["Callsign", "UHF"])

        writer.heading("Tankers")
        tankers = []
        for tanker in self.tankers:
            tankers.append([
                tanker.callsign,
                tanker.variant,
                tanker.tacan,
                self.format_frequency(tanker.freq),
            ])
        writer.table(tankers, headers=["Callsign", "Type", "TACAN", "UHF"])

        writer.heading("JTAC")
        jtacs = []
        for jtac in self.jtacs:
            jtacs.append([jtac.callsign, jtac.region, jtac.code])
        writer.table(jtacs, headers=["Callsign", "Region", "Laser Code"])

        writer.write(path)

    def airfield_info_row(self, row_title: str,
                          runway: Optional[RunwayData]) -> List[str]:
        """Creates a table row for a given airfield.

        Args:
            row_title: Purpose of the airfield. e.g. "Departure", "Arrival" or
                "Divert".
            runway: The runway described by this row.

        Returns:
            A list of strings to be used as a row of the airfield table.
        """
        if runway is None:
            return [row_title, "", "", "", "", ""]

        atc = ""
        if runway.atc is not None:
            atc = self.format_frequency(runway.atc)
        return [
            row_title,
            runway.airfield_name,
            atc,
            runway.tacan or "",
            runway.ils or runway.icls or "",
            runway.runway_name,
        ]

    def format_frequency(self, frequency: RadioFrequency) -> str:
        channel = self.flight.channel_for(frequency)
        if channel is None:
            return str(frequency)
        return f"{channel.radio_name} Ch {channel.channel}"


class KneeboardGenerator(MissionInfoGenerator):
    """Creates kneeboard pages for each client flight in the mission."""

    def __init__(self, mission: Mission) -> None:
        super().__init__(mission)

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
        for flight in self.flights:
            if not flight.client_units:
                continue
            all_flights[flight.aircraft_type].extend(
                self.generate_flight_kneeboard(flight))
        return all_flights

    def generate_flight_kneeboard(self, flight: FlightData) -> List[KneeboardPage]:
        """Returns a list of kneeboard pages for the given flight."""
        return [
            BriefingPage(
                flight, self.comms, self.awacs, self.tankers, self.jtacs
            ),
        ]
