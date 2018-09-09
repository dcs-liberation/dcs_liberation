import pickle

from dcs.mission import Mission

for terrain in ["cau", "gulf"]:
    m = Mission()
    m.load_file("./{}_terrain.miz".format(terrain))

    landmap = []
    for plane_group in m.country("USA").plane_group:
        landmap.append([(x.position.x, x.position.y) for x in plane_group.points])

    with open("../{}landmap.p".format(terrain), "wb") as f:
        pickle.dump(landmap, f)
