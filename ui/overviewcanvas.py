import os
import platform
from threading import Thread
from tkinter.ttk import *

import pygame

from theater.theatergroundobject import CATEGORY_MAP
from ui.styles import STYLES
from ui.window import *


EVENT_DEPARTURE_MAX_DISTANCE = 250000


class OverviewCanvas:
    mainmenu = None  # type: ui.mainmenu.MainMenu

    BRIGHT_RED = (200, 64, 64)
    BRIGHT_GREEN = (64, 200, 64)

    RED = (255, 125, 125)
    BLUE = (164, 164, 255)
    DARK_BLUE = (45, 62, 80)
    WHITE = (255, 255, 255)
    GREEN = (128, 186, 128)
    BLACK = (0, 0, 0)
    BACKGROUND = pygame.Color(0, 64, 64)
    ANTIALIASING = True

    WIDTH = 1066
    HEIGHT = 600

    started = None
    selected_event_info = None  # type: typing.Tuple[Event, typing.Tuple[int, int]]
    frontline_vector_cache = None  # type: typing.Dict[str, typing.Tuple[Point, int, int]]

    def __init__(self, frame: Frame, parent, game: Game):

        self.parent = parent
        self.game = game

        # Remove any previously existing pygame instance
        pygame.quit()

        # Pygame objects
        self.map = None
        self.screen = None
        self.surface: pygame.Surface = None
        self.thread: Thread = None
        self.clock = pygame.time.Clock()
        self.expanded = True

        pygame.font.init()
        self.font: pygame.font.SysFont = pygame.font.SysFont("arial", 15)
        self.fontsmall: pygame.font.SysFont = pygame.font.SysFont("arial", 10)
        self.icons = {}

        # Frontline are too heavy on performance to compute in realtime, so keep them in a cache
        self.frontline_vector_cache = {}

        # Map state
        self.redraw_required = True
        self.zoom = 1
        self.scroll = [0, 0]
        self.exited = False

        # Display options
        self.display_ground_targets = BooleanVar(value=True)
        self.display_forces = BooleanVar(value=True)
        self.display_bases = BooleanVar(value=True)
        self.display_road = BooleanVar(value=True)
        self.display_rules = self.compute_display_rules()

        parent.window.tk.protocol("<WM_DELETE_WINDOW>", self.on_close)

        self.wrapper = Frame(frame, **STYLES["frame-wrapper"])
        self.wrapper.grid(column=0, row=0, sticky=NSEW)  # Adds grid
        self.wrapper.pack(side=LEFT)  # packs window to the left

        self.embed = Frame(self.wrapper, width=self.WIDTH, height=self.HEIGHT, borderwidth=2, **STYLES["frame-wrapper"])
        self.embed.grid(column=0, row=0, sticky=NSEW)  # Adds grid

        self.options = Frame(self.wrapper, borderwidth=2, **STYLES["frame-wrapper"])
        self.options.grid(column=0, row=1, sticky=NSEW)
        self.build_map_options_panel()

        self.init_sdl_layer()
        self.init_sdl_thread()

    def build_map_options_panel(self):
        def force_redraw():
            if self.screen:
                self.redraw_required = True
                self.draw()

        col = 0
        Label(self.options, text="Bases", **STYLES["widget"]).grid(row=0, column=col, sticky=W)
        Checkbutton(self.options, variable=self.display_bases, **STYLES["radiobutton"]).grid(row=0, column=col + 1,
                                                                                             sticky=E)
        Separator(self.options, orient=VERTICAL).grid(row=0, column=col + 2, sticky=NS)
        col += 3
        Label(self.options, text="Roads", **STYLES["widget"]).grid(row=0, column=col, sticky=W)
        Checkbutton(self.options, variable=self.display_road, **STYLES["radiobutton"]).grid(row=0, column=col + 1,
                                                                                            sticky=E)
        Separator(self.options, orient=VERTICAL).grid(row=0, column=col + 2, sticky=NS)
        col += 3
        Label(self.options, text="Strike targets", **STYLES["widget"]).grid(row=0, column=col, sticky=W)
        Checkbutton(self.options, variable=self.display_ground_targets, **STYLES["radiobutton"]).grid(row=0,
                                                                                                      column=col + 1,
                                                                                                      sticky=E)
        Separator(self.options, orient=VERTICAL).grid(row=0, column=col + 2, sticky=NS)
        col += 3
        Label(self.options, text="Forces", **STYLES["widget"]).grid(row=0, column=col, sticky=W)
        Checkbutton(self.options, variable=self.display_forces, **STYLES["radiobutton"]).grid(row=0, column=col + 1,
                                                                                              sticky=E)
        Separator(self.options, orient=VERTICAL).grid(row=0, column=col + 2, sticky=NS)
        col += 4
        Button(self.options, text="Toggle size", command=lambda: self.map_size_toggle(), **STYLES["btn-primary"]).grid(row=0, column=col, sticky=E, padx=(10,10))

    def map_size_toggle(self):
        if self.expanded:
            self.embed.configure(width=0)
            self.options.configure(width=0)
            self.expanded = False
        else:
            self.embed.configure(width=self.WIDTH)
            self.options.configure(width=self.WIDTH)
            self.expanded = True

    def on_close(self):
        self.exited = True
        if self.thread is not None:
            self.thread.join()

    def init_sdl_layer(self):
        # Setup pygame to run in tk frame
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        if platform.system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'

        # Create pygame 'screen'
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.screen.fill(pygame.Color(*self.BLACK))

        # Load icons resources
        self.icons = {}
        self.icons["target"] = pygame.image.load(os.path.join("resources", "ui", "target.png"))
        self.icons["cleared"] = pygame.image.load(os.path.join("resources", "ui", "cleared.png"))
        for category in CATEGORY_MAP.keys():
            try:
                self.icons[category] = pygame.image.load(os.path.join("resources", "ui", category + ".png"))
            except:
                print("Couldn't load icon for : " + category)

        # Load the map image
        self.map = pygame.image.load(os.path.join("resources", self.game.theater.overview_image)).convert()
        pygame.draw.rect(self.map, self.BLACK, (0, 0, self.map.get_width(), self.map.get_height()), 10)
        pygame.draw.rect(self.map, self.WHITE, (0, 0, self.map.get_width(), self.map.get_height()), 5)

        # Create surfaces for drawing
        self.surface = pygame.Surface((self.map.get_width(), self.map.get_height()))
        self.surface.set_alpha(None)
        self.overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)

        # Init pygame display
        pygame.display.init()
        pygame.display.update()

    def init_sdl_thread(self):
        if OverviewCanvas.started is not None:
            OverviewCanvas.started.exited = True
        self.thread = Thread(target=self.sdl_thread)
        self.thread.start()
        OverviewCanvas.started = self
        print("Started SDL app")

    def sdl_thread(self):
        self.redraw_required = True
        i = 0
        while not self.exited:
            self.clock.tick(60)
            self.draw()
            i += 1
            if i == 300:
                self.frontline_vector_cache = {}
                i = 0
        print("Stopped SDL app")

    def draw(self):
        try:
            self.embed.winfo_ismapped()
            self.embed.winfo_manager()
        except:
            self.exited = True

        right_down = False
        left_down = False

        # Detect changes on display rules
        r = self.compute_display_rules()
        if r != self.display_rules:
            self.display_rules = r
            self.redraw_required = True

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

        if self.redraw_required:
            # Fill
            self.screen.fill(self.BACKGROUND)
            self.overlay.fill(pygame.Color(0, 0, 0, 0))

            # Surface
            cursor_pos = pygame.mouse.get_pos()
            cursor_pos = (
                cursor_pos[0] / self.zoom - self.scroll[0], cursor_pos[1] / self.zoom - self.scroll[1])
            self.draw_map(self.surface, self.overlay, cursor_pos, [left_down, right_down])

            # Scaling
            scaled = pygame.transform.scale(self.surface, (
                int(self.surface.get_width() * self.zoom), int(self.surface.get_height() * self.zoom)))
            self.screen.blit(scaled, (self.scroll[0]*self.zoom, self.scroll[1]*self.zoom))
            self.screen.blit(self.overlay, (0, 0))

            pygame.display.flip()

        self.redraw_required = False

    def draw_map(self, surface: pygame.Surface, overlay: pygame.Surface, mouse_pos: (int, int), mouse_down: [bool, bool]):
        self.surface.blit(self.map, (0, 0))

        # Display zoom level on overlay
        zoom_lvl = self.font.render("  x " + str(self.zoom) + "  ", self.ANTIALIASING, self.WHITE, self.DARK_BLUE)
        self.overlay.blit(zoom_lvl, (self.overlay.get_width()-zoom_lvl.get_width()-5,
                                     self.overlay.get_height()-zoom_lvl.get_height()-5))

        # Debug
        # pygame.draw.rect(surface, (255, 0, 255), (mouse_pos[0], mouse_pos[1], 5, 5), 2)

        for cp in self.game.theater.controlpoints:
            coords = self._transform_point(cp.position)

            if self.display_ground_targets.get():
                if cp.captured:
                    color = self._player_color()
                else:
                    color = self._enemy_color()
                for ground_object in cp.ground_objects:
                    x, y = self._transform_point(ground_object.position)
                    pygame.draw.line(surface, color, coords, (x + 8, y + 8), 1)
                    self.draw_ground_object(ground_object, surface, color, mouse_pos)

            if self.display_road.get():
                for connected_cp in cp.connected_points:
                    connected_coords = self._transform_point(connected_cp.position)
                    if connected_cp.captured != cp.captured:
                        color = self._enemy_color()
                    elif connected_cp.captured and cp.captured:
                        color = self._player_color()
                    else:
                        color = self.BLACK

                    pygame.draw.line(surface, color, coords, connected_coords, 2)

                    if cp.captured and not connected_cp.captured and Conflict.has_frontline_between(cp, connected_cp):
                        frontline = self._frontline_vector(cp, connected_cp)
                        if not frontline:
                            continue

                        frontline_pos, heading, distance = frontline

                        if distance < 10000:
                            frontline_pos = frontline_pos.point_from_heading(heading + 180, 5000)
                            distance = 10000

                        start_coords = self._transform_point(frontline_pos, treshold=10)
                        end_coords = self._transform_point(frontline_pos.point_from_heading(heading, distance),
                                                           treshold=60)

                        pygame.draw.line(surface, color, start_coords, end_coords, 4)

        if self.display_bases.get():
            mouse_down = self.draw_bases(mouse_pos, mouse_down)

        mouse_down = self.draw_events(self.surface, mouse_pos, mouse_down)

        if mouse_down[0]:
            self.selected_event_info = None

    def draw_bases(self, mouse_pos, mouse_down):
        for cp in self.game.theater.controlpoints:
            coords = self._transform_point(cp.position)
            radius = 12 * math.pow(cp.importance, 1)
            radius_m = radius * cp.base.strength - 2

            if cp.captured:
                color = self._player_color()
            else:
                color = self._enemy_color()

            pygame.draw.circle(self.surface, self.BLACK, (int(coords[0]), int(coords[1])), int(radius))
            pygame.draw.circle(self.surface, color, (int(coords[0]), int(coords[1])), int(radius_m))

            label = self.font.render(cp.name, self.ANTIALIASING, (225, 225, 225), self.BLACK)
            labelHover = self.font.render(cp.name, self.ANTIALIASING, (255, 255, 255), (128, 186, 128))
            labelClick = self.font.render(cp.name, self.ANTIALIASING, (255, 255, 255), (122, 122, 255))

            point =  coords[0] - label.get_width() / 2 + 1, coords[1] + 1
            rect = pygame.Rect(*point, label.get_width(), label.get_height())

            if rect.collidepoint(*mouse_pos):
                if mouse_down[0]:
                    self.surface.blit(labelClick, (coords[0] - label.get_width() / 2 + 1, coords[1] + 1))
                    self._selected_cp(cp)
                    mouse_down[0] = False
                else:
                    self.surface.blit(labelHover, (coords[0] - label.get_width() / 2 + 1, coords[1] + 1))

                self.draw_base_info(self.overlay, cp, (0, 0))
                if self.selected_event_info and cp.captured and self.selected_event_info[0].location.distance_to_point(cp.position) < EVENT_DEPARTURE_MAX_DISTANCE:
                    pygame.draw.line(self.surface, self.WHITE, point, self.selected_event_info[1])

            else:
                self.surface.blit(label, (coords[0] - label.get_width() / 2 + 1, coords[1] + 1))

            if self.display_forces.get():
                units_title = " {} / {} / {} ".format(cp.base.total_planes, cp.base.total_armor, cp.base.total_aa)
                label2 = self.fontsmall.render(units_title, self.ANTIALIASING, color, (30, 30, 30))
                self.surface.blit(label2, (coords[0] - label2.get_width() / 2, coords[1] + label.get_height() + 1))

        return mouse_down

    def draw_base_info(self, surface: pygame.Surface, control_point: ControlPoint, pos):
        title = self.font.render(control_point.name, self.ANTIALIASING, self.BLACK, self.GREEN)
        hp = self.font.render("Strength : ", self.ANTIALIASING, (225, 225, 225), self.BLACK)

        armor_txt = "ARMOR      >    "
        for key, value in control_point.base.armor.items():
            armor_txt += key.id + " x " + str(value) + " | "
        armor = self.font.render(armor_txt, self.ANTIALIASING, (225, 225, 225), self.BLACK)

        aircraft_txt = "AIRCRAFT >    "
        for key, value in control_point.base.aircraft.items():
            aircraft_txt += key.id + " x " + str(value) + " | "
        aircraft = self.font.render(aircraft_txt, self.ANTIALIASING, (225, 225, 225), self.BLACK)

        aa_txt = "AA/SAM       >    "
        for key, value in control_point.base.aa.items():
            aa_txt += key.id + " x " + str(value) + " | "
        aa = self.font.render(aa_txt, self.ANTIALIASING, (225, 225, 225), self.BLACK)

        lineheight = title.get_height()
        w = max([max([a.get_width() for a in [title, armor, aircraft, aa]]), 150])
        h = 5 * lineheight + 4 * 5

        # Draw frame
        pygame.draw.rect(surface, self.GREEN, (pos[0], pos[1], w + 8, h + 8))
        pygame.draw.rect(surface, self.BLACK, (pos[0] + 2, pos[1] + 2, w + 4, h + 4))
        pygame.draw.rect(surface, self.GREEN, (pos[0] + 2, pos[1], w + 4, lineheight + 4))

        # Title
        surface.blit(title, (pos[0] + 4, 4 + pos[1]))
        surface.blit(hp, (pos[0] + 4, 4 + pos[1] + lineheight + 5))

        # Draw gauge
        pygame.draw.rect(surface, self.WHITE,
                         (pos[0] + hp.get_width() + 3, 4 + pos[1] + lineheight + 5, 54, lineheight))
        pygame.draw.rect(surface, self.BRIGHT_RED,
                         (pos[0] + hp.get_width() + 5, 4 + pos[1] + lineheight + 5 + 2, 50, lineheight - 4))
        pygame.draw.rect(surface, self.BRIGHT_GREEN, (
            pos[0] + hp.get_width() + 5, 4 + pos[1] + lineheight + 5 + 2, 50 * control_point.base.strength, lineheight - 4))

        # Text
        surface.blit(armor, (pos[0] + 4, 4 + pos[1] + lineheight * 2 + 10))
        surface.blit(aircraft, (pos[0] + 4, 4 + pos[1] + lineheight * 3 + 15))
        surface.blit(aa, (pos[0] + 4, 4 + pos[1] + lineheight * 4 + 20))

    def draw_ground_object(self, ground_object: TheaterGroundObject, surface: pygame.Surface, color, mouse_pos):
        x, y = self._transform_point(ground_object.position)
        rect = pygame.Rect(x, y, 16, 16)

        if ground_object.is_dead:
            surface.blit(self.icons["cleared"], (x, y))
        else:
            if ground_object.category in self.icons.keys():
                icon = self.icons[ground_object.category]
            else:
                icon = self.icons["target"]
            surface.blit(icon, (x, y))

        if rect.collidepoint(*mouse_pos):
            self.draw_ground_object_info(ground_object, (x, y), color, surface)

    def draw_ground_object_info(self, ground_object: TheaterGroundObject, pos, color, surface: pygame.Surface):
        lb = self.font.render(str(ground_object), self.ANTIALIASING, color, self.BLACK)
        surface.blit(lb, (pos[0] + 18, pos[1]))

    def draw_events(self, surface: pygame.Surface, mouse_pos, mouse_down):
        location_point_counters = {}

        def _location_to_point(location: Point) -> typing.Tuple[int, int]:
            nonlocal location_point_counters
            key = str(location.x) + str(location.y)

            point = self._transform_point(location)
            point = point[0], point[1] + location_point_counters.get(key, 0) * 40

            location_point_counters[key] = location_point_counters.get(key, 0) + 1
            return point

        for event in self.game.events:
            location = event.location
            if isinstance(event, FrontlinePatrolEvent) or isinstance(event, FrontlineAttackEvent):
                location = self._frontline_center(event.from_cp, event.to_cp)

            point = _location_to_point(location)
            rect = pygame.Rect(*point, 30, 30)
            pygame.draw.rect(surface, self.BLACK, rect)

            if rect.collidepoint(*mouse_pos) or self.selected_event_info == (event, point):
                line = self.font.render(str(event), self.ANTIALIASING, self.WHITE, self.BLACK)
                surface.blit(line, rect.center)

            if rect.collidepoint(*mouse_pos):
                if mouse_down[0]:
                    self.selected_event_info = event, point
                    mouse_down[0] = False

        return mouse_down

    def _selected_cp(self, cp):
        if self.selected_event_info:
            event = self.selected_event_info[0]
            event.departure_cp = cp

            self.selected_event_info = None
            self.parent.start_event(event)
        else:
            self.parent.go_cp(cp)

    def _transform_point(self, p: Point, treshold=30) -> (int, int):
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

    def _frontline_vector(self, from_cp: ControlPoint, to_cp: ControlPoint):
        # Cache mechanism to avoid performing frontline vector computation on every frame
        key = str(from_cp.id) + "_" + str(to_cp.id)
        if key in self.frontline_vector_cache:
            return self.frontline_vector_cache[key]
        else:
            frontline = Conflict.frontline_vector(from_cp, to_cp, self.game.theater)
            self.frontline_vector_cache[key] = frontline
            return frontline

    def _frontline_center(self, from_cp: ControlPoint, to_cp: ControlPoint) -> typing.Optional[Point]:
        frontline_vector = self._frontline_vector(from_cp, to_cp)
        if frontline_vector:
            return frontline_vector[0].point_from_heading(frontline_vector[1], frontline_vector[2]/2)
        else:
            return None

    def _player_color(self):
        return self.game.player == "USA" and self.BLUE or self.RED

    def _enemy_color(self):
        return self.game.player == "USA" and self.RED or self.BLUE

    def update(self):
        self.draw()

    def compute_display_rules(self):
        return sum([1 if a.get() else 0 for a in [self.display_forces, self.display_road, self.display_bases, self.display_ground_targets]])

    def display(self, cp: ControlPoint):
        def action(_):
            return self.parent.go_cp(cp)

        return action
