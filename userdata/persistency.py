import typing
import pickle
import os
import shutil


def _save_file() -> str:
    return os.path.expanduser("~\Saved Games\DCS\liberation_save")


def _temporary_save_file() -> str:
    return os.path.expanduser("~\Saved Games\DCS\liberation_save_tmp")


def _save_file_exists() -> bool:
    return os.path.exists(_save_file())


def mission_path_for(name: str) -> str:
    return os.path.expanduser("~\Saved Games\DCS\Missions\{}".format(name))


def restore_game():
    if not _save_file_exists():
        return None

    try:
        with open(_save_file(), "rb") as f:
            return pickle.load(f)
    except Exception as e:
        raise e


def save_game(game) -> bool:
    try:
        with open(_temporary_save_file(), "wb") as f:
            pickle.dump(game, f)
        shutil.copy(_temporary_save_file(), _save_file())
        return True
    except Exception as e:
        print(e)
        return False
