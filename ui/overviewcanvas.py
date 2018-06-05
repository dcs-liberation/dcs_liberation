from tkinter import *
from tkinter.ttk import *

from ui.window import *

from game.game import *


class OverviewCanvas:
    def __init__(self, frame: Frame, game: Game):
        self.canvas = Canvas(frame, width=600, height=400)
        self.canvas.grid(column=0, row=0, sticky=NSEW)
        self.image = PhotoImage(file="resources/caumap.gif")

        self.game = game

    def cp_coordinates(self, cp: ControlPoint) -> (int, int):
        point_a = (-317948.32727306, 635639.37385346)
        point_a_img = 361 - 60, 306 + 20

        point_b = (-355692.3067714, 617269.96285781)
        point_b_img = 345 - 59.5, 339 + 19.5

        x_dist = point_a_img[0] - point_b_img[0]
        lon_dist = point_a[1] - point_b[1]

        y_dist = point_a_img[1] - point_b_img[1]
        lat_dist = point_b[0] - point_a[0]

        x_scale = float(x_dist) / float(lon_dist)
        y_scale = float(y_dist) / float(lat_dist)

        # ---
        x_offset = cp.position.x - point_a[0]
        y_offset = cp.position.y - point_a[1]

        return point_b_img[1] + y_offset * y_scale, point_a_img[0] - x_offset * x_scale

    def update(self):
        self.canvas.delete(ALL)
        self.canvas.create_image((self.image.width()/2, self.image.height()/2), image=self.image)

        for cp in self.game.theater.controlpoints:
            coords = self.cp_coordinates(cp)
            for connected_cp in cp.connected_points:
                connected_coords = self.cp_coordinates(connected_cp)
                if connected_cp.captured != cp.captured:
                    color = "red"
                elif connected_cp.captured and cp.captured:
                    color = "blue"
                else:
                    color = "black"

                self.canvas.create_line((coords[0], coords[1], connected_coords[0], connected_coords[1]), width=3, fill=color)

        for cp in self.game.theater.controlpoints:
            coords = self.cp_coordinates(cp)
            arc_size = 12 * math.pow(cp.importance, 1)
            self.canvas.create_arc((coords[0] - arc_size/2, coords[1] - arc_size/2),
                                   (coords[0]+arc_size, coords[1]+arc_size),
                                   fill='red')

