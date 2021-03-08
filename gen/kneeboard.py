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
import datetime
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING, Tuple

from PIL import Image, ImageDraw, ImageFont
from dcs.mission import Mission
from dcs.unittype import FlyingType
from tabulate import tabulate

from game.utils import meters
from .aircraft import AIRCRAFT_DATA, FlightData
from .airsupportgen import AwacsInfo, TankerInfo
from .briefinggen import CommInfo, JtacInfo, MissionInfoGenerator
from .flights.flight import FlightWaypoint, FlightWaypointType
from .radios import RadioFrequency
from .runways import RunwayData


if TYPE_CHECKING:
    from game import Game


class KneeboardPageWriter:
    """Creates kneeboard images."""

    def __init__(self, page_margin: int = 24, line_spacing: int = 12) -> None:
        self.image = Image.new("RGB", (768, 1024), (0xFF, 0xFF, 0xFF))
        # These font sizes create a relatively full page for current sorties. If
        # we start generating more complicated flight plans, or start including
        # more information in the comm ladder (the latter of which we should
        # probably do), we'll need to split some of this information off into a
        # second page.
        self.title_font = ImageFont.truetype("arial.ttf", 32)
        self.heading_font = ImageFont.truetype("arial.ttf", 24)
        self.content_font = ImageFont.truetype("arial.ttf", 20)
        self.table_font = ImageFont.truetype("resources/fonts/Inconsolata.otf", 20)
        self.draw = ImageDraw.Draw(self.image)
        self.x = page_margin
        self.y = page_margin
        self.line_spacing = line_spacing

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y

    def text(
        self, text: str, font=None, fill: Tuple[int, int, int] = (0, 0, 0)
    ) -> None:
        if font is None:
            font = self.content_font

        self.draw.text(self.position, text, font=font, fill=fill)
        width, height = self.draw.textsize(text, font=font)
        self.y += height + self.line_spacing

    def title(self, title: str) -> None:
        self.text(title, font=self.title_font)

    def heading(self, text: str) -> None:
        self.text(text, font=self.heading_font)

    def table(
        self, cells: List[List[str]], headers: Optional[List[str]] = None
    ) -> None:
        if headers is None:
            headers = []
        table = tabulate(cells, headers=headers, numalign="right")
        self.text(table, font=self.table_font)

    def write(self, path: Path) -> None:
        self.image.save(path)

    @staticmethod
    def wrap_line(inputstr: str, max_length: int) -> str:
        if len(inputstr) <= max_length:
            return inputstr
        tokens = inputstr.split(" ")
        output = ""
        segments = []
        for token in tokens:
            combo = output + " " + token
            if len(combo) > max_length:
                combo = output + "\n" + token
                segments.append(combo)
                output = ""
            else:
                output = combo
        return "".join(segments + [output]).strip()


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

    WAYPOINT_DESC_MAX_LEN = 25

    def __init__(self, start_time: datetime.datetime) -> None:
        self.start_time = start_time
        self.rows: List[List[str]] = []
        self.target_points: List[NumberedWaypoint] = []
        self.last_waypoint: Optional[FlightWaypoint] = None

    def add_waypoint(self, waypoint_num: int, waypoint: FlightWaypoint) -> None:
        if waypoint.waypoint_type == FlightWaypointType.TARGET_POINT:
            self.target_points.append(NumberedWaypoint(waypoint_num, waypoint))
            return

        if self.target_points:
            self.coalesce_target_points()
            self.target_points = []

        self.add_waypoint_row(NumberedWaypoint(waypoint_num, waypoint))
        self.last_waypoint = waypoint

    def coalesce_target_points(self) -> None:
        if len(self.target_points) <= 4:
            for steerpoint in self.target_points:
                self.add_waypoint_row(steerpoint)
            return

        first_waypoint_num = self.target_points[0].number
        last_waypoint_num = self.target_points[-1].number

        self.rows.append(
            [
                f"{first_waypoint_num}-{last_waypoint_num}",
                "Target points",
                "0",
                self._waypoint_distance(self.target_points[0].waypoint),
                self._ground_speed(self.target_points[0].waypoint),
                self._format_time(self.target_points[0].waypoint.tot),
                self._format_time(self.target_points[0].waypoint.departure_time),
            ]
        )
        self.last_waypoint = self.target_points[-1].waypoint

    def add_waypoint_row(self, waypoint: NumberedWaypoint) -> None:
        self.rows.append(
            [
                str(waypoint.number),
                KneeboardPageWriter.wrap_line(
                    waypoint.waypoint.pretty_name,
                    FlightPlanBuilder.WAYPOINT_DESC_MAX_LEN,
                ),
                str(int(waypoint.waypoint.alt.feet)),
                self._waypoint_distance(waypoint.waypoint),
                self._ground_speed(waypoint.waypoint),
                self._format_time(waypoint.waypoint.tot),
                self._format_time(waypoint.waypoint.departure_time),
            ]
        )

    def _format_time(self, time: Optional[datetime.timedelta]) -> str:
        if time is None:
            return ""
        local_time = self.start_time + time
        return local_time.strftime(f"%H:%M:%S")

    def _waypoint_distance(self, waypoint: FlightWaypoint) -> str:
        if self.last_waypoint is None:
            return "-"

        distance = meters(
            self.last_waypoint.position.distance_to_point(waypoint.position)
        )
        return f"{distance.nautical_miles:.1f} NM"

    def _ground_speed(self, waypoint: FlightWaypoint) -> str:
        if self.last_waypoint is None:
            return "-"

        if waypoint.tot is None:
            return "-"

        if self.last_waypoint.departure_time is not None:
            last_time = self.last_waypoint.departure_time
        elif self.last_waypoint.tot is not None:
            last_time = self.last_waypoint.tot
        else:
            return "-"

        distance = meters(
            self.last_waypoint.position.distance_to_point(waypoint.position)
        )
        duration = (waypoint.tot - last_time).total_seconds() / 3600
        return f"{int(distance.nautical_miles / duration)} kt"

    def build(self) -> List[List[str]]:
        return self.rows


class BriefingPage(KneeboardPage):
    """A kneeboard page containing briefing information."""

    def __init__(
        self,
        flight: FlightData,
        comms: List[CommInfo],
        awacs: List[AwacsInfo],
        tankers: List[TankerInfo],
        jtacs: List[JtacInfo],
        start_time: datetime.datetime,
    ) -> None:
        self.flight = flight
        self.comms = list(comms)
        self.awacs = awacs
        self.tankers = tankers
        self.jtacs = jtacs
        self.start_time = start_time
        self.comms.append(CommInfo("Flight", self.flight.intra_flight_channel))

    def write(self, path: Path) -> None:
        writer = KneeboardPageWriter()
        if self.flight.custom_name is not None:
            custom_name_title = ' ("{}")'.format(self.flight.custom_name)
        else:
            custom_name_title = ""
        writer.title(f"{self.flight.callsign} Mission Info{custom_name_title}")

        # TODO: Handle carriers.
        writer.heading("Airfield Info")
        writer.table(
            [
                self.airfield_info_row("Departure", self.flight.departure),
                self.airfield_info_row("Arrival", self.flight.arrival),
                self.airfield_info_row("Divert", self.flight.divert),
            ],
            headers=["", "Airbase", "ATC", "TCN", "I(C)LS", "RWY"],
        )

        writer.heading("Flight Plan")
        flight_plan_builder = FlightPlanBuilder(self.start_time)
        for num, waypoint in enumerate(self.flight.waypoints):
            flight_plan_builder.add_waypoint(num, waypoint)
        writer.table(
            flight_plan_builder.build(),
            headers=["#", "Action", "Alt", "Dist", "GSPD", "Time", "Departure"],
        )

        flight_plan_builder
        writer.table(
            [
                [
                    "{}lbs".format(self.flight.bingo_fuel),
                    "{}lbs".format(self.flight.joker_fuel),
                ]
            ],
            ["Bingo", "Joker"],
        )

        # AEW&C
        writer.heading("AEW&C")
        aewc_ladder = []

        for single_aewc in self.awacs:

            if single_aewc.depature_location is None:
                dep = "-"
                arr = "-"
            else:
                dep = self._format_time(single_aewc.start_time)
                arr = self._format_time(single_aewc.end_time)

            aewc_ladder.append(
                [
                    str(single_aewc.callsign),
                    str(single_aewc.freq),
                    str(single_aewc.depature_location),
                    str(dep),
                    str(arr),
                ]
            )

        writer.table(
            aewc_ladder,
            headers=["Callsign", "FREQ", "Depature", "ETD", "ETA"],
        )

        # Package Section
        writer.heading("Comm ladder")
        comm_ladder = []
        for comm in self.comms:
            comm_ladder.append(
                [comm.name, "", "", "", self.format_frequency(comm.freq)]
            )

        for tanker in self.tankers:
            comm_ladder.append(
                [
                    tanker.callsign,
                    "Tanker",
                    tanker.variant,
                    str(tanker.tacan),
                    self.format_frequency(tanker.freq),
                ]
            )

        writer.table(comm_ladder, headers=["Callsign", "Task", "Type", "TACAN", "FREQ"])

        writer.heading("JTAC")
        jtacs = []
        for jtac in self.jtacs:
            jtacs.append([jtac.callsign, jtac.region, jtac.code])
        writer.table(jtacs, headers=["Callsign", "Region", "Laser Code"])

        writer.write(path)

    def airfield_info_row(
        self, row_title: str, runway: Optional[RunwayData]
    ) -> List[str]:
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
        if runway.tacan is None:
            tacan = ""
        else:
            tacan = str(runway.tacan)
        if runway.ils is not None:
            ils = str(runway.ils)
        elif runway.icls is not None:
            ils = str(runway.icls)
        else:
            ils = ""
        return [
            row_title,
            runway.airfield_name,
            atc,
            tacan,
            ils,
            runway.runway_name,
        ]

    def format_frequency(self, frequency: RadioFrequency) -> str:
        channel = self.flight.channel_for(frequency)
        if channel is None:
            return str(frequency)

        namer = AIRCRAFT_DATA[self.flight.aircraft_type.id].channel_namer
        channel_name = namer.channel_name(channel.radio_id, channel.channel)
        return f"{channel_name} {frequency}"

    def _format_time(self, time: Optional[datetime.timedelta]) -> str:
        if time is None:
            return ""
        local_time = self.start_time + time
        return local_time.strftime(f"%H:%M:%S")


class KneeboardGenerator(MissionInfoGenerator):
    """Creates kneeboard pages for each client flight in the mission."""

    def __init__(self, mission: Mission, game: "Game") -> None:
        super().__init__(mission, game)

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
                self.generate_flight_kneeboard(flight)
            )
        return all_flights

    def generate_flight_kneeboard(self, flight: FlightData) -> List[KneeboardPage]:
        """Returns a list of kneeboard pages for the given flight."""
        return [
            BriefingPage(
                flight,
                self.comms,
                self.awacs,
                self.tankers,
                self.jtacs,
                self.mission.start_time,
            ),
        ]
