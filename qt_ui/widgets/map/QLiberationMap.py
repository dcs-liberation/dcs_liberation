from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

from game.server.settings import ServerSettings
from qt_ui.models import GameModel


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
    def __init__(self, game_model: GameModel, dev: bool, parent) -> None:
        super().__init__(parent)
        self.game_model = game_model
        self.setMinimumSize(800, 600)

        self.page = LoggingWebPage(self)
        # Required to allow "cross-origin" access from file:// scoped canvas.html to the
        # localhost HTTP backend.
        self.page.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True
        )

        if dev:
            url = QUrl("http://localhost:3000")
        else:
            url = QUrl.fromLocalFile(str(Path("client/build/index.html").resolve()))
        server_settings = ServerSettings.get()
        host = server_settings.server_bind_address
        if host.startswith("::"):
            host = f"[{host}]"
        port = server_settings.server_port
        url.setQuery(f"server={host}:{port}")
        self.page.load(url)
        self.setPage(self.page)
