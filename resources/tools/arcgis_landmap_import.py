"""Generates landmaps from GIS shapefiles."""
import argparse
import logging
import pickle
from collections.abc import Iterator
from enum import Enum, unique
from pathlib import Path

from pyproj import CRS, Transformer
from shapefile import Reader, Shape
from shapely.geometry import LineString, MultiPolygon, Polygon, shape
from shapely.ops import unary_union

from game.profiling import logged_duration
from game.theater import ConflictTheater, Landmap
from game.theater.theaterloader import TheaterLoader
from resources.tools.generate_landmap import to_multipoly

THIS_DIR = Path(__file__).resolve()
TOP_DIR = THIS_DIR.parents[2]
IMPORT_DIR = TOP_DIR / "unshipped_data/arcgis_maps"
RESOURCES_DIR = TOP_DIR / "resources"


ALL_THEATER_NAMES = [d.name for d in (RESOURCES_DIR / "theaters").iterdir()]


@unique
class ShapeType(Enum):
    LAND = "land"
    SEA = "sea"
    EXCLUSION = "exclusion"

    @property
    def import_directory_name(self) -> str:
        return self.value


class CoordinateConverter:
    def __init__(self, theater: ConflictTheater, projection_file: Path) -> None:
        self.theater = theater
        self.transformer = self._transformer_for(projection_file)

    def convert_to_dcs_coords(self, polys: list[Polygon]) -> list[Polygon]:
        new_polys = []
        for poly in polys:
            for boundary, holes in self._boundary_and_holes_of(poly):
                new_polys.append(
                    Polygon(
                        self._convert_line_to_dcs_coords(boundary),
                        holes=[
                            self._convert_line_to_dcs_coords(hole) for hole in holes
                        ],
                    )
                )
        return new_polys

    def _transformer_for(self, projection_file: Path) -> Transformer:
        prj = projection_file.read_text()
        return Transformer.from_crs(
            CRS(prj), self.theater.terrain.projection_parameters.to_crs()
        )

    @staticmethod
    def _boundary_and_holes_of(poly: Polygon) -> Iterator[LineString, list[LineString]]:
        try:
            boundary, *holes = poly.boundary.geoms
            yield boundary, holes
        except AttributeError:
            yield poly.boundary, []

    def _convert_line_to_dcs_coords(
        self, line: LineString
    ) -> list[tuple[float, float]]:
        return [self.transformer.transform(x, y) for x, y in line.coords]


class ShapefileReader:
    def __init__(
        self, theater_name: str, theater: ConflictTheater, shape_type: ShapeType
    ) -> None:
        self.theater_name = theater_name
        self.theater = theater
        self.shape_type = shape_type

    def read_dcs_polys(self) -> list[Polygon]:
        shapefile = self._shapefile_path
        logging.debug(
            f"Reading ARCGIS landmap {self.shape_type.value} data from {shapefile}"
        )
        with logged_duration("Loading polygons"):
            raw_polys = self._load_raw_polys_from_shapefile(shapefile)
        logging.debug("Converting to DCS coordinate system")
        with logged_duration("Converting shapefile data to DCS coordinates"):
            converter = CoordinateConverter(self.theater, shapefile.with_suffix(".prj"))
            return converter.convert_to_dcs_coords(raw_polys)

    @staticmethod
    def _polys_from_map_shape(map_shape: Shape) -> list[Polygon]:
        geoms = shape(map_shape)
        try:
            return geoms.geoms
        except AttributeError:
            return [geoms]

    def _load_raw_polys_from_shapefile(self, shapefile: Path) -> list[Polygon]:
        polys: list[Polygon] = []
        with Reader(shapefile) as reader:
            shapes = reader.shapes()
            for idx, map_shape in enumerate(shapes):
                polys.extend(self._polys_from_map_shape(map_shape))
        return polys

    @property
    def _import_directory(self) -> Path:
        return IMPORT_DIR / self.theater_name / self.shape_type.import_directory_name

    @property
    def _shapefile_path(self) -> Path:
        import_dir = self._import_directory
        files = list(import_dir.glob("*.shp"))
        if len(files) != 1:
            raise RuntimeError(
                f"Could not find a unique file matching {import_dir / '*.shp'}"
            )
        return files[0]


class PolygonFilter:
    def __init__(self, min_size_sq_m: float) -> None:
        self.min_size_sq_m = min_size_sq_m

    def filter(self, polys: list[Polygon]) -> list[Polygon]:
        logging.debug("Filtering small polys")
        with logged_duration("Filtering small polys"):
            return self._ignore_small_polys(polys)

    def _ignore_small_polys(self, polys: list[Polygon]) -> list[Polygon]:
        # Polygons are in DCS coordinates, which are in meters.
        filtered = [p for p in polys if p.area >= self.min_size_sq_m]
        logging.debug(
            "Filtered %d polygons smaller than %d sq meters",
            len(polys) - len(filtered),
            self.min_size_sq_m,
        )
        return filtered


class Importer:
    def __init__(self, theater_name: str) -> None:
        self.theater_name = theater_name
        self.theater = TheaterLoader(theater_name).load()

    def generate_landmap(self) -> Landmap:
        return Landmap(
            inclusion_zones=self._terrain_multipoly_for(ShapeType.LAND),
            exclusion_zones=self._terrain_multipoly_for(ShapeType.EXCLUSION),
            sea_zones=self._terrain_multipoly_for(ShapeType.SEA),
        )

    def _terrain_multipoly_for(self, shape_type: ShapeType) -> MultiPolygon:
        polys = ShapefileReader(
            self.theater_name, self.theater, shape_type
        ).read_dcs_polys()
        polys = PolygonFilter(min_size_sq_m=50**2).filter(polys)
        logging.debug("Merging %d polys", len(polys))
        with logged_duration("Merging polygons"):
            # Multithreading on our side will not speed up unary_union. This was
            # benchmarked during development with a chunked merge, but all chunk sizes
            # tested underperformed the single call. Testing with the Falklands
            # exclusion polys (do not compare these numbers to your local results, the
            # input data has likely changed).
            #
            # Chunk size of 10: 4m30s
            # Chunk size of 100: 3m55s
            # Chunk size of 1000: 3m50s
            # No chunking: 3m35s
            #
            # The most expensive part of the process was always the final merge. This is
            # probably because there are too many disconnected polygons, so the earlier
            # merges did not actually combine many polys, but instead just (slowly)
            # created multipolygons.
            return to_multipoly(unary_union(polys))


def write_landmap(theater_name: str, landmap: Landmap) -> None:
    with TheaterLoader(theater_name).landmap_path.open("wb") as landmap_file:
        pickle.dump(landmap, landmap_file)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "theater",
        choices=ALL_THEATER_NAMES,
        help="Name of the theater to import.",
    )

    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    args = parse_args()

    with logged_duration("Shapefile import and landmap generation"):
        landmap = Importer(args.theater).generate_landmap()
        write_landmap(args.theater, landmap)
    logging.info(
        "Final landmap has %d land, %d sea, and %d exclusion polys",
        len(landmap.inclusion_zones.geoms),
        len(landmap.sea_zones.geoms),
        len(landmap.exclusion_zones.geoms),
    )


if __name__ == "__main__":
    main()
