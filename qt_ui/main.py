import logging
import os
import sys
from shutil import copyfile

import dcs
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QSplashScreen
from dcs import installation

from qt_ui import uiconstants
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.QLiberationWindow import QLiberationWindow
from userdata import persistency, logging as logging_module

if __name__ == "__main__":

    persistency.setup(installation.get_dcs_saved_games_directory())

    custom_payloads = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..\\resources\\customized_payloads")
    if os.path.exists(custom_payloads):
        dcs.planes.FlyingType.payload_dirs.append(custom_payloads)
    else:
        # For release version the path is different.
        custom_payloads = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       "resources\\customized_payloads")
        if os.path.exists(custom_payloads):
            dcs.planes.FlyingType.payload_dirs.append(custom_payloads)

    VERSION_STRING = "2.0RC6"
    logging_module.setup_version_string(VERSION_STRING)
    logging.info("Using {} as userdata folder".format(persistency.base_path()))

    app = QApplication(sys.argv)

    # Splash screen setup
    pixmap = QPixmap("./resources/ui/splash_screen.png")
    splash = QSplashScreen(pixmap)
    splash.show()

    # Once splash screen is up : load resources & setup stuff
    uiconstants.load_icons()
    uiconstants.load_event_icons()
    uiconstants.load_aircraft_icons()
    uiconstants.load_vehicle_icons()


    css = ""
    with open("./resources/stylesheets/style.css") as stylesheet:
        css = stylesheet.read()

    # Replace DCS Mission scripting file to allow DCS Liberation to work
    print("Replace : " + installation.get_dcs_install_directory() + os.path.sep + "Scripts/MissionScripting.lua")
    copyfile("./resources/scripts/MissionScripting.lua", installation.get_dcs_install_directory() + os.path.sep + "Scripts/MissionScripting.lua")
    app.processEvents()

    # Apply CSS (need works)
    app.setStyleSheet(css)
    GameUpdateSignal()

    # Start window
    window = QLiberationWindow()
    window.showMaximized()

    splash.finish(window)
    sys.exit(app.exec_())

