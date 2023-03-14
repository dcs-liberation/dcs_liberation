from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

from qt_ui import liberation_install
from .paths import save_dir
from .savegamebundle import SaveGameBundle

if TYPE_CHECKING:
    from game.game import Game


class SaveManager:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.player_save_location: Path | None = None
        self.last_saved_bundle: SaveGameBundle | None = None

    @property
    def autosave_path(self) -> Path:
        # This is a property rather than a member because it's one less thing we need to
        # update when loading a save that may have been copied from another machine.
        return self.default_save_directory() / "autosave.liberation.zip"

    @property
    def default_save_location(self) -> Path:
        if self.player_save_location is not None:
            return self.player_save_location
        return self.autosave_path

    @property
    def default_save_bundle(self) -> SaveGameBundle:
        return SaveGameBundle(self.default_save_location)

    def save_player(self, override_destination: Path | None = None) -> None:
        copy_from = self.last_saved_bundle
        with self._save_bundle_context(override_destination) as bundle:
            self.player_save_location = bundle.bundle_path
            bundle.save_player(self.game, copy_from)
            liberation_install.setup_last_save_file(str(bundle.bundle_path))
            liberation_install.save_config()

    def save_last_turn(self) -> None:
        with self._save_bundle_context() as bundle:
            bundle.save_last_turn(self.game)

    def save_start_of_turn(self) -> None:
        with self._save_bundle_context() as bundle:
            bundle.save_start_of_turn(self.game)

    def set_loaded_from(self, bundle: SaveGameBundle) -> None:
        """Reconfigures this save manager based on the loaded game.

        The SaveManager is persisted to Game, including details like the last saved path
        and bundle details. This data is no longer valid if the save was moved manually
        (such as from one machine to another), so it needs to be replaced with the load
        location.

        This should only be called by SaveGameBundle after a game load.
        """
        self.player_save_location = bundle.bundle_path
        self.last_saved_bundle = bundle

    @contextmanager
    def _save_bundle_context(
        self, override_destination: Path | None = None
    ) -> Iterator[SaveGameBundle]:
        if override_destination is not None:
            bundle = SaveGameBundle(override_destination)
        else:
            bundle = self.default_save_bundle

        previous_saved_bundle = self.last_saved_bundle
        try:
            self.last_saved_bundle = bundle
            yield bundle
        except Exception:
            self.last_saved_bundle = previous_saved_bundle
            raise

    @staticmethod
    def load_last_turn(bundle_path: Path) -> Game:
        return SaveGameBundle(bundle_path).load_last_turn()

    @staticmethod
    def load_start_of_turn(bundle_path: Path) -> Game:
        return SaveGameBundle(bundle_path).load_start_of_turn()

    @staticmethod
    def load_player_save(bundle_path: Path) -> Game:
        return SaveGameBundle(bundle_path).load_player()

    @staticmethod
    def default_save_directory() -> Path:
        return save_dir()
