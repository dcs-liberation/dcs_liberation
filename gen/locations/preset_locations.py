from dataclasses import dataclass

from dcs import Point


@dataclass
class PresetLocation:
    """A preset location"""
    position: Point
    heading: int
    id: str

    def __str__(self):
        return "-" * 10 + "X: {}\n Y: {}\nHdg: {}°\nId: {}".format(self.position.x, self.position.y, self.heading,
                                                                   self.id) + "-" * 10
