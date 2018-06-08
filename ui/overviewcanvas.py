from tkinter import *
from tkinter.ttk import *

from ui.window import *

from game.game import *
from theater.conflicttheater import *


class OverviewCanvas:
    mainmenu = None  # type: ui.mainmenu.MainMenu

    def __init__(self, frame: Frame, parent, game: Game):
        self.canvas = Canvas(frame, width=616, height=350)
        self.canvas.grid(column=0, row=0, sticky=NSEW)
        self.image = PhotoImage(file="resources/caumap.gif")
        self.parent = parent

        self.game = game

    def cp_coordinates(self, cp: ControlPoint) -> (int, int):
        point_a = list(self.game.theater.reference_points.keys())[0]
        point_a_img = self.game.theater.reference_points[point_a]

        point_b = list(self.game.theater.reference_points.keys())[1]
        point_b_img = self.game.theater.reference_points[point_b]

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

    def create_cp_title(self, coords, cp: ControlPoint):
        title = cp.name
        font = ("Helvetica", 13)

        self.canvas.create_text(coords[0]+1, coords[1]+1, text=title, fill='white', font=font)
        self.canvas.create_text(coords[0], coords[1], text=title, font=font)

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

                self.canvas.create_line((coords[0], coords[1], connected_coords[0], connected_coords[1]), width=2, fill=color)

        for cp in self.game.theater.controlpoints:
            coords = self.cp_coordinates(cp)
            arc_size = 18 * math.pow(cp.importance, 1)
            extent = max(cp.base.strength * 180, 10)
            start = (180 - extent) / 2
            color = cp.captured and 'blue' or 'red'

            cp_id = self.canvas.create_arc((coords[0] - arc_size/2, coords[1] - arc_size/2),
                                           (coords[0]+arc_size/2, coords[1]+arc_size/2),
                                           fill=color,
                                           style=PIESLICE,
                                           start=start,
                                           extent=extent)
            self.canvas.tag_bind(cp_id, "<Button-1>", self.display(cp))
            self.create_cp_title((coords[0] + arc_size/2, coords[1] + arc_size/2), cp)
            self.canvas.create_text(coords[0], coords[1] - arc_size / 1.5, text="8/4/2", font=("Helvetica", 10))

    def display(self, cp: ControlPoint):
        def action(_):
            return self.parent.go_cp(cp)

        return action

