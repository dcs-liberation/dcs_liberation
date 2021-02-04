from typing import List, Optional

from PySide2.QtCore import QRect
from PySide2.QtGui import QBrush
from PySide2.QtWidgets import QGraphicsItem

import qt_ui.uiconstants as const
from game import Game
from game.data.building_data import FORTIFICATION_BUILDINGS
from game.db import REWARDS
from game.theater import ControlPoint, TheaterGroundObject
from game.theater.theatergroundobject import MissileSiteGroundObject, CoastalSiteGroundObject
from qt_ui.windows.groundobject.QGroundObjectMenu import QGroundObjectMenu
from .QMapObject import QMapObject
from ...displayoptions import DisplayOptions


class QMapGroundObject(QMapObject):
    def __init__(self, parent, x: float, y: float, w: float, h: float,
                 control_point: ControlPoint,
                 ground_object: TheaterGroundObject, game: Game,
                 buildings: Optional[List[TheaterGroundObject]] = None) -> None:
        super().__init__(x, y, w, h, mission_target=ground_object)
        self.ground_object = ground_object
        self.control_point = control_point
        self.parent = parent
        self.game = game
        self.setZValue(2)
        self.buildings = buildings if buildings is not None else []
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations, False)
        self.ground_object_dialog: Optional[QGroundObjectMenu] = None
        self.setToolTip(self.tooltip)

    @property
    def tooltip(self) -> str:
        lines = [
            f"[{self.ground_object.obj_name}]",
            f"${self.production_per_turn} per turn",
        ]
        if self.ground_object.groups:
            units = {}
            for g in self.ground_object.groups:
                for u in g.units:
                    if u.type in units:
                        units[u.type] = units[u.type]+1
                    else:
                        units[u.type] = 1

            for unit in units.keys():
                lines.append(f"{unit} x {units[unit]}")
        else:
            for building in self.buildings:
                if not building.is_dead:
                    lines.append(f"{building.dcs_identifier}")

        return "\n".join(lines)

    @property
    def production_per_turn(self) -> int:
        production = 0
        for building in self.buildings:
            if building.is_dead:
                continue
            if building.category in REWARDS.keys():
                production += REWARDS[building.category]
        return production

    def paint(self, painter, option, widget=None) -> None:
        player_icons = "_blue"
        enemy_icons = ""

        if DisplayOptions.ground_objects:
            painter.save()

            cat = self.ground_object.category
            if cat == "aa" and self.ground_object.sea_object:
                cat = "ship"
            if isinstance(self.ground_object, MissileSiteGroundObject):
                cat = "missile"
            if isinstance(self.ground_object, CoastalSiteGroundObject):
                cat = "coastal"

            rect = QRect(option.rect.x() + 2, option.rect.y(),
                         option.rect.width() - 2, option.rect.height())

            is_dead = self.ground_object.is_dead
            for building in self.buildings:
                if not building.is_dead:
                    is_dead = False
                    break

            if cat == "aa":
                has_threat = False
                for group in self.ground_object.groups:
                    if self.ground_object.threat_range(group).distance_in_meters > 0:
                        has_threat = True

            if not is_dead and not self.control_point.captured:
                if cat == "aa" and not has_threat:
                    painter.drawPixmap(rect, const.ICONS["nothreat" + enemy_icons])
                else:    
                    painter.drawPixmap(rect, const.ICONS[cat + enemy_icons])
            elif not is_dead:
                if cat == "aa" and not has_threat:
                    painter.drawPixmap(rect, const.ICONS["nothreat" + player_icons])
                else:
                    painter.drawPixmap(rect, const.ICONS[cat + player_icons])
            else:
                painter.drawPixmap(rect, const.ICONS["destroyed"])

            self.draw_health_gauge(painter, option)
            painter.restore()

    def draw_health_gauge(self, painter, option) -> None:
        units_alive = 0
        units_dead = 0

        if len(self.ground_object.groups) == 0:
            for building in self.buildings:
                if building.dcs_identifier in FORTIFICATION_BUILDINGS:
                    continue
                if building.is_dead:
                    units_dead += 1
                else:
                    units_alive += 1

        for g in self.ground_object.groups:
            units_alive += len(g.units)
            if hasattr(g, "units_losts"):
                units_dead += len(g.units_losts)

        if units_dead + units_alive > 0:
            ratio = float(units_alive)/(float(units_dead) + float(units_alive))
            bar_height = ratio * option.rect.height()
            painter.fillRect(option.rect.x(), option.rect.y(), 2,
                             option.rect.height(),
                             QBrush(const.COLORS["dark_red"]))
            painter.fillRect(option.rect.x(), option.rect.y(), 2, bar_height,
                             QBrush(const.COLORS["green"]))

    def on_click(self) -> None:
        self.ground_object_dialog = QGroundObjectMenu(
            self.window(),
            self.ground_object,
            self.buildings,
            self.control_point,
            self.game
        )
        self.ground_object_dialog.show()
