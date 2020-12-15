import pickle

from dcs.mission import Mission
from shapely import geometry

for terrain in ["cau", "nev", "syria", "channel", "normandy", "gulf"]:
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
            exclusion_zones.append(geometry.Polygon(zone))
        else:
            if plane_group.units[0].type == "F-15C":
                exclusion_zones.append(geometry.Polygon(zone))
            else:
                inclusion_zones.append(geometry.Polygon(zone))

    for ship_group in m.country("USA").ship_group:
        zone = [(x.position.x, x.position.y) for x in ship_group.points]
        seas_zones.append(geometry.Polygon(zone))

    with open("../{}landmap.p".format(terrain), "wb") as f:
        print(len(inclusion_zones), len(exclusion_zones), len(seas_zones))
        pickle.dump((inclusion_zones, exclusion_zones, seas_zones), f)
