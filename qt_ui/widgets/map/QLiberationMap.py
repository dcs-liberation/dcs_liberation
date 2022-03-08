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
    QWebEngineSettings,
    QWebEngineView,
)

from game import Game
from game.server.settings import ServerSettings
from qt_ui.models import GameModel
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
    def __init__(self, game_model: GameModel, new_map: bool, dev: bool, parent) -> None:
        super().__init__(parent)
        self.game_model = game_model
        self.setMinimumSize(800, 600)
        self.map_model = MapModel(game_model)

        self.channel = QWebChannel()
        self.channel.registerObject("game", self.map_model)

        self.page = LoggingWebPage(self)
        # Required to allow "cross-origin" access from file:// scoped canvas.html to the
        # localhost HTTP backend.
        self.page.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls, True
        )
        self.page.setWebChannel(self.channel)

        if new_map and dev:
            url = QUrl("http://localhost:3000")
        elif new_map:
            url = QUrl.fromLocalFile(str(Path("client/build/index.html").resolve()))
        else:
            url = QUrl.fromLocalFile(
                str(Path("resources/ui/map/canvas.html").resolve())
            )
        server_settings = ServerSettings.get()
        host = server_settings.server_bind_address
        if host.startswith("::"):
            host = f"[{host}]"
        port = server_settings.server_port
        url.setQuery(f"server={host}:{port}")
        self.page.load(url)
        self.setPage(self.page)

    def set_game(self, game: Optional[Game]) -> None:
        if game is None:
            self.map_model.clear()
        else:
            self.map_model.reset()
