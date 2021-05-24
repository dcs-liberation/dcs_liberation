from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class LatLon:
    latitude: float
    longitude: float

    def as_list(self) -> List[float]:
        return [self.latitude, self.longitude]
