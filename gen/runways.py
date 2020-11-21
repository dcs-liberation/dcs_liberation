"""Runway information and selection."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterator, Optional

from dcs.terrain.terrain import Airport

from game.theater import ControlPoint, ControlPointType
from game.weather import Conditions
from .airfields import AIRFIELD_DATA
from .radios import RadioFrequency
from .tacan import TacanChannel


@dataclass(frozen=True)
class RunwayData:
    airfield_name: str
    runway_heading: int
    runway_name: str
    atc: Optional[RadioFrequency] = None
    tacan: Optional[TacanChannel] = None
    tacan_callsign: Optional[str] = None
    ils: Optional[RadioFrequency] = None
    icls: Optional[int] = None

    @classmethod
    def for_airfield(cls, airport: Airport, runway_heading: int,
                     runway_name: str) -> RunwayData:
        """Creates RunwayData for the given runway of an airfield.

        Args:
            airport: The airfield the runway belongs to.
            runway_heading: Heading of the runway.
            runway_name: Identifier of the runway to use. e.g. "03" or "20L".
        """
        atc: Optional[RadioFrequency] = None
        tacan: Optional[TacanChannel] = None
        tacan_callsign: Optional[str] = None
        ils: Optional[RadioFrequency] = None
        try:
            airfield = AIRFIELD_DATA[airport.name]
            if airfield.atc is not None:
                atc = airfield.atc.uhf
            else:
                atc = None
            tacan = airfield.tacan
            tacan_callsign = airfield.tacan_callsign
            ils = airfield.ils_freq(runway_name)
        except KeyError:
            logging.warning(f"No airfield data for {airport.name}")
        return cls(
            airfield_name=airport.name,
            runway_heading=runway_heading,
            runway_name=runway_name,
            atc=atc,
            tacan=tacan,
            tacan_callsign=tacan_callsign,
            ils=ils
        )

    @classmethod
    def for_pydcs_airport(cls, airport: Airport) -> Iterator[RunwayData]:
        for runway in airport.runways:
            runway_number = runway.heading // 10
            runway_side = ["", "L", "R"][runway.leftright]
            runway_name = f"{runway_number:02}{runway_side}"
            yield cls.for_airfield(airport, runway.heading, runway_name)

            # pydcs only exposes one runway per physical runway, so to expose
            # both sides of the runway we need to generate the other.
            heading = (runway.heading + 180) % 360
            runway_number = heading // 10
            runway_side = ["", "R", "L"][runway.leftright]
            runway_name = f"{runway_number:02}{runway_side}"
            yield cls.for_airfield(airport, heading, runway_name)


class RunwayAssigner:
    def __init__(self, conditions: Conditions):
        self.conditions = conditions

    def angle_off_headwind(self, runway: RunwayData) -> int:
        wind = self.conditions.weather.wind.at_0m.direction
        ideal_heading = (wind + 180) % 360
        return abs(runway.runway_heading - ideal_heading)

    def get_preferred_runway(self, airport: Airport) -> RunwayData:
        """Returns the preferred runway for the given airport.

        Right now we're only selecting runways based on whether or not
        they have
        ILS, but we could also choose based on wind conditions, or which
        direction flight plans should follow.
        """
        runways = list(RunwayData.for_pydcs_airport(airport))

        # Find the runway with the best headwind first.
        best_runways = [runways[0]]
        best_angle_off_headwind = self.angle_off_headwind(best_runways[0])
        for runway in runways[1:]:
            angle_off_headwind = self.angle_off_headwind(runway)
            if angle_off_headwind == best_angle_off_headwind:
                best_runways.append(runway)
            elif angle_off_headwind < best_angle_off_headwind:
                best_runways = [runway]
                best_angle_off_headwind = angle_off_headwind

        for runway in best_runways:
            # But if there are multiple runways with the same heading,
            # prefer
            # and ILS capable runway.
            if runway.ils is not None:
                return runway

        # Otherwise the only difference between the two is the distance from
        # parking, which we don't know, so just pick the first one.
        return best_runways[0]

    def takeoff_heading(self, departure: ControlPoint) -> int:
        if departure.cptype == ControlPointType.AIRBASE:
            return self.get_preferred_runway(departure.airport).runway_heading
        elif departure.is_fleet:
            # The carrier will be angled into the wind automatically.
            return (self.conditions.weather.wind.at_0m.direction + 180) % 360
        logging.warning(
            f"Unhandled departure control point: {departure.cptype}")
        return 0

    def landing_heading(self, arrival: ControlPoint) -> int:
        if arrival.cptype == ControlPointType.AIRBASE:
            return self.get_preferred_runway(arrival.airport).runway_heading
        elif arrival.is_fleet:
            # The carrier will be angled into the wind automatically.
            return (self.conditions.weather.wind.at_0m.direction + 180) % 360
        logging.warning(
            f"Unhandled departure control point: {arrival.cptype}")
        return 0
