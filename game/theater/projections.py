from dataclasses import dataclass

from pyproj import CRS


@dataclass(frozen=True)
class TransverseMercator:
    central_meridian: int
    false_easting: float
    false_northing: float
    scale_factor: float

    def to_crs(self) -> CRS:
        return CRS.from_proj4(
            " ".join(
                [
                    "+proj=tmerc",
                    "+lat_0=0",
                    f"+lon_0={self.central_meridian}",
                    f"+k_0={self.scale_factor}",
                    f"+x_0={self.false_easting}",
                    f"+y_0={self.false_northing}",
                    "+towgs84=0,0,0,0,0,0,0",
                    "+units=m",
                    "+vunits=m",
                    "+ellps=WGS84",
                    "+no_defs",
                    "+axis=neu",
                ]
            )
        )
