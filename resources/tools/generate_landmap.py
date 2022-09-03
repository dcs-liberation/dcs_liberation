import pickle
from functools import singledispatch

from dcs.mission import Mission
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon
from shapely.ops import unary_union

from game.theater.landmap import Landmap


@singledispatch
def to_multipoly(obj) -> MultiPolygon:
    raise NotImplementedError(
        f"to_multipoly not implemented for {obj.__class__.__name__}"
    )


@to_multipoly.register
def _poly_to_multipoly(obj: Polygon) -> MultiPolygon:
    return MultiPolygon([obj])


@to_multipoly.register
def _multipoly_to_multipoly(obj: MultiPolygon) -> MultiPolygon:
    return obj


@to_multipoly.register
def _geometry_collection_to_multipoly(obj: GeometryCollection) -> MultiPolygon:
    if obj.is_empty:
        return MultiPolygon()
    raise RuntimeError(f"Not sure how to convert collection to multipoly: {obj.wkt}")


def main() -> None:
    for terrain in [
        "cau",
        "nev",
        "syria",
        "channel",
        "normandy",
        "gulf",
        "marianaislands",
    ]:
        print("Terrain " + terrain)
        m = Mission()
        m.load_file("./{}_terrain.miz".format(terrain))

        inclusion_zones = []
        exclusion_zones = []
        seas_zones = []
        for plane_group in m.country("USA").plane_group:
            zone = [(x.position.x, x.position.y) for x in plane_group.points]

            if terrain == "cau" and inclusion_zones:
                # legacy
                exclusion_zones.append(Polygon(zone))
            else:
                poly = Polygon(zone)
                if not poly.is_valid:
                    raise RuntimeError(f"{plane_group} is invalid")
                if plane_group.units[0].type == "F-15C":
                    exclusion_zones.append(poly)
                else:
                    inclusion_zones.append(poly)

        for ship_group in m.country("USA").ship_group:
            zone = [(x.position.x, x.position.y) for x in ship_group.points]
            seas_zones.append(Polygon(zone))

        with open("../{}landmap.p".format(terrain), "wb") as f:
            print(len(inclusion_zones), len(exclusion_zones), len(seas_zones))
            pickle.dump(
                Landmap(
                    to_multipoly(unary_union(inclusion_zones)),
                    to_multipoly(unary_union(exclusion_zones)),
                    to_multipoly(unary_union(seas_zones)),
                ),
                f,
            )


if __name__ == "__main__":
    main()
