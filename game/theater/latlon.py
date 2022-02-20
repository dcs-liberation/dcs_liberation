from typing import List, Tuple

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class LatLon:
    # These names match Leaflet for easier interop.
    lat: float
    lng: float

    def as_list(self) -> List[float]:
        return [self.lat, self.lng]

    @staticmethod
    def _components(dimension: float) -> Tuple[int, int, float]:
        degrees = int(dimension)
        minutes = int(dimension * 60 % 60)
        seconds = dimension * 3600 % 60
        return degrees, minutes, seconds

    def _format_component(
        self, dimension: float, hemispheres: Tuple[str, str], seconds_precision: int
    ) -> str:
        hemisphere = hemispheres[0] if dimension >= 0 else hemispheres[1]
        degrees, minutes, seconds = self._components(dimension)
        return f"{degrees}°{minutes:02}'{seconds:02.{seconds_precision}f}\"{hemisphere}"

    def format_dms(self, include_decimal_seconds: bool = False) -> str:
        precision = 2 if include_decimal_seconds else 0
        return " ".join(
            [
                self._format_component(self.lat, ("N", "S"), precision),
                self._format_component(self.lng, ("E", "W"), precision),
            ]
        )
