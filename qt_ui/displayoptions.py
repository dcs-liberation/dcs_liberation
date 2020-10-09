"""Visibility options for the game map."""
from dataclasses import dataclass
from typing import Iterator


@dataclass
class DisplayRule:
    name: str
    _value: bool

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
        QLiberationMap.instance.reload_scene()
        QLiberationMap.instance.update()

    def __bool__(self) -> bool:
        return self.value


class DisplayOptions:
    ground_objects = DisplayRule("Ground Objects", True)
    control_points = DisplayRule("Control Points", True)
    lines = DisplayRule("Lines", True)
    events = DisplayRule("Events", True)
    sam_ranges = DisplayRule("SAM Ranges", True)
    flight_paths = DisplayRule("Flight Paths", False)

    @classmethod
    def menu_items(cls) -> Iterator[DisplayRule]:
        # Python 3.6 enforces that __dict__ is order preserving by default.
        for value in cls.__dict__.values():
            if isinstance(value, DisplayRule):
                yield value
