from dcs import Point
from dcs.drawing import LineStyle, Rgba
from dcs.drawing.drawings import StandardLayer
from dcs.mission import Mission

from game import Game
from game.missiongenerator.frontlineconflictdescription import (
    FrontLineConflictDescription,
)

# Misc config settings for objects drawn in ME mission file (and F10 map)
FRONTLINE_COLORS = Rgba(255, 0, 0, 255)
WHITE = Rgba(255, 255, 255, 255)
CP_RED = Rgba(255, 0, 0, 80)
CP_BLUE = Rgba(0, 0, 255, 80)
CP_CIRCLE_RADIUS = 2500
BLUE_PATH_COLOR = Rgba(0, 0, 255, 100)
RED_PATH_COLOR = Rgba(255, 0, 0, 100)
ACTIVE_PATH_COLOR = Rgba(255, 80, 80, 100)


class DrawingsGenerator:
    """
    Generate drawn objects for the F10 map and mission editor
    """

    def __init__(self, mission: Mission, game: Game) -> None:
        self.mission = mission
        self.game = game
        self.player_layer = self.mission.drawings.get_layer(StandardLayer.Blue)

    def generate_cps_markers(self) -> None:
        """
        Generate cps as circles
        """
        for cp in self.game.theater.controlpoints:
            if cp.captured:
                color = CP_BLUE
            else:
                color = CP_RED
            shape = self.player_layer.add_circle(
                cp.position,
                CP_CIRCLE_RADIUS,
                line_thickness=2,
                color=WHITE,
                fill=color,
                line_style=LineStyle.Dot,
            )
            shape.name = cp.name

    def generate_routes(self) -> None:
        """
        Generate routes drawing between cps
        """
        seen = set()
        for cp in self.game.theater.controlpoints:
            seen.add(cp)
            for destination, convoy_route in cp.convoy_routes.items():
                if destination in seen:
                    continue
                else:

                    # Determine path color
                    if cp.captured and destination.captured:
                        color = BLUE_PATH_COLOR
                    elif not cp.captured and not destination.captured:
                        color = RED_PATH_COLOR
                    else:
                        color = ACTIVE_PATH_COLOR

                    # Add shape to layer
                    shape = self.player_layer.add_line_segments(
                        cp.position,
                        [Point(0, 0, self.game.theater.terrain)]
                        + [p - cp.position for p in convoy_route]
                        + [destination.position - cp.position],
                        line_thickness=6,
                        color=color,
                        line_style=LineStyle.Solid,
                    )
                    shape.name = "path from " + cp.name + " to " + destination.name

    def generate_frontlines_drawing(self) -> None:
        """
        Generate a frontline "line" for each active frontline
        """
        for front_line in self.game.theater.conflicts():
            bounds = FrontLineConflictDescription.frontline_bounds(
                front_line, self.game.theater
            )

            end_point = bounds.left_position.point_from_heading(
                bounds.heading_from_left_to_right.degrees, bounds.length
            )
            shape = self.player_layer.add_line_segment(
                bounds.left_position,
                end_point - bounds.left_position,
                line_thickness=16,
                color=FRONTLINE_COLORS,
                line_style=LineStyle.Triangle,
            )
            shape.name = front_line.name

    def generate(self) -> None:
        self.generate_frontlines_drawing()
        self.generate_routes()
        self.generate_cps_markers()
