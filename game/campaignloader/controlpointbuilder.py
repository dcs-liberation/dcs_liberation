from dcs import Point
from dcs.terrain import Airport

from game.campaignloader.controlpointconfig import ControlPointConfig
from game.theater import (
    Airfield,
    Carrier,
    ConflictTheater,
    ControlPoint,
    Fob,
    Lha,
    OffMapSpawn,
)


class ControlPointBuilder:
    def __init__(
        self, theater: ConflictTheater, configs: dict[str | int, ControlPointConfig]
    ) -> None:
        self.theater = theater
        self.config = configs

    def create_airfield(self, airport: Airport) -> Airfield:
        cp = Airfield(airport, self.theater, starts_blue=airport.is_blue())

        # Use the unlimited aircraft option to determine if an airfield should
        # be owned by the player when the campaign is "inverted".
        cp.captured_invert = airport.unlimited_aircrafts

        self._apply_config(airport.id, cp)
        return cp

    def create_fob(
        self,
        name: str,
        position: Point,
        theater: ConflictTheater,
        starts_blue: bool,
        captured_invert: bool,
    ) -> Fob:
        cp = Fob(name, position, theater, starts_blue)
        cp.captured_invert = captured_invert
        self._apply_config(name, cp)
        return cp

    def create_carrier(
        self,
        name: str,
        position: Point,
        theater: ConflictTheater,
        starts_blue: bool,
        captured_invert: bool,
    ) -> Carrier:
        cp = Carrier(name, position, theater, starts_blue)
        cp.captured_invert = captured_invert
        self._apply_config(name, cp)
        return cp

    def create_lha(
        self,
        name: str,
        position: Point,
        theater: ConflictTheater,
        starts_blue: bool,
        captured_invert: bool,
    ) -> Lha:
        cp = Lha(name, position, theater, starts_blue)
        cp.captured_invert = captured_invert
        self._apply_config(name, cp)
        return cp

    def create_off_map(
        self,
        name: str,
        position: Point,
        theater: ConflictTheater,
        starts_blue: bool,
        captured_invert: bool,
    ) -> OffMapSpawn:
        cp = OffMapSpawn(name, position, theater, starts_blue)
        cp.captured_invert = captured_invert
        self._apply_config(name, cp)
        return cp

    def _apply_config(self, cp_id: str | int, control_point: ControlPoint) -> None:
        config = self.config.get(cp_id)
        if config is None:
            return

        control_point.ferry_only = config.ferry_only
