from __future__ import annotations

import uuid
from typing import Any, TYPE_CHECKING

from dcs.planes import C_101CC, C_101EB, Su_33

from game.ato.loadouts import Loadout

if TYPE_CHECKING:
    from game.dcs.aircrafttype import AircraftType
    from game.squadrons.pilot import Pilot
    from game.squadrons.squadron import Squadron
    from game.theater.controlpoint import ControlPoint
    from game.theater.missiontarget import MissionTarget
    from game.transfers import TransferOrder
    from .flightroster import FlightRoster
    from .flighttype import FlightType
    from .package import Package
    from .starttype import StartType


class Flight:
    def __init__(
        self,
        package: Package,
        country: str,
        squadron: Squadron,
        count: int,
        flight_type: FlightType,
        start_type: StartType,
        divert: ControlPoint | None,
        custom_name: str | None = None,
        cargo: TransferOrder | None = None,
        roster: FlightRoster | None = None,
    ) -> None:
        self.id = uuid.uuid4()
        self.package = package
        self.country = country
        self.coalition = squadron.coalition
        self.squadron = squadron
        self.squadron.claim_inventory(count)
        if roster is None:
            self.roster = FlightRoster(self.squadron, initial_size=count)
        else:
            self.roster = roster
        self.divert = divert
        self.flight_type = flight_type
        # TODO: Replace with FlightPlan.
        self.targets: list[MissionTarget] = []
        self.loadout = Loadout.default_for(self)
        self.start_type = start_type
        self.use_custom_loadout = False
        self.custom_name = custom_name

        # Only used by transport missions.
        self.cargo = cargo

        # Flight properties that can be set in the mission editor. This is used for
        # things like HMD selection, ripple quantity, etc. Any values set here will take
        # the place of the defaults defined by DCS.
        #
        # This is a part of the Flight rather than the Loadout because DCS does not
        # associate these choices with the loadout, and we don't want to reset these
        # options when players switch loadouts.
        self.props: dict[str, Any] = {}

    def resize(self, new_size: int) -> None:
        self.squadron.claim_inventory(new_size - self.count)
        self.roster.resize(new_size)

    def set_pilot(self, index: int, pilot: Pilot | None) -> None:
        self.roster.set_pilot(index, pilot)

    def return_pilots_and_aircraft(self) -> None:
        self.roster.clear()
        self.squadron.claim_inventory(-self.count)

    def max_takeoff_fuel(self) -> float | None:
        # Special case so Su 33 and C101 can take off
        unit_type = self.unit_type.dcs_unit_type
        if unit_type == Su_33:
            if self.flight_type.is_air_to_air:
                return Su_33.fuel_max / 2.2
            else:
                return Su_33.fuel_max * 0.8
        elif unit_type in {C_101EB, C_101CC}:
            return unit_type.fuel_max * 0.5
        return None

    def __repr__(self) -> str:
        if self.custom_name:
            return f"{self.custom_name} {self.count} x {self.unit_type}"
        return f"[{self.flight_type}] {self.count} x {self.unit_type}"

    def __str__(self) -> str:
        if self.custom_name:
            return f"{self.custom_name} {self.count} x {self.unit_type}"
        return f"[{self.flight_type}] {self.count} x {self.unit_type}"

    @property
    def is_helo(self) -> bool:
        return self.unit_type.dcs_unit_type.helicopter

    @property
    def arrival(self) -> ControlPoint:
        return self.squadron.arrival

    @property
    def count(self) -> int:
        return self.roster.max_size

    @property
    def missing_pilots(self) -> int:
        return self.roster.missing_pilots

    @property
    def unit_type(self) -> AircraftType:
        return self.squadron.aircraft

    @property
    def from_cp(self) -> ControlPoint:
        return self.departure

    @property
    def blue(self) -> bool:
        return self.squadron.player

    @property
    def departure(self) -> ControlPoint:
        return self.squadron.location

    @property
    def client_count(self) -> int:
        return self.roster.player_count
