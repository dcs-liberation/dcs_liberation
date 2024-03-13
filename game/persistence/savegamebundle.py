from __future__ import annotations

import logging
import pickle
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING
from zipfile import ZIP_LZMA, ZipFile

from game.profiling import logged_duration
from game.zipfileext import ZipFileExt

if TYPE_CHECKING:
    from game import Game


class SaveGameBundle:
    """The bundle of saved game assets.

    A save game bundle includes the pickled game object (as well as some backups of
    other game states, like the turn start and previous turn) and the state.json.
    """

    MANUAL_SAVE_NAME = "player.liberation"
    LAST_TURN_SAVE_NAME = "last_turn.liberation"
    START_OF_TURN_SAVE_NAME = "start_of_turn.liberation"
    PRE_SIM_CHECKPOINT_SAVE_NAME = "pre_sim_checkpoint.liberation"

    def __init__(self, bundle_path: Path) -> None:
        self.bundle_path = bundle_path

    def save_player(self, game: Game, copy_from: SaveGameBundle | None) -> None:
        """Writes the save game manually created by the player.

        This save is the one created whenever the player presses save or save-as.
        """
        with logged_duration("Saving game"):
            self._update_bundle_member(game, self.MANUAL_SAVE_NAME, copy_from)

    def save_last_turn(self, game: Game) -> None:
        """Writes the save for the state of the previous turn.

        This save is the state of the game before the state.json changes are applied.
        This is mostly useful as a debugging tool for bugs that occur in the turn
        transition, but can also be used by players to "rewind" to the previous turn.
        """
        with logged_duration("Saving last turn"):
            self._update_bundle_member(game, self.LAST_TURN_SAVE_NAME, copy_from=self)

    def save_start_of_turn(self, game: Game) -> None:
        """Writes the save for the state at the start of the turn.

        This save is the state of the game immediately after the state.json is applied.
        It can be used by players to "rewind" to the start of the turn.
        """
        with logged_duration("Saving start of turn"):
            self._update_bundle_member(
                game, self.START_OF_TURN_SAVE_NAME, copy_from=self
            )

    def save_pre_sim_checkpoint(self, game: Game) -> None:
        """Writes the save file for the state before beginning simulation.

        This save is the state of the game after the player presses "TAKE OFF", but
        before the fast-forward simulation begins. It is not practical to rewind, but
        players commonly will want to cancel and continue planning after pressing that
        button, so we make a checkpoint that we can reload on abort.
        """
        with logged_duration("Saving pre-sim checkpoint"):
            self._update_bundle_member(
                game, self.PRE_SIM_CHECKPOINT_SAVE_NAME, copy_from=self
            )

    def load_player(self) -> Game:
        """Loads the save manually created by the player via save/save-as."""
        return self._load_from(self.MANUAL_SAVE_NAME)

    def load_start_of_turn(self) -> Game:
        """Loads the save automatically created at the start of the turn."""
        return self._load_from(self.START_OF_TURN_SAVE_NAME)

    def load_last_turn(self) -> Game:
        """Loads the save automatically created at the end of the last turn."""
        return self._load_from(self.LAST_TURN_SAVE_NAME)

    def load_pre_sim_checkpoint(self) -> Game:
        """Loads the save automatically created before the simulation began."""
        return self._load_from(self.PRE_SIM_CHECKPOINT_SAVE_NAME)

    def _load_from(self, name: str) -> Game:
        with ZipFile(self.bundle_path) as zip_bundle:
            with zip_bundle.open(name, "r") as save:
                game = pickle.load(save)
                game.save_manager.set_loaded_from(self)
                return game

    def _update_bundle_member(
        self, game: Game, name: str, copy_from: SaveGameBundle | None
    ) -> None:
        # Perform all save work in a copy of the current save to avoid corrupting the
        # save if there's an error while saving.
        with NamedTemporaryFile(
            "wb", suffix=".liberation.zip", delete=False
        ) as temp_save_file:
            temp_file_path = Path(temp_save_file.name)

        # We don't have all the state to create the temporary save from scratch (no last
        # turn, start of turn, etc.), so copy the existing save to create the temp save.
        #
        # Python doesn't actually support overwriting or removing zipfile members, so we
        # have to create a new zipfile and copy over only the files that we won't be
        # writing.
        if copy_from is not None and copy_from.bundle_path.exists():
            shutil.copy(copy_from.bundle_path, temp_file_path)
            ZipFileExt.remove_member(temp_file_path, name, missing_ok=True)

        with ZipFile(temp_file_path, "a", compression=ZIP_LZMA) as zip_bundle:
            with zip_bundle.open(name, "w") as entry:
                pickle.dump(game, entry)

        try:
            temp_file_path.replace(self.bundle_path)
        except OSError:
            # The file might be copyable but not movable if the temp and saved game
            # directories are on different file systems.
            # https://github.com/dcs-liberation/dcs_liberation/issues/2748
            shutil.copy(temp_file_path, self.bundle_path)
            temp_file_path.unlink()
            logging.warning(
                "Save game %s was copyable from temporary location %s but not "
                "moveable. The temp directory and save game directory might be on "
                "different file systems. This makes saving the game slower.",
                self.bundle_path,
                temp_file_path,
            )
