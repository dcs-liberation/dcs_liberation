import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import dcs
from PySide2 import QtWidgets
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QSplashScreen

from game import Game, db, persistency, VERSION
from game.settings import Settings
from game.theater.start_generator import GameGenerator, GeneratorSettings
from qt_ui import (
    liberation_install,
    liberation_theme,
    logging_config,
    uiconstants,
)
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.QLiberationWindow import QLiberationWindow
from qt_ui.windows.newgame.QCampaignList import Campaign
from qt_ui.windows.newgame.QNewGameWizard import DEFAULT_BUDGET
from qt_ui.windows.preferences.QLiberationFirstStartWindow import \
    QLiberationFirstStartWindow


def run_ui(game: Optional[Game] = None) -> None:
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1" # Potential fix for 4K screens
    app = QApplication(sys.argv)

    # init the theme and load the stylesheet based on the theme index
    liberation_theme.init()
    with open("./resources/stylesheets/"+liberation_theme.get_theme_css_file()) as stylesheet:
        logging.info('Loading stylesheet: %s', liberation_theme.get_theme_css_file())
        app.setStyleSheet(stylesheet.read())

    # Inject custom payload in pydcs framework
    custom_payloads = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..\\resources\\customized_payloads")
    if os.path.exists(custom_payloads):
        dcs.unittype.FlyingType.payload_dirs.append(custom_payloads)
    else:
        # For release version the path is different.
        custom_payloads = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                       "resources\\customized_payloads")
        if os.path.exists(custom_payloads):
            dcs.unittype.FlyingType.payload_dirs.append(custom_payloads)

    first_start = liberation_install.init()
    if first_start:
        window = QLiberationFirstStartWindow()
        window.exec_()

    logging.info("Using {} as 'Saved Game Folder'".format(persistency.base_path()))
    logging.info("Using {} as 'DCS installation folder'".format(liberation_install.get_dcs_install_directory()))

    # Splash screen setup
    pixmap = QPixmap("./resources/ui/splash_screen.png")
    splash = QSplashScreen(pixmap)
    splash.show()

    # Once splash screen is up : load resources & setup stuff
    uiconstants.load_icons()
    uiconstants.load_event_icons()
    uiconstants.load_aircraft_icons()
    uiconstants.load_vehicle_icons()

    # Replace DCS Mission scripting file to allow DCS Liberation to work
    try:
        liberation_install.replace_mission_scripting_file()
    except:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.setWindowTitle("Wrong DCS installation directory.")
        error_dialog.showMessage("Unable to modify Mission Scripting file. Possible issues with rights. Try running as admin, or please perform the modification of the MissionScripting file manually.")
        error_dialog.exec_()

    # Apply CSS (need works)
    GameUpdateSignal()

    # Start window
    window = QLiberationWindow(game)
    window.showMaximized()
    splash.finish(window)
    qt_execution_code = app.exec_()

    # Restore Mission Scripting file
    logging.info("QT App terminated with status code : " + str(qt_execution_code))
    logging.info("Attempt to restore original mission scripting file")
    liberation_install.restore_original_mission_scripting()
    logging.info("QT process exited with code : " + str(qt_execution_code))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")

    def path_arg(arg: str) -> Path:
        path = Path(arg)
        if not path.exists():
            raise argparse.ArgumentTypeError("path does not exist")
        return path

    new_game = subparsers.add_parser("new-game")

    new_game.add_argument(
        "campaign", type=path_arg,
        help="Path to the campaign to start."
    )

    new_game.add_argument(
        "--blue", default="USA 2005", help="Name of the blue faction."
    )

    new_game.add_argument(
        "--red", default="Russia 1990", help="Name of the red faction."
    )

    new_game.add_argument(
        "--supercarrier", action="store_true",
        help="Use the supercarrier module."
    )

    new_game.add_argument(
        "--auto-procurement", action="store_true",
        help="Automate bluefor procurement."
    )

    new_game.add_argument(
        "--inverted", action="store_true",
        help="Invert the campaign."
    )

    return parser.parse_args()


def create_game(campaign_path: Path, blue: str, red: str,
                supercarrier: bool, auto_procurement: bool,
                inverted: bool) -> Game:
    campaign = Campaign.from_json(campaign_path)
    generator = GameGenerator(
        blue, red, campaign.load_theater(),
        Settings(
            supercarrier=supercarrier,
            automate_runway_repair=auto_procurement,
            automate_front_line_reinforcements=auto_procurement,
            automate_aircraft_reinforcements=auto_procurement
        ),
        GeneratorSettings(
            start_date=datetime.today(),
            player_budget=DEFAULT_BUDGET,
            enemy_budget=DEFAULT_BUDGET,
            midgame=False,
            inverted=inverted,
            no_carrier=False,
            no_lha=False,
            no_player_navy=False,
            no_enemy_navy=False
        )
    )
    return generator.generate()


def main():
    logging_config.init_logging(VERSION)

    # Load eagerly to catch errors early.
    db.FACTIONS.initialize()

    game: Optional[Game] = None

    args = parse_args()
    if args.subcommand == "new-game":
        game = create_game(args.campaign, args.blue, args.red,
                           args.supercarrier, args.auto_procurement,
                           args.inverted)

    run_ui(game)


if __name__ == "__main__":
    main()
