"""Application-wide dialog management."""
from typing import Optional

from game.ato.flight import Flight
from game.theater.missiontarget import MissionTarget
from .models import GameModel, PackageModel
from .windows.mission.QEditFlightDialog import QEditFlightDialog
from .windows.mission.QPackageDialog import (
    QEditPackageDialog,
    QNewPackageDialog,
)


class Dialog:
    """Dialog management singleton.

    Opens dialogs and keeps references to dialog windows so that their creators
    do not need to worry about the lifetime of the dialog object, and can open
    dialogs without needing to have their own reference to common data like the
    game model.
    """

    #: The game model. Is only None before initialization, as the game model
    #: itself is responsible for handling the case where no game is loaded.
    game_model: Optional[GameModel] = None

    new_package_dialog: Optional[QNewPackageDialog] = None
    edit_package_dialog: Optional[QEditPackageDialog] = None
    edit_flight_dialog: Optional[QEditFlightDialog] = None

    @classmethod
    def set_game(cls, game_model: GameModel) -> None:
        """Sets the game model."""
        cls.game_model = game_model

    @classmethod
    def open_new_package_dialog(cls, mission_target: MissionTarget, parent=None):
        """Opens the dialog to create a new package with the given target."""
        cls.new_package_dialog = QNewPackageDialog(
            cls.game_model, cls.game_model.ato_model, mission_target, parent=parent
        )
        cls.new_package_dialog.show()

    @classmethod
    def open_edit_package_dialog(cls, package_model: PackageModel):
        """Opens the dialog to edit the given package."""
        cls.edit_package_dialog = QEditPackageDialog(
            cls.game_model, cls.game_model.ato_model, package_model
        )
        cls.edit_package_dialog.show()

    @classmethod
    def open_edit_flight_dialog(
        cls, package_model: PackageModel, flight: Flight, parent=None
    ) -> None:
        """Opens the dialog to edit the given flight."""
        cls.edit_flight_dialog = QEditFlightDialog(
            cls.game_model, package_model, flight, parent=parent
        )
        cls.edit_flight_dialog.show()
