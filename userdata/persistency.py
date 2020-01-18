import logging
import os
import pickle
import shutil
import sys

from dcs import installation

_user_folder = None  # type: str


def setup(user_folder: str):
    global _user_folder
    _user_folder = user_folder


def base_path() -> str:
    global _user_folder
    assert _user_folder

    openbeta_path = os.path.join(_user_folder, "DCS.openbeta")
    if "--force-stable-DCS" not in sys.argv and os.path.exists(openbeta_path):
        return openbeta_path
    else:
        return os.path.join(_user_folder, "DCS")


def _save_file() -> str:
    return os.path.join(base_path(), "liberation_save")


def _temporary_save_file() -> str:
    return os.path.join(base_path(), "liberation_save_tmp")


def _save_file_exists() -> bool:
    return os.path.exists(_save_file())


def mission_path_for(name: str) -> str:
    return os.path.join(base_path(), "Missions", "{}".format(name))


def restore_game():
    if not _save_file_exists():
        return None

    with open(_save_file(), "rb") as f:
        return pickle.load(f)


def save_game(game) -> bool:
    try:
        with open(_temporary_save_file(), "wb") as f:
            pickle.dump(game, f)
        shutil.copy(_temporary_save_file(), _save_file())
        return True
    except Exception as e:
        logging.error(e)
        return False
