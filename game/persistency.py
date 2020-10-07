import logging
import os
import pickle
import shutil
from typing import Optional

_dcs_saved_game_folder: Optional[str] = None
_file_abs_path = None

def setup(user_folder: str):
    global _dcs_saved_game_folder
    _dcs_saved_game_folder = user_folder
    _file_abs_path = os.path.join(base_path(), "default.liberation")

def base_path() -> str:
    global _dcs_saved_game_folder
    assert _dcs_saved_game_folder
    return _dcs_saved_game_folder

def _save_file() -> str:
    return os.path.join(base_path(), "default.liberation")

def _temporary_save_file() -> str:
    return os.path.join(base_path(), "tmpsave.liberation")

def _autosave_path() -> str:
    return os.path.join(base_path(), "autosave.liberation")

def _save_file_exists() -> bool:
    return os.path.exists(_save_file())

def mission_path_for(name: str) -> str:
    return os.path.join(base_path(), "Missions", "{}".format(name))


def restore_game():
    if not _save_file_exists():
        return None

    with open(_save_file(), "rb") as f:
        try:
            save = pickle.load(f)
            return save
        except Exception:
            logging.exception("Invalid Save game")
            return None


def load_game(path):
    with open(path, "rb") as f:
        try:
            save = pickle.load(f)
            save.savepath = path
            return save
        except Exception:
            logging.exception("Invalid Save game")
            return None


def save_game(game) -> bool:
    try:
        with open(_temporary_save_file(), "wb") as f:
            pickle.dump(game, f)
        shutil.copy(_temporary_save_file(), game.savepath)
        return True
    except Exception:
        logging.exception("Could not save game")
        return False


def autosave(game) -> bool:
    """
    Autosave to the autosave location
    :param game: Game to save
    :return: True if saved succesfully
    """
    try:
        with open(_autosave_path(), "wb") as f:
            pickle.dump(game, f)
        return True
    except Exception:
        logging.exception("Could not save game")
        return False

