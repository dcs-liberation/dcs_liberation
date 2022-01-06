from __future__ import annotations

from collections.abc import Iterator
from typing import Optional, TYPE_CHECKING

from dcs import Point
from shapely.ops import unary_union

from game.utils import dcs_to_shapely_point

if TYPE_CHECKING:
    from game.ato import Flight
    from game.ato.airtaaskingorder import AirTaskingOrder
    from game.threatzones import ThreatPoly
    from game.sim.combat import FrozenCombat


class AircraftEngagementZones:
    def __init__(self, individual_zones: dict[Flight, ThreatPoly]) -> None:
        self.individual_zones = individual_zones
        self.threat_zones = self._make_combined_zone()

    def update_for_combat(self, combat: FrozenCombat) -> None:
        for flight in combat.iter_flights():
            try:
                del self.individual_zones[flight]
            except KeyError:
                pass
        self.threat_zones = self._make_combined_zone()

    def remove_flight(self, flight: Flight) -> None:
        try:
            del self.individual_zones[flight]
        except KeyError:
            pass
        self.threat_zones = self._make_combined_zone()

    def _make_combined_zone(self) -> ThreatPoly:
        return unary_union(self.individual_zones.values())

    def covers(self, position: Point) -> bool:
        return self.threat_zones.intersects(dcs_to_shapely_point(position))

    def iter_intercepting_flights(self, position: Point) -> Iterator[Flight]:
        for flight, zone in self.individual_zones.items():
            if zone.intersects(dcs_to_shapely_point(position)):
                yield flight

    @classmethod
    def from_ato(cls, ato: AirTaskingOrder) -> AircraftEngagementZones:
        zones = {}
        for package in ato.packages:
            for flight in package.flights:
                if (region := cls.commit_region(flight)) is not None:
                    zones[flight] = region
        return AircraftEngagementZones(zones)

    @classmethod
    def commit_region(cls, flight: Flight) -> Optional[ThreatPoly]:
        return flight.state.a2a_commit_region()
