import os

from tkinter import *

from tkinter.ttk import *

from ui.styles import STYLES
from ui.window import *
import pygame, platform
from threading import Thread

from game.game import *
from gen.conflictgen import Conflict
from theater.conflicttheater import *


class OverviewCanvas:
    mainmenu = None  # type: ui.mainmenu.MainMenu

    RED = (255, 125, 125)
    BLUE = (164, 164, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BACKGROUND = pygame.Color(0, 64, 64)
    ANTIALIASING = True

    def __init__(self, frame: Frame, parent, game: Game):

        self.parent = parent
        self.game = game

        # Pygame objects
        self.map = None
        self.screen = None
        self.surface: pygame.Surface = None
        self.thread: Thread = None
        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 15)
        self.fontsmall = pygame.font.SysFont("arial", 10)

        # Frontline are too heavy on performance to compute in realtime, so keep them in a cache
        self.frontline_vector_cache = {}

        # Map state
        self.zoom = 1
        self.scroll = [0, 0]
        self.exited = False

        # Display options
        self.display_ground_targets = BooleanVar(value=True)
        self.display_forces = BooleanVar(value=True)
        self.display_bases = BooleanVar(value=True)
        self.display_road = BooleanVar(value=True)

        parent.window.tk.protocol("<WM_DELETE_WINDOW>", self.on_close)

        self.wrapper = Frame(frame, **STYLES["frame-wrapper"])
        self.wrapper.grid(column=0, row=0, sticky=NSEW)  # Adds grid
        self.wrapper.pack(side=LEFT)  # packs window to the left

        self.embed = Frame(self.wrapper, width=1066, height=600, borderwidth=2, **STYLES["frame-wrapper"])
        self.embed.grid(column=0, row=0, sticky=NSEW)  # Adds grid

        self.options = Frame(self.wrapper, borderwidth=2, **STYLES["frame-wrapper"])
        self.options.grid(column=0, row=1, sticky=NSEW)
        self.build_map_options_panel()

        self.init_sdl_layer()
        self.init_sdl_thread()

    def build_map_options_panel(self):
        col = 0
        Label(self.options, text="Ground targets", **STYLES["widget"]).grid(row=0, column=col, sticky=W)
        Checkbutton(self.options, variable=self.display_ground_targets, **STYLES["radiobutton"]).grid(row=0,
                                                                                                      column=col + 1,                                                                                        sticky=E)
        Separator(self.options, orient=VERTICAL).grid(row=0, column=col + 2, sticky=NS)
        col += 3
        Label(self.options, text="Forces", **STYLES["widget"]).grid(row=0, column=col, sticky=W)
        Checkbutton(self.options, variable=self.display_forces, **STYLES["radiobutton"]).grid(row=0, column=col + 1,
                                                                                              sticky=E)
        Separator(self.options, orient=VERTICAL).grid(row=0, column=col + 2, sticky=NS)
        col += 3
        Label(self.options, text="Bases", **STYLES["widget"]).grid(row=0, column=col, sticky=W)
        Checkbutton(self.options, variable=self.display_bases, **STYLES["radiobutton"]).grid(row=0, column=col + 1,
                                                                                             sticky=E)
        Separator(self.options, orient=VERTICAL).grid(row=0, column=col + 2, sticky=NS)
        col += 4
        Label(self.options, text="Roads", **STYLES["widget"]).grid(row=0, column=col, sticky=W)
        Checkbutton(self.options, variable=self.display_road, **STYLES["radiobutton"]).grid(row=0, column=col + 1,
                                                                                            sticky=E)
        Separator(self.options, orient=VERTICAL).grid(row=0, column=col + 2, sticky=NS)
        col += 4
        Label(self.options,
              text="[ Use mouse wheel to zoom, right mouse click + move to pan the map view, click on one of your base to manage it ]",
              **STYLES["widget"]).grid(row=0, column=col, sticky=W)

    def on_close(self):
        print("on_close")
        self.exited = True
        if self.thread is not None:
            self.thread.join()

    def init_sdl_layer(self):
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        if platform.system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'

        self.screen = pygame.display.set_mode((1066, 600), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.screen.fill(pygame.Color(0, 128, 128))
        self.screen.set_alpha(None)

        self.icon_tg = pygame.image.load(os.path.join("resources", "ui", "target.png"))
        self.icon_sam = pygame.image.load(os.path.join("resources", "ui", "sam.png"))
        self.icon_clr = pygame.image.load(os.path.join("resources", "ui", "cleared.png"))

        self.map = pygame.image.load(os.path.join("resources", self.game.theater.overview_image)).convert()
        pygame.draw.rect(self.map, self.BLACK, (0, 0, self.map.get_width(), self.map.get_height()), 10)
        pygame.draw.rect(self.map, self.WHITE, (0, 0, self.map.get_width(), self.map.get_height()), 5)
        self.surface = pygame.Surface((self.map.get_width(), self.map.get_height()))

        pygame.display.init()
        pygame.display.update()

    def init_sdl_thread(self):
        self.thread = Thread(target=self.sdl_thread)
        self.thread.start()

    def sdl_thread(self):
        self.redraw_required = True
        i = 0
        while not self.exited:
            self.clock.tick(60)
            self.draw()
            i += 1

            if i == 300:
                self.frontline_vector_cache = {}
                i = 300

    def draw(self):

        try:
            self.parent.window.tk.winfo_ismapped()
        except:
            self.exited = True

        right_down = False
        left_down = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                self.redraw_required = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Scroll wheel
                if event.button == 4:
                    self.zoom += 0.25
                    self.redraw_required = True
                elif event.button == 5:
                    self.zoom -= 0.25
                    self.redraw_required = True

                if event.button == 3:
                    right_down = True
                    pygame.mouse.get_rel()
                if event.button == 1:
                    left_down = True
                    self.redraw_required = True

        # If Right click pressed
        if pygame.mouse.get_pressed()[2] == 1 and not right_down:
            scr = pygame.mouse.get_rel()
            self.scroll[0] += scr[0]
            self.scroll[1] += scr[1]
            self.redraw_required = True

        if self.zoom <= 0.5:
            self.zoom = 0.5
        elif self.zoom > 10:
            self.zoom = 10

        if (self.redraw_required):
            # Fill
            self.screen.fill(self.BACKGROUND)

            # Surface
            cursor_pos = pygame.mouse.get_pos()
            cursor_pos = (
                (cursor_pos[0] - self.scroll[0]) / self.zoom, (cursor_pos[1] - self.scroll[1]) / self.zoom)
            self.draw_map(self.surface, cursor_pos, (left_down, right_down));

            # Scaling
            scaled = pygame.transform.scale(self.surface, (
            int(self.surface.get_width() * self.zoom), int(self.surface.get_height() * self.zoom)))
            self.screen.blit(scaled, self.scroll)

            pygame.display.flip()

        self.redraw_required = False

    def draw_map(self, surface: pygame.Surface, mouse_pos: (int, int), mouse_down: (bool, bool)):

        self.surface.blit(self.map, (0, 0))

        # Debug
        # pygame.draw.rect(surface, (255, 0, 255), (mouse_pos[0], mouse_pos[1], 5, 5), 2)

        for cp in self.game.theater.controlpoints:

            if self.display_ground_targets.get():
                if cp.captured:
                    color = self._player_color()
                else:
                    color = self._enemy_color()
                for ground_object in cp.ground_objects:
                    self.draw_ground_object(ground_object, surface, color, mouse_pos)

            if self.display_road.get():
                coords = self.transform_point(cp.position)
                for connected_cp in cp.connected_points:
                    connected_coords = self.transform_point(connected_cp.position)
                    if connected_cp.captured != cp.captured:
                        color = self._enemy_color()
                    elif connected_cp.captured and cp.captured:
                        color = self._player_color()
                    else:
                        color = self.BLACK

                    pygame.draw.line(surface, color, coords, connected_coords, 4)

                    if cp.captured and not connected_cp.captured and Conflict.has_frontline_between(cp, connected_cp):

                        # Cache mechanism to avoid performing frontline vector computation on every loop
                        frontline = None
                        hash = str(cp.id) + "_" + str(connected_cp.id)
                        if hash in self.frontline_vector_cache:
                            frontline = self.frontline_vector_cache[hash]
                        else:
                            frontline = Conflict.frontline_vector(cp, connected_cp, self.game.theater)
                            self.frontline_vector_cache[hash] = frontline

                        if not frontline:
                            continue

                        frontline_pos, heading, distance = frontline

                        if distance < 10000:
                            frontline_pos = frontline_pos.point_from_heading(heading + 180, 5000)
                            distance = 10000

                        start_coords = self.transform_point(frontline_pos, treshold=10)
                        end_coords = self.transform_point(frontline_pos.point_from_heading(heading, distance),
                                                          treshold=60)

                        pygame.draw.line(surface, color, start_coords, end_coords, 4)

        if self.display_bases.get():
            for cp in self.game.theater.controlpoints:
                coords = self.transform_point(cp.position)
                radius = 12 * math.pow(cp.importance, 1)
                radius_m = radius * cp.base.strength - 2

                if cp.captured:
                    color = self._player_color()
                else:
                    color = self._enemy_color()

                pygame.draw.circle(surface, self.BLACK, (int(coords[0]), int(coords[1])), int(radius))
                pygame.draw.circle(surface, color, (int(coords[0]), int(coords[1])), int(radius_m))

                label = self.font.render(cp.name, self.ANTIALIASING, (225, 225, 225), self.BLACK)
                labelHover = self.font.render(cp.name, self.ANTIALIASING, (255, 255, 255), (128, 186, 128))
                labelClick = self.font.render(cp.name, self.ANTIALIASING, (255, 255, 255), (122, 122, 255))

                rect = pygame.Rect(coords[0] - label.get_width() / 2 + 1, coords[1] + 1, label.get_width(),
                                   label.get_height())

                if rect.collidepoint(mouse_pos):
                    if (mouse_down[0]):
                        surface.blit(labelClick, (coords[0] - label.get_width() / 2 + 1, coords[1] + 1))
                        self.parent.go_cp(cp)
                    else:
                        surface.blit(labelHover, (coords[0] - label.get_width() / 2 + 1, coords[1] + 1))
                else:
                    surface.blit(label, (coords[0] - label.get_width() / 2 + 1, coords[1] + 1))

                if self.display_forces.get():
                    units_title = " {} / {} / {} ".format(cp.base.total_planes, cp.base.total_armor, cp.base.total_aa)
                    label2 = self.fontsmall.render(units_title, self.ANTIALIASING, color, (30, 30, 30))
                    surface.blit(label2, (coords[0] - label2.get_width() / 2, coords[1] + label.get_height() + 1))

    def draw_ground_object(self, ground_object: TheaterGroundObject, surface: pygame.Surface, color, mouse_pos):
        x, y = self.transform_point(ground_object.position)
        rect = pygame.Rect(x, y, 16, 16)

        if ground_object.is_dead:
            surface.blit(self.icon_clr, (x, y))
        else:
            if ground_object.name_abbrev == "AA":
                surface.blit(self.icon_sam, (x, y))
            else:
                surface.blit(self.icon_tg, (x, y))

        if rect.collidepoint(mouse_pos):
            self.draw_ground_object_info(ground_object, (x, y), color, surface);

    def render_roads(self):
        # Note : This is really slow. Viewport is much smoother when not rendering line.
        pass

    def draw_ground_object_info(self, ground_object: TheaterGroundObject, pos, color, surface: pygame.Surface):
        lb = self.font.render("Type : " + ground_object.name_abbrev, self.ANTIALIASING, color, self.BLACK);
        surface.blit(lb, (pos[0] + 18, pos[1]))

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

    def _player_color(self):
        return self.game.player == "USA" and self.BLUE or self.RED

    def _enemy_color(self):
        return self.game.player == "USA" and self.RED or self.BLUE

    def update(self):
        self.draw()

    def display(self, cp: ControlPoint):
        def action(_):
            return self.parent.go_cp(cp)

        return action
