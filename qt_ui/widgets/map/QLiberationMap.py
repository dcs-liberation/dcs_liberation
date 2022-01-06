from __future__ import annotations

import logging
from pathlib import Path
from typing import (
    Optional,
)

from PySide2.QtCore import QUrl
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtWebEngineWidgets import (
    QWebEnginePage,
    QWebEngineView,
)

from game import Game
from qt_ui.models import GameModel
from qt_ui.simcontroller import SimController
from .model import MapModel


class LoggingWebPage(QWebEnginePage):
    def javaScriptConsoleMessage(
        self,
        level: QWebEnginePage.JavaScriptConsoleMessageLevel,
        message: str,
        line_number: int,
        source: str,
    ) -> None:
        if level == QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel:
            logging.error(message)
        elif level == QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel:
            logging.warning(message)
        else:
            logging.info(message)


class QLiberationMap(QWebEngineView):
    def __init__(
        self, game_model: GameModel, sim_controller: SimController, parent
    ) -> None:
        super().__init__(parent)
        self.game_model = game_model
        self.setMinimumSize(800, 600)
        self.map_model = MapModel(game_model, sim_controller)

        self.channel = QWebChannel()
        self.channel.registerObject("game", self.map_model)

        self.page = LoggingWebPage(self)
        self.page.setWebChannel(self.channel)
        self.page.load(
            QUrl.fromLocalFile(str(Path("resources/ui/map/canvas.html").resolve()))
        )
        self.setPage(self.page)

    def set_game(self, game: Optional[Game]) -> None:
        if game is None:
            self.map_model.clear()
        else:
            self.map_model.reset()
