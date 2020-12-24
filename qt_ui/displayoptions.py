"""Visibility options for the game map."""
from dataclasses import dataclass, field
from typing import Iterator, Optional, Union


@dataclass
class DisplayRule:
    name: str
    _value: bool
    debug_only: bool = field(default=False)

    @property
    def menu_text(self) -> str:
        return self.name

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, value: bool) -> None:
        from qt_ui.widgets.map.QLiberationMap import QLiberationMap
        self._value = value
        if QLiberationMap.instance is not None:
            QLiberationMap.instance.reload_scene()
            QLiberationMap.instance.update()

    def __bool__(self) -> bool:
        return self.value


class DisplayGroup:
    def __init__(self, name: Optional[str], debug_only: bool = False) -> None:
        self.name = name
        self.debug_only = debug_only

    def __iter__(self) -> Iterator[DisplayRule]:
        # Python 3.6 enforces that __dict__ is order preserving by default.
        for value in self.__dict__.values():
            if isinstance(value, DisplayRule):
                yield value


class FlightPathOptions(DisplayGroup):
    def __init__(self) -> None:
        super().__init__("Flight Paths")
        self.hide = DisplayRule("Hide Flight Paths", False)
        self.only_selected = DisplayRule("Show Selected Flight Path", False)
        self.all = DisplayRule("Show All Flight Paths", True)


class ThreatZoneOptions(DisplayGroup):
    def __init__(self, coalition_name: str) -> None:
        super().__init__(f"{coalition_name} Threat Zones")
        self.none = DisplayRule(
            f"Hide {coalition_name.lower()} threat zones", True)
        self.all = DisplayRule(
            f"Show full {coalition_name.lower()} threat zones", False)
        self.aircraft = DisplayRule(
            f"Show {coalition_name.lower()} aircraft threat tones", False)
        self.air_defenses = DisplayRule(
            f"Show {coalition_name.lower()} air defenses threat zones", False)


class NavMeshOptions(DisplayGroup):
    def __init__(self) -> None:
        super().__init__("Navmeshes", debug_only=True)
        self.hide = DisplayRule("DEBUG Hide Navmeshes", True)
        self.blue_navmesh = DisplayRule("DEBUG Show blue navmesh", False)
        self.red_navmesh = DisplayRule("DEBUG Show red navmesh", False)


class PathDebugFactionOptions(DisplayGroup):
    def __init__(self) -> None:
        super().__init__("Faction for path debugging", debug_only=True)
        self.blue = DisplayRule("Debug blue paths", True)
        self.red = DisplayRule("Debug red paths", False)


class PathDebugOptions(DisplayGroup):
    def __init__(self) -> None:
        super().__init__("Shortest paths", debug_only=True)
        self.hide = DisplayRule("DEBUG Hide paths", True)
        self.shortest_path = DisplayRule("DEBUG Show shortest path", False)
        self.barcap = DisplayRule("DEBUG Show BARCAP plan", False)
        self.cas = DisplayRule("DEBUG Show CAS plan", False)
        self.sweep = DisplayRule("DEBUG Show fighter sweep plan", False)
        self.strike = DisplayRule("DEBUG Show strike plan", False)
        self.tarcap = DisplayRule("DEBUG Show TARCAP plan", False)


class DisplayOptions:
    ground_objects = DisplayRule("Ground Objects", True)
    control_points = DisplayRule("Control Points", True)
    lines = DisplayRule("Lines", True)
    sam_ranges = DisplayRule("Ally SAM Threat Range", False)
    enemy_sam_ranges = DisplayRule("Enemy SAM Threat Range", True)
    detection_range = DisplayRule("SAM Detection Range", False)
    map_poly = DisplayRule("Map Polygon Debug Mode", False)
    waypoint_info = DisplayRule("Waypoint Information", True)
    culling = DisplayRule("Display Culling Zones", False)
    flight_paths = FlightPathOptions()
    actual_frontline_pos = DisplayRule("Display Actual Frontline Location",
                                       False)
    blue_threat_zones = ThreatZoneOptions("Blue")
    red_threat_zones = ThreatZoneOptions("Red")
    navmeshes = NavMeshOptions()
    path_debug_faction = PathDebugFactionOptions()
    path_debug = PathDebugOptions()

    @classmethod
    def menu_items(cls) -> Iterator[Union[DisplayGroup, DisplayRule]]:
        debug = False  # Set to True to enable debug options.
        # Python 3.6 enforces that __dict__ is order preserving by default.
        for value in cls.__dict__.values():
            if isinstance(value, DisplayRule):
                if value.debug_only and not debug:
                    continue
                yield value
            elif isinstance(value, DisplayGroup):
                if value.debug_only and not debug:
                    continue
                yield value
