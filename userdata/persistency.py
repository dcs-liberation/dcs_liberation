import pickle
import os
import shutil

from game.game import Game


def _save_file() -> str:
    return "build/save"


def _temporary_save_file() -> str:
    return "build/save_tmp"


def _save_file_exists() -> bool:
    return os.path.exists(_save_file())


def restore_game() -> Game:
    if not _save_file_exists():
        return None

    try:
        with open(_save_file(), "rb") as f:
            return pickle.load(f)
    except:
        return None


def save_game(game: Game) -> bool:
    try:
        with open(_temporary_save_file(), "wb") as f:
            pickle.dump(game, f)
            shutil.copy(_temporary_save_file(), _save_file())
            return True
    except:
        return False
