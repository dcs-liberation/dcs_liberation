from dataclasses import dataclass
import pickle
from functools import cached_property
from typing import Optional, Tuple, Union
import logging
from pathlib import Path
from typing import List

from shapely import geometry
from shapely.geometry import MultiPolygon, Polygon

from dcs.drawing.drawing import LineStyle, Rgba
from dcs.drawing.polygon import FreeFormPolygon
from dcs.mapping import Point
from dcs.mission import Mission
from dcs.terrain.terrain import Terrain


@dataclass(frozen=True)
class Landmap:
    inclusion_zones: MultiPolygon
    exclusion_zones: MultiPolygon
    sea_zones: MultiPolygon

    def __post_init__(self) -> None:
        if not self.inclusion_zones.is_valid:
            raise RuntimeError("Inclusion zones not valid")
        if not self.exclusion_zones.is_valid:
            raise RuntimeError("Exclusion zones not valid")
        if not self.sea_zones.is_valid:
            raise RuntimeError("Sea zones not valid")

    @cached_property
    def inclusion_zone_only(self) -> MultiPolygon:
        return self.inclusion_zones - self.exclusion_zones - self.sea_zones


def load_landmap(filename: Path) -> Optional[Landmap]:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except:
        logging.exception(f"Failed to load landmap {filename}")
        return None


def poly_contains(x: float, y: float, poly: Union[MultiPolygon, Polygon]) -> bool:
    return poly.contains(geometry.Point(x, y))


def to_miz(landmap: Landmap, terrain: Terrain, mission_filename: str) -> None:
    """
    Writes landmap to .miz file so that zones can be visualized and edited in the
    mission editor.
    """

    def multi_polygon_to_miz(
        mission: Mission,
        terrain: Terrain,
        multi_polygon: MultiPolygon,
        color: Rgba,
        prefix: str,
        layer_index: int = 4,
        layer_name: str = "Author",
    ) -> None:
        reference_position = Point(0, 0, terrain)
        for i in range(len(multi_polygon.geoms)):
            polygon = multi_polygon.geoms[i]
            if len(polygon.interiors) > 0:
                raise ValueError(
                    f"Polygon hole found when trying to export {prefix} {i}. to_miz() does not support landmap zones with holes."
                )
            coordinates = polygon.exterior.xy
            points = []
            for j in range(len(coordinates[0])):
                points.append(Point(coordinates[0][j], coordinates[1][j], terrain))
            polygon_drawing = FreeFormPolygon(
                visible=True,
                position=reference_position,
                name=f"{prefix}-{i}",
                color=color,
                layer_name=layer_name,
                fill=color,
                line_thickness=10,
                line_style=LineStyle.Solid,
                points=points,
            )
            mission.drawings.layers[layer_index].objects.append(polygon_drawing)

    mission = Mission(terrain=terrain)
    multi_polygon_to_miz(
        mission, terrain, landmap.exclusion_zones, Rgba(255, 0, 0, 128), "Exclusion"
    )
    multi_polygon_to_miz(
        mission, terrain, landmap.sea_zones, Rgba(0, 0, 255, 128), "Sea"
    )
    multi_polygon_to_miz(
        mission, terrain, landmap.inclusion_zones, Rgba(0, 255, 0, 128), "Inclusion"
    )
    mission.save(mission_filename)


def from_miz(mission_filename: str, layer_index: int = 4) -> Landmap:
    """
    Generate Landmap object from Free Form Polygons drawn in a .miz file.
    Landmap.inclusion_zones are expected to be named Inclusion-<suffix>
    Landmap.exclusion_zones are expected to be named Exclusion-<suffix>
    Landmap.sea_zones are expected to be named Sea-<suffix>
    """
    mission = Mission()
    mission.load_file(mission_filename)
    polygons: dict[str, List[Polygon]] = {"Inclusion": [], "Exclusion": [], "Sea": []}
    for draw_object in mission.drawings.layers[layer_index].objects:
        if type(draw_object) != FreeFormPolygon:
            logging.debug(
                f"Object {draw_object.name} is not a FreeFormPolygon, ignoring"
            )
            continue
        name_split = draw_object.name.split(
            "-"
        )  # names are in the format <Inclusion|Exclusion|Sea>-<suffix>
        zone_type = name_split[0]
        if len(name_split) != 2 or zone_type not in ("Exclusion", "Sea", "Inclusion"):
            logging.debug(
                f"Object name {draw_object.name} does not conform to expected format <Exclusion|Sea|Inclusion>-<suffix>, ignoring"
            )
            continue
        polygon_points = []
        for point in draw_object.points:
            polygon_points.append(
                (point.x + draw_object.position.x, point.y + draw_object.position.y)
            )
        polygons[zone_type].append(Polygon(polygon_points))
    landmap = Landmap(
        inclusion_zones=MultiPolygon(polygons["Inclusion"]),
        exclusion_zones=MultiPolygon(polygons["Exclusion"]),
        sea_zones=MultiPolygon(polygons["Sea"]),
    )
    return landmap
