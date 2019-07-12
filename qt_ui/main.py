import logging
import os
import sys
from time import sleep

import dcs
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QLabel, QSplashScreen

from qt_ui import uiconstants
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.QLiberationWindow import QLiberationWindow
from userdata import persistency, logging as logging_module

if __name__ == "__main__":

    assert len(sys.argv) >= 3, "__init__.py should be started with two mandatory arguments: %UserProfile% location and application version"

    persistency.setup(sys.argv[1])
    dcs.planes.FlyingType.payload_dirs = [
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources\\payloads")]

    VERSION_STRING = sys.argv[2]
    logging_module.setup_version_string(VERSION_STRING)
    logging.info("Using {} as userdata folder".format(persistency.base_path()))

    app = QApplication(sys.argv)
    uiconstants.load_icons()
    uiconstants.load_event_icons()

    # Splash screen setup
    pixmap = QPixmap("./resources/ui/splash_screen.png")
    splash = QSplashScreen(pixmap)
    splash.show()

    # Once splash screen is up : load resources & setup stuff
    persistency.setup(sys.argv[1])

    css = ""
    with open("./resources/stylesheets/style.css") as stylesheet:
        css = stylesheet.read()

    app.processEvents()

    # Uncomment to apply CSS (need works)
    #app.setStyleSheet(css)

    GameUpdateSignal()

    # Start window
    window = QLiberationWindow()
    window.show()

    splash.finish(window)
    sys.exit(app.exec_())

