import pickle
import typing

from dcs.mission import Mission
from dcs.mapping import Point
from dcs.unit import *
from dcs.statics import warehouse_map, fortification_map


def load_templates():
    temp_mis = Mission()
    temp_mis.load_file("resources/tools/groundobject_templates.miz")

    groups = {}  # type: typing.Dict[str, typing.Dict[int, typing.List[Static]]]

    for static_group in temp_mis.country("USA").static_group + temp_mis.country("USAF Aggressors").static_group:
        for static in static_group.units:
            static_name = str(static.name).split()[0]
            tpl_name, tpl_idx = static_name[:-1], int(static_name[-1])

            groups[tpl_name] = groups.get(tpl_name, {})
            groups[tpl_name][tpl_idx] = groups[tpl_name].get(tpl_idx, [])
            groups[tpl_name][tpl_idx].append(static)

    tpls = {name: {idx: [] for idx in groups[name].keys()} for name in groups.keys()}
    for category_name, category_groups in groups.items():
        for idx, static_groups in category_groups.items():
            dist = -1
            a, b = None, None
            for aa in static_groups:
                for bb in static_groups:
                    if aa.position.distance_to_point(bb.position) > dist:
                        dist = aa.position.distance_to_point(bb.position)
                        a = aa
                        b = bb

            center = a.position.point_from_heading(a.position.heading_between_point(b.position), dist / 2)
            for static in static_groups:
                tpls[category_name][idx].append({
                    "type": static.type,
                    "offset": Point(center.x - static.position.x, center.y - static.position.y),
                    "heading": static.heading,
                })

    tpls["aa"] = {0: [{"type": "AA", "offset": Point(0, 0), "heading": 0}]}
    return tpls


with open("resources/groundobject_templates.p", "wb") as f:
    pickle.dump(load_templates(), f)
