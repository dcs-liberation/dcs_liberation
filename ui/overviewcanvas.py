import os

from tkinter import *

from tkinter.ttk import *

from ui.window import *
import pygame, platform
from threading import Thread

from game.game import *
from gen.conflictgen import Conflict
from theater.conflicttheater import *


class OverviewCanvas:
    mainmenu = None  # type: ui.mainmenu.MainMenu

    RED = (255,125,125)
    BLUE = (164,164,255)

    def __init__(self, frame: Frame, parent, game: Game):

        self.parent = parent
        self.game = game
        self.screen = None
        print(pygame.font.get_fonts())

        # Pygame objects
        self.map = None
        self.surface = None
        self.thread = None
        self.clock = pygame.time.Clock();
        pygame.font.init();
        self.font = pygame.font.SysFont("arial", 18)

        # Map state
        self.zoom = 10
        self.scroll = [0, 0]

        self.exited = False

        # self.image = PhotoImage(file=os.path.join("resources", game.theater.overview_image))
        # self.canvas = Canvas(frame, width=self.image.width(), height=self.image.height())
        # self.canvas.grid(column=0, row=0, sticky=NSEW)

        # TODO : dirty :(
        parent.window.tk.protocol("<WM_DELETE_WINDOW>", self.on_close)

        self.embed = Frame(frame, width=800, height=600)  # creates embed frame for pygame window
        self.embed.grid(column=0, row=0, sticky=NSEW)  # Adds grid
        self.embed.pack(side=LEFT)  # packs window to the left

        self.init_sdl_layer()
        self.init_sdl_thread()

    def on_close(self):
        print("on_close")

        self.exited = True
        if self.thread is not None:
            self.thread.join()

    def init_sdl_layer(self):
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        #if platform.system == "Windows":
        #    os.environ['SDL_VIDEODRIVER'] = 'windib'

        self.screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF|pygame.HWSURFACE)
        self.screen.fill(pygame.Color(0, 128, 128))
        self.screen.set_alpha(None)

        self.map = pygame.image.load(os.path.join("resources", self.game.theater.overview_image)).convert()
        self.surface = pygame.Surface((self.map.get_width(), self.map.get_height()))

        pygame.display.init()
        pygame.display.update()

    def init_sdl_thread(self):

        # tk = Tk()
        # tk.winfo_ismapped()

        self.thread = Thread(target=self.sdl_thread)
        self.thread.start()

    def sdl_thread(self):
        redraw_required = True
        while not self.exited:

            try:
                self.parent.window.tk.winfo_ismapped()
            except:
                self.exited = True

            self.clock.tick(60)

            if(redraw_required):
                # Fill
                self.screen.fill(pygame.Color(0, 128, 128))

                # Surface
                self.draw_map(self.surface);

                # Scaling
                scaled = pygame.transform.scale(self.surface, (int(self.surface.get_width() * self.zoom), int(self.surface.get_height() * self.zoom)))
                self.screen.blit(scaled, self.scroll)

                pygame.display.flip()

            redraw_required = False

            right_down = False
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Scroll wheel
                    if event.button == 4:
                        self.zoom += 0.25
                        redraw_required = True
                    elif event.button == 5:
                        self.zoom -= 0.25
                        redraw_required = True

                    if event.button == 3:
                        right_down = True
                        pygame.mouse.get_rel()

            # If Right click pressed
            if pygame.mouse.get_pressed()[2] == 1 and not right_down:
                scr = pygame.mouse.get_rel()
                self.scroll[0] += scr[0]
                self.scroll[1] += scr[1]
                redraw_required = True

            if (self.zoom <= 1):
                self.zoom = 1
            elif (self.zoom > 20):
                self.zoom = 20

    def draw_map(self, surface: pygame.Surface):

        self.surface.blit(self.map, (0,0))

        for cp in self.game.theater.controlpoints:

            for ground_object in cp.ground_objects:
                x, y = self.transform_point(ground_object.position)
                label = self.font.render(ground_object.name_abbrev, False, (0,0,0) if ground_object.is_dead else self._enemy_color())
                surface.blit(label, (x,y))

            coords = self.transform_point(cp.position)
            for connected_cp in cp.connected_points:
                connected_coords = self.transform_point(connected_cp.position)
                if connected_cp.captured != cp.captured:
                    color = self._enemy_color()
                elif connected_cp.captured and cp.captured:
                    color = self._player_color()
                else:
                    color = (0,0,0)

                pygame.draw.line(surface, color, coords, connected_coords, 4)
                #self.canvas.create_line((coords[0], coords[1], connected_coords[0], connected_coords[1]), width=2, fill=color)

                if cp.captured and not connected_cp.captured and Conflict.has_frontline_between(cp, connected_cp):
                    frontline = Conflict.frontline_vector(cp, connected_cp, self.game.theater)
                    if not frontline:
                        continue

                    frontline_pos, heading, distance = frontline
                    if distance < 10000:
                        frontline_pos = frontline_pos.point_from_heading(heading + 180, 5000)
                        distance = 10000

                    start_coords = self.transform_point(frontline_pos, treshold=10)
                    end_coords = self.transform_point(frontline_pos.point_from_heading(heading, distance), treshold=60)

                    #self.canvas.create_line((*start_coords, *end_coords), width=2, fill=color)
                    pygame.draw.line(surface, color, start_coords, end_coords, 4)

        for cp in self.game.theater.controlpoints:
            coords = self.transform_point(cp.position)
            radius = 12 * math.pow(cp.importance, 1)
            radius_m = radius * cp.base.strength - 2;

            if cp.captured:
                color = self._player_color()
            else:
                color = self._enemy_color()

            pygame.draw.circle(surface, (0,0,0), (int(coords[0]), int(coords[1])), int(radius))
            pygame.draw.circle(surface, color, (int(coords[0]), int(coords[1])), int(radius_m))

            #self.canvas.tag_bind(cp_id, "<Button-1>", self.display(cp))
            #self.create_cp_title((coords[0] + arc_size/4, coords[1] + arc_size/4), cp)

            units_title = "{}/{}/{}".format(cp.base.total_planes, cp.base.total_armor, cp.base.total_aa)

            label = self.font.render(cp.name, False, color, (0,0,0))
            surface.blit(label, (coords[0]-label.get_width()/2, coords[1]))

            #self.canvas.create_text(coords[0]+1, coords[1] - arc_size / 1.5 +1, text=units_title, font=("Helvetica", 8), fill=color)
            #self.canvas.create_text(coords[0], coords[1] - arc_size / 1.5, text=units_title, font=("Helvetica", 8), fill="white")

            #id = self.canvas.create_text(coords[0], coords[1], text=title, font=font)


            """cp_id = self.canvas.create_arc((coords[0] - arc_size/2, coords[1] - arc_size/2),
                                           (coords[0] + arc_size/2, coords[1] + arc_size/2),
                                           fill=color,
                                           style=PIESLICE,
                                           start=start,
                                           extent=extent)"""


    def transform_point(self, p: Point, treshold=30) -> (int, int):
        point_a = list(self.game.theater.reference_points.keys())[0]
        point_a_img = self.game.theater.reference_points[point_a]

        point_b = list(self.game.theater.reference_points.keys())[1]
        point_b_img = self.game.theater.reference_points[point_b]

        Y_dist = point_a_img[0] - point_b_img[0]
        lon_dist = point_a[1] - point_b[1]

        X_dist = point_a_img[1] - point_b_img[1]
        lat_dist = point_b[0] - point_a[0]

        Y_scale = float(Y_dist) / float(lon_dist)
        X_scale = float(X_dist) / float(lat_dist)

        # ---
        Y_offset = p.x - point_a[0]
        X_offset = p.y - point_a[1]

        X = point_b_img[1] + X_offset * X_scale
        Y = point_a_img[0] - Y_offset * Y_scale

        return X > treshold and X or treshold, Y > treshold and Y or treshold

    def create_cp_title(self, coords, cp: ControlPoint):
        title = cp.name
        font = ("Helvetica", 10)

        id = self.canvas.create_text(coords[0], coords[1], text=title, font=font)
        self.canvas.tag_bind(id, "<Button-1>", self.display(cp))

        id = self.canvas.create_text(coords[0] + 1, coords[1] + 1, text=title, fill='white', font=font)
        self.canvas.tag_bind(id, "<Button-1>", self.display(cp))

    def _player_color(self):
        return self.game.player == "USA" and self.BLUE or self.RED

    def _enemy_color(self):
        return self.game.player == "USA" and self.RED or self.BLUE

    def update(self):

        self.screen.blit(self.map, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.zoom += 1
                elif event.button == 5:
                    self.zoom -= 1
        pygame.display.update()

        """
        self.canvas.delete(ALL)
        self.canvas.create_image((self.image.width()/2, self.image.height()/2), image=self.image)

        for cp in self.game.theater.controlpoints:
            for ground_object in cp.ground_objects:
                x, y = self.transform_point(ground_object.position)
                self.canvas.create_text(x,
                                        y,
                                        text=".",
                                        fill="black" if ground_object.is_dead else self._enemy_color(),
                                        font=("Helvetica", 18))

            coords = self.transform_point(cp.position)
            for connected_cp in cp.connected_points:
                connected_coords = self.transform_point(connected_cp.position)
                if connected_cp.captured != cp.captured:
                    color = self._enemy_color()
                elif connected_cp.captured and cp.captured:
                    color = self._player_color()
                else:
                    color = "black"

                self.canvas.create_line((coords[0], coords[1], connected_coords[0], connected_coords[1]), width=2, fill=color)

                if cp.captured and not connected_cp.captured and Conflict.has_frontline_between(cp, connected_cp):
                    frontline = Conflict.frontline_vector(cp, connected_cp, self.game.theater)
                    if not frontline:
                        continue

                    frontline_pos, heading, distance = frontline
                    if distance < 10000:
                        frontline_pos = frontline_pos.point_from_heading(heading + 180, 5000)
                        distance = 10000

                    start_coords = self.transform_point(frontline_pos, treshold=10)
                    end_coords = self.transform_point(frontline_pos.point_from_heading(heading, distance), treshold=60)

                    self.canvas.create_line((*start_coords, *end_coords), width=2, fill=color)

        for cp in self.game.theater.controlpoints:
            coords = self.transform_point(cp.position)
            arc_size = 16 * math.pow(cp.importance, 1)
            extent = max(cp.base.strength * 180, 10)
            start = (180 - extent) / 2

            if cp.captured:
                color = self._player_color()
            else:
                color = self._enemy_color()

            cp_id = self.canvas.create_arc((coords[0] - arc_size/2, coords[1] - arc_size/2),
                                           (coords[0] + arc_size/2, coords[1] + arc_size/2),
                                           fill=color,
                                           style=PIESLICE,
                                           start=start,
                                           extent=extent)

        """
        """
            for r in cp.radials:
                p = self.transform_point(cp.position.point_from_heading(r, 20000))
                self.canvas.create_text(p[0], p[1], text="{}".format(r))
            continue
        """

        """
            self.canvas.tag_bind(cp_id, "<Button-1>", self.display(cp))
            self.create_cp_title((coords[0] + arc_size/4, coords[1] + arc_size/4), cp)

            units_title = "{}/{}/{}".format(cp.base.total_planes, cp.base.total_armor, cp.base.total_aa)
            self.canvas.create_text(coords[0]+1, coords[1] - arc_size / 1.5 +1, text=units_title, font=("Helvetica", 8), fill=color)
            self.canvas.create_text(coords[0], coords[1] - arc_size / 1.5, text=units_title, font=("Helvetica", 8), fill="white")
        """

    def display(self, cp: ControlPoint):
        def action(_):
            return self.parent.go_cp(cp)

        return action
