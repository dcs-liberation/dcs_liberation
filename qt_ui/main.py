from __future__ import annotations

import argparse
import logging
import ntpath
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import yaml
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QCheckBox, QSplashScreen, QDialog
from dcs.payloads import PayloadDirectories

from game import Game, VERSION, logging_config, persistence
from game.ato import FlightType
from game.campaignloader.campaign import Campaign, DEFAULT_BUDGET
from game.data.weapons import Pylon, Weapon, WeaponGroup
from game.dcs.aircrafttype import AircraftType
from game.factions.factions import Factions
from game.persistence.paths import liberation_user_dir
from game.plugins import LuaPluginManager
from game.profiling import logged_duration
from game.server import EventStream, Server
from game.settings import Settings
from game.sim import GameUpdateEvents
from game.theater.start_generator import GameGenerator, GeneratorSettings, ModSettings
from pydcs_extensions import load_mods
from qt_ui import (
    liberation_install,
    liberation_theme,
    uiconstants,
)
from qt_ui.uiflags import UiFlags
from qt_ui.windows.AirWingConfigurationDialog import AirWingConfigurationDialog
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.QLiberationWindow import QLiberationWindow
from qt_ui.windows.preferences.QLiberationFirstStartWindow import (
    QLiberationFirstStartWindow,
)

THIS_DIR = Path(__file__).parent


def inject_custom_payloads(user_path: Path) -> None:
    dev_payloads = THIS_DIR.parent / "resources/customized_payloads"
    # The packaged release rearranges the file locations, so the release has the
    # customized payloads in a different location.
    release_payloads = THIS_DIR / "resources/customized_payloads"
    if dev_payloads.exists():
        payloads = dev_payloads
    elif release_payloads.exists():
        payloads = release_payloads
    else:
        raise RuntimeError(
            f"Could not find customized payloads at {release_payloads} or "
            f"{dev_payloads}. Aircraft will have no payloads."
        )
    # We configure these as fallbacks so that the user's payloads override ours.
    PayloadDirectories.set_fallback(payloads)
    PayloadDirectories.set_preferred(user_path / "MissionEditor" / "UnitPayloads")


def on_game_load(game: Game | None) -> None:
    EventStream.drain()
    EventStream.put_nowait(GameUpdateEvents().game_loaded(game))


def run_ui(create_game_params: CreateGameParams | None, ui_flags: UiFlags) -> None:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"  # Potential fix for 4K screens
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)

    # init the theme and load the stylesheet based on the theme index
    liberation_theme.init()
    with open(
        "./resources/stylesheets/" + liberation_theme.get_theme_css_file(),
        encoding="utf-8",
    ) as stylesheet:
        logging.info("Loading stylesheet: %s", liberation_theme.get_theme_css_file())
        app.setStyleSheet(stylesheet.read())

    first_start = liberation_install.init()
    if first_start:
        window = QLiberationFirstStartWindow()
        window.exec_()

    logging.info("Using {} as 'Saved Game Folder'".format(persistence.base_path()))
    logging.info(
        "Using {} as 'DCS installation folder'".format(
            liberation_install.get_dcs_install_directory()
        )
    )

    inject_custom_payloads(Path(persistence.base_path()))

    # Splash screen setup
    pixmap = QPixmap("./resources/ui/splash_screen.png")
    splash = QSplashScreen(pixmap)
    splash.show()

    # Once splash screen is up : load resources & setup stuff
    uiconstants.load_icons()
    uiconstants.load_event_icons()
    uiconstants.load_aircraft_icons()
    uiconstants.load_vehicle_icons()

    # Show warning if no DCS Installation directory was set
    if liberation_install.get_dcs_install_directory() == "":
        logging.warning(
            "DCS Installation directory is empty. MissionScripting file will not be replaced!"
        )
        if not liberation_install.ignore_empty_install_directory():
            ignore_checkbox = QCheckBox("Do not show again")
            ignore_checkbox.stateChanged.connect(set_ignore_empty_install_directory)
            message_box = QtWidgets.QMessageBox(parent=splash)
            message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            message_box.setWindowTitle("No DCS installation directory.")
            message_box.setText(
                "The DCS Installation directory is not set correctly. "
                "This will prevent DCS Liberation from working properly, as the MissionScripting "
                "file will not be modified."
                "<br/><br/>To solve this problem, you can set the Installation directory "
                "within the preferences menu. You can also manually edit or replace the "
                "following file:"
                "<br/><br/><strong>&lt;dcs_installation_directory&gt;/Scripts/MissionScripting.lua</strong>"
                "<br/><br/>The easiest way to do it is to replace the original file with the file in dcs-liberation distribution (&lt;dcs_liberation_installation&gt;/resources/scripts/MissionScripting.lua)."
                "<br/><br/>You can find more information on how to manually change this file in the Liberation Wiki (Page: Dedicated Server Guide) on GitHub.</p>"
            )
            message_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            message_box.setCheckBox(ignore_checkbox)
            message_box.exec_()
    # Replace DCS Mission scripting file to allow DCS Liberation to work
    try:
        liberation_install.replace_mission_scripting_file()
    except:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.setWindowTitle("Wrong DCS installation directory.")
        error_dialog.showMessage(
            "Unable to modify Mission Scripting file. Possible issues with rights. Try running as admin, or please perform the modification of the MissionScripting file manually."
        )
        error_dialog.exec_()

    # Apply CSS (need works)
    GameUpdateSignal()
    GameUpdateSignal.get_instance().game_loaded.connect(on_game_load)

    game: Game | None = None
    if create_game_params is not None:
        with logged_duration("New game creation"):
            game = create_game(create_game_params)

    # Start window
    window = QLiberationWindow(game, ui_flags)
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

    parser.add_argument(
        "--warn-missing-weapon-data",
        action="store_true",
        help="Emits a warning for weapons without date or fallback information.",
    )

    parser.add_argument("--dev", action="store_true", help="Enable development mode.")

    speed_controls_group = parser.add_argument_group()
    speed_controls_group.add_argument(
        "--show-sim-speed-controls",
        action="store_true",
        default=False,
        help="Shows the sim speed controls in the top panel.",
    )
    speed_controls_group.add_argument(
        "--no-show-sim-speed-controls",
        dest="show_sim_speed_controls",
        action="store_false",
        help="Hides the sim speed controls in the top panel (default).",
    )

    parser.add_argument("--new-map", help="Deprecated. Does nothing.")
    parser.add_argument("--old-map", help="Deprecated. Does nothing.")

    new_game = subparsers.add_parser("new-game")

    new_game.add_argument(
        "campaign", type=path_arg, help="Path to the campaign to start."
    )

    new_game.add_argument(
        "--blue", default="USA 2005", help="Name of the blue faction."
    )

    new_game.add_argument(
        "--red", default="Russia 1990", help="Name of the red faction."
    )

    new_game.add_argument(
        "--supercarrier", action="store_true", help="Use the supercarrier module."
    )

    new_game.add_argument(
        "--auto-procurement", action="store_true", help="Automate bluefor procurement."
    )

    new_game.add_argument(
        "--use-new-squadron-rules",
        action="store_true",
        help=(
            "Limit the number of aircraft per squadron and begin the campaign with "
            "them at full strength."
        ),
    )

    new_game.add_argument(
        "--inverted", action="store_true", help="Invert the campaign."
    )

    new_game.add_argument(
        "--date",
        type=datetime.fromisoformat,
        default=datetime.today(),
        help="Start date of the campaign.",
    )

    new_game.add_argument(
        "--restrict-weapons-by-date",
        action="store_true",
        help="Enable campaign date restricted weapons.",
    )

    new_game.add_argument("--cheats", action="store_true", help="Enable cheats.")

    new_game.add_argument(
        "--advanced-iads", action="store_true", help="Enable advanced IADS."
    )

    new_game.add_argument(
        "--show-air-wing-config",
        action="store_true",
        help="Show the air wing configuration dialog after generating the game.",
    )

    lint_weapons = subparsers.add_parser("lint-weapons")
    lint_weapons.add_argument("aircraft", help="Name of the aircraft variant to lint.")

    subparsers.add_parser("dump-task-priorities")

    return parser.parse_args()


@dataclass(frozen=True)
class CreateGameParams:
    campaign_path: Path
    blue: str
    red: str
    supercarrier: bool
    auto_procurement: bool
    inverted: bool
    cheats: bool
    start_date: datetime
    restrict_weapons_by_date: bool
    advanced_iads: bool
    use_new_squadron_rules: bool
    show_air_wing_config: bool

    @staticmethod
    def from_args(args: argparse.Namespace) -> CreateGameParams | None:
        if args.subcommand != "new-game":
            return None
        return CreateGameParams(
            args.campaign,
            args.blue,
            args.red,
            args.supercarrier,
            args.auto_procurement,
            args.inverted,
            args.cheats,
            args.date,
            args.restrict_weapons_by_date,
            args.advanced_iads,
            args.use_new_squadron_rules,
            args.show_air_wing_config,
        )


def create_game(params: CreateGameParams) -> Game:
    campaign = Campaign.from_file(params.campaign_path)
    theater = campaign.load_theater(params.advanced_iads)
    faction_loader = Factions.load()
    lua_plugin_manager = LuaPluginManager.load()
    lua_plugin_manager.merge_player_settings()
    generator = GameGenerator(
        faction_loader.get_by_name(params.blue),
        faction_loader.get_by_name(params.red),
        theater,
        campaign.load_air_wing_config(theater),
        Settings(
            supercarrier=params.supercarrier,
            automate_runway_repair=params.auto_procurement,
            automate_front_line_reinforcements=params.auto_procurement,
            automate_aircraft_reinforcements=params.auto_procurement,
            enable_frontline_cheats=params.cheats,
            enable_base_capture_cheat=params.cheats,
            restrict_weapons_by_date=params.restrict_weapons_by_date,
            enable_squadron_aircraft_limits=params.use_new_squadron_rules,
        ),
        GeneratorSettings(
            start_date=params.start_date,
            start_time=campaign.recommended_start_time,
            player_budget=DEFAULT_BUDGET,
            enemy_budget=DEFAULT_BUDGET,
            inverted=params.inverted,
            advanced_iads=theater.iads_network.advanced_iads,
            no_carrier=False,
            no_lha=False,
            no_player_navy=False,
            no_enemy_navy=False,
        ),
        ModSettings(
            a4_skyhawk=False,
            f22_raptor=False,
            f104_starfighter=False,
            hercules=False,
            jas39_gripen=False,
            su57_felon=False,
            frenchpack=False,
            high_digit_sams=False,
        ),
        lua_plugin_manager,
    )
    game = generator.generate()
    if params.show_air_wing_config:
        if AirWingConfigurationDialog(game, None).exec() == QDialog.DialogCode.Rejected:
            sys.exit("Aborted air wing configuration")
    game.begin_turn_0(squadrons_start_full=params.use_new_squadron_rules)
    return game


def set_ignore_empty_install_directory(value: bool) -> None:
    liberation_install.set_ignore_empty_install_directory(value)
    liberation_install.save_config()


def lint_all_weapon_data() -> None:
    for weapon in WeaponGroup.named("Unknown").weapons:
        logging.warning(f"No weapon data for {weapon}: {weapon.clsid}")


def lint_weapon_data_for_aircraft(aircraft: AircraftType) -> None:
    all_weapons: set[Weapon] = set()
    for pylon in Pylon.iter_pylons(aircraft):
        all_weapons |= pylon.allowed

    for weapon in all_weapons:
        if weapon.weapon_group.name == "Unknown":
            logging.warning(f'{weapon.clsid} "{weapon.name}" has no weapon data')


def fix_pycharm_debugger_if_needed() -> None:
    """Applies workaround for a pycharm debugger bug.

    https://youtrack.jetbrains.com/issue/PY-53232/Debugger-doesnt-work-when-pyproj-is-imported
    """
    # sys.gettrace() will return something whenever *some* debugger is being used. The
    # pdb module will be loaded if that debugger is the built-in python debugger.
    if sys.gettrace() is not None and "pdb" not in sys.modules:
        logging.debug(
            "Applying workaround for https://youtrack.jetbrains.com/issue/PY-53232/Debugger-doesnt-work-when-pyproj-is-imported"
        )
        ntpath.sep = "\\"


def dump_task_priorities() -> None:
    first_start = liberation_install.init()
    if first_start:
        sys.exit(
            "Cannot dump task priorities without configuring DCS Liberation. Start the"
            "UI for the first run configuration."
        )

    data: dict[str, dict[str, int]] = {}
    for task in FlightType:
        data[task.value] = {
            a.name: a.task_priority(task)
            for a in AircraftType.priority_list_for_task(task)
        }

    debug_path = liberation_user_dir() / "Debug" / "priorities.yaml"
    debug_path.parent.mkdir(parents=True, exist_ok=True)
    with debug_path.open("w", encoding="utf-8") as output:
        yaml.dump(data, output, sort_keys=False, allow_unicode=True)


def main():
    logging_config.init_logging(VERSION)

    logging.debug("Python version %s", sys.version)

    fix_pycharm_debugger_if_needed()

    if not str(Path(__file__)).isascii():
        logging.warning(
            "Installation path contains non-ASCII characters. This is known to cause problems."
        )

    args = parse_args()

    # TODO: Flesh out data and then make unconditional.
    if args.warn_missing_weapon_data:
        lint_all_weapon_data()

    load_mods()

    if args.subcommand == "lint-weapons":
        lint_weapon_data_for_aircraft(AircraftType.named(args.aircraft))
        return
    if args.subcommand == "dump-task-priorities":
        dump_task_priorities()
        return

    with Server().run_in_thread():
        run_ui(
            CreateGameParams.from_args(args),
            UiFlags(args.dev, args.show_sim_speed_controls),
        )


if __name__ == "__main__":
    main()
