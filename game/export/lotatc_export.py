import json
import logging
import uuid
import utm

from game.version import (
    VERSION
)

from typing import (
    Tuple
)

from game import Game
from dcs.mapping import Point

def export_threat_circles(game: Game, path):

    colorRed = '#64E32000'

    data = {}
    data['enabled'] = 'true'
    data['version'] = '2.2.0'
    data['drawings'] = []

    point_a = game.theater.reference_points[0]

    timestamp = game.current_day.isoformat()

    objects_aa = []
    for cp in game.theater.control_points_for(False):
        for ground_object in cp.ground_objects:
            if ground_object.obj_name in objects_aa:
                continue
        
            if ground_object.might_have_aa and not ground_object.is_dead:
                objects_aa.append(ground_object)

    for o in objects_aa:
        go_pos = o.position
        go_pos1 = _transpose_point(point_a.world_coordinates - go_pos)

        for g in o.groups:
            threat_range = o.threat_range(g)
            threat_pos = o.position + Point(threat_range.meters, threat_range.meters)
            threat_radius = go_pos.distance_to_point(threat_pos)

            (lat, lon) = utm.to_latlon(point_a.world_coordinates.x, point_a.world_coordinates.y, 1, 'U', None, False)

            data['drawings'].append({
                'author': VERSION,
                'brushStyle': 1,
                'color': colorRed,
                'colorBg': '#00ff0000',
                'id': f"{uuid.uuid4()}",
                'longitude': go_pos1.x,
                'latitude': go_pos1.y,
                'radius': threat_radius,
                'lineWidth': 1,
                'name': f"{o.name}|{o.group_name}",
                'shared': True,
                'timestamp': timestamp,
                'type': 'circle',
                'text': f"{o.name}|{o.group_name}",
                'font': {
                    'color': colorRed,
                    'font': 'Lato'
                },
            })

    try:
        with open(path, "w") as f:
            json.dump(data, f)

    except Exception:
        logging.exception("Could not export LotAtc drawings file")

    return

def _transform_point(game: Game, world_point: Point) -> Tuple[float, float]:
    point_a = game.theater.reference_points[0]
    scale = _scaling_factor(game)

    offset = _transpose_point(point_a.world_coordinates - world_point)
    scaled = Point(offset.x * scale.x, offset.y * scale.y)
    transformed = point_a.world_coordinates - scaled
    return transformed.x, transformed.y

def _scene_to_dcs_coords(game: Game, scene_point: Point) -> Point:
    point_a = game.theater.reference_points[0]
    scale = _scaling_factor(game)

    offset = point_a.image_coordinates - scene_point
    scaled = _transpose_point(Point(offset.x / scale.x, offset.y / scale.y))
    return point_a.world_coordinates - scaled

def _scaling_factor(game: Game) -> Point:
    point_a = game.theater.reference_points[0]
    point_b = game.theater.reference_points[1]

    world_distance = _transpose_point(
        point_b.world_coordinates - point_a.world_coordinates
    )
    image_distance = point_b.image_coordinates - point_a.image_coordinates

    x_scale = image_distance.x / world_distance.x
    y_scale = image_distance.y / world_distance.y
    return Point(x_scale, y_scale)

def _transpose_point(p: Point) -> Point:
    return Point(p.y, p.x)