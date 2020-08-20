import pickle

from dcs.mission import Mission
from dcs.planes import A_10C

for terrain in ["cau"]:
    print("Terrain " + terrain)
    m = Mission()
    m.load_file("./{}_terrain.miz".format(terrain))

    inclusion_zones = []
    exclusion_zones = []
    for plane_group in m.country("USA").plane_group:
        zone = [(x.position.x, x.position.y) for x in plane_group.points]

        if terrain == "cau" and inclusion_zones:
            # legacy
            exclusion_zones.append(zone)
        else:
            if plane_group.units[0].type == "F-15C":
                exclusion_zones.append(zone)
            else:
                inclusion_zones.append(zone)

    with open("../{}landmap.p".format(terrain), "wb") as f:
        print(len(inclusion_zones), len(exclusion_zones))
        pickle.dump((inclusion_zones, exclusion_zones), f)
