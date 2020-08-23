from PySide2.QtCore import QPoint, QRect, QPointF, Qt
from PySide2.QtGui import QPainter, QBrush
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent

import qt_ui.uiconstants as CONST
from game import db, Game
from game.data.building_data import FORTIFICATION_BUILDINGS
from qt_ui.windows.groundobject.QGroundObjectMenu import QGroundObjectMenu
from theater import TheaterGroundObject, ControlPoint


class QMapGroundObject(QGraphicsRectItem):

    def __init__(self, parent, x: float, y: float, w: float, h: float, cp: ControlPoint, model: TheaterGroundObject, game:Game, buildings=[]):
        super(QMapGroundObject, self).__init__(x, y, w, h)
        self.model = model
        self.cp = cp
        self.parent = parent
        self.game = game
        self.setAcceptHoverEvents(True)
        self.setZValue(2)
        self.buildings = buildings
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations, False)

        if len(self.model.groups) > 0:
            units = {}
            for g in self.model.groups:
                print(g)
                for u in g.units:
                    if u.type in units.keys():
                        units[u.type] = units[u.type]+1
                    else:
                        units[u.type] = 1
            tooltip = "[" + self.model.obj_name + "]" + "\n"
            for unit in units.keys():
                tooltip = tooltip + str(unit) + "x" + str(units[unit]) + "\n"
            self.setToolTip(tooltip[:-1])
        else:
            tooltip = "[" + self.model.obj_name + "]" + "\n"
            for building in buildings:
                if not building.is_dead:
                    tooltip = tooltip + str(building.dcs_identifier) + "\n"
            self.setToolTip(tooltip[:-1])

    def mousePressEvent(self, event:QGraphicsSceneMouseEvent):
        self.openEditionMenu()

    def paint(self, painter, option, widget=None):
        #super(QMapControlPoint, self).paint(painter, option, widget)

        playerIcons = "_blue"
        enemyIcons = ""

        if self.parent.get_display_rule("go"):
            painter.save()

            cat = self.model.category
            if cat == "aa" and self.model.sea_object:
                cat = "ship"

            rect = QRect(option.rect.x()+2,option.rect.y(),option.rect.width()-2,option.rect.height())

            is_dead = self.model.is_dead
            for building in self.buildings:
                if not building.is_dead:
                    is_dead = False
                    break

            if not is_dead and not self.cp.captured:
                painter.drawPixmap(rect, CONST.ICONS[cat + enemyIcons])
            elif not is_dead:
                painter.drawPixmap(rect, CONST.ICONS[cat + playerIcons])
            else:
                painter.drawPixmap(rect, CONST.ICONS["destroyed"])

            self.drawHealthGauge(painter, option)
            painter.restore()

    def drawHealthGauge(self, painter, option):
        units_alive = 0
        units_dead = 0

        if len(self.model.groups) == 0:
            for building in self.buildings:
                if building.dcs_identifier in FORTIFICATION_BUILDINGS:
                    continue
                if building.is_dead:
                    units_dead += 1
                else:
                    units_alive += 1

        for g in self.model.groups:
            units_alive += len(g.units)
            if hasattr(g, "units_losts"):
                units_dead += len(g.units_losts)

        if units_dead + units_alive > 0:
            ratio = float(units_alive)/(float(units_dead) + float(units_alive))
            bar_height = ratio * option.rect.height()
            painter.fillRect(option.rect.x(), option.rect.y(), 2, option.rect.height(), QBrush(CONST.COLORS["dark_red"]))
            painter.fillRect(option.rect.x(), option.rect.y(), 2, bar_height, QBrush(CONST.COLORS["green"]))


    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        self.update()
        self.setCursor(Qt.PointingHandCursor)

    def mouseMoveEvent(self, event:QGraphicsSceneMouseEvent):
        self.update()
        self.setCursor(Qt.PointingHandCursor)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        self.update()

    def openEditionMenu(self):
        self.editionMenu = QGroundObjectMenu(self.window(), self.model, self.buildings, self.cp, self.game)
        self.editionMenu.show()

