from __future__ import annotations

from pathlib import Path

_dcs_saved_game_folder: Path | None = None


def set_dcs_save_game_directory(user_folder: Path) -> None:
    global _dcs_saved_game_folder
    _dcs_saved_game_folder = user_folder
    if not save_dir().exists():
        save_dir().mkdir(parents=True)


def base_path() -> str:
    global _dcs_saved_game_folder
    assert _dcs_saved_game_folder is not None
    return str(_dcs_saved_game_folder)


def save_dir() -> Path:
    return Path(base_path()) / "Liberation" / "Saves"


def mission_path_for(name: str) -> Path:
    return Path(base_path()) / "Missions" / name
