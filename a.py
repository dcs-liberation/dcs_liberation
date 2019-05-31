from theater.caucasus import *
from gen.conflictgen import Conflict

from matplotlib import pyplot
from matplotlib import lines
from shapely import geometry
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

def put_lines(ls, ax):
    for g in ls.geoms:
        ax.plot([g.xy[0][0], g.xy[0][1]], [g.xy[1][0], g.xy[1][1]])

cau = CaucasusTheater()
#left, heading, dist = Conflict.frontline_vector(cau.soganlug, cau.kutaisi, cau)
#right = left.point_from_heading(heading, dist)

left, heading = Conflict.frontline_position(cau, cau.soganlug, cau.kutaisi)
right = left.point_from_heading(heading+90, 80000)
left = left.point_from_heading(heading-90, 80000)

line = geometry.LineString([(left.x, left.y), (right.x, right.y)])
line = line.intersection(cau.land_poly)

fig = pyplot.figure(1, figsize=(20, 20), dpi=90)
ax = fig.add_subplot(121)
ax.set_ylim([0, 1500000])
ax.set_xlim([-600000, 400000])

patch = PolygonPatch(cau.land_poly, facecolor=(0, 0, 0), edgecolor=(0, 0, 0), alpha=0.5, zorder=2)
ax.add_patch(patch)
ax.plot([left.x, right.x], [left.y, right.y], 'k-', lw=2)

ax.plot([cau.soganlug.position.x, cau.soganlug.position.x+1000], [cau.soganlug.position.y, cau.soganlug.position.y+1000], lw=5)
ax.plot([cau.kutaisi.position.x, cau.kutaisi.position.x+1000], [cau.kutaisi.position.y, cau.kutaisi.position.y+1000], lw=5)
put_lines(line, ax)
pyplot.show()

