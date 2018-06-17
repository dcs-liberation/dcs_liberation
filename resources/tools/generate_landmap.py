import pickle

from dcs.mission import Mission
from dcs.terrain import PersianGulf

m = Mission()
m.load_file("./gulf_terrain.miz")

landmap = []
for plane_group in m.country("USA").plane_group:
    landmap.append([(x.position.x, x.position.y) for x in plane_group.points])

with open("gulflandmap.p", "wb") as f:
    pickle.dump(landmap, f)
