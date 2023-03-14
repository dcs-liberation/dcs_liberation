import datetime
from pathlib import Path
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from game import Game
from game.persistence import SaveManager, set_dcs_save_game_directory


@pytest.fixture(autouse=True)
def mock_setup_last_save_file(mocker: MockerFixture) -> Mock:
    return mocker.patch("qt_ui.liberation_install.setup_last_save_file")


@pytest.fixture(autouse=True)
def mock_save_config(mocker: MockerFixture) -> Mock:
    return mocker.patch("qt_ui.liberation_install.save_config")


@pytest.fixture(autouse=True)
def setup_persistence_paths(tmp_path: Path) -> None:
    set_dcs_save_game_directory(tmp_path)


@pytest.fixture
def save_manager(game: Game) -> SaveManager:
    return game.save_manager


def test_new_savemanager_saves_to_autosave(save_manager: SaveManager) -> None:
    assert save_manager.default_save_location == save_manager.autosave_path


def test_savemanager_saves_to_last_save_location(save_manager: SaveManager) -> None:
    save_manager.player_save_location = Path("Saves/foo.liberation.zip")
    assert save_manager.default_save_location == save_manager.player_save_location


def test_saving_without_name_saves_to_autosave_path(save_manager: SaveManager) -> None:
    assert not save_manager.autosave_path.exists()
    save_manager.save_player()
    assert save_manager.autosave_path.exists()


def test_saving_with_name_updates_last_save_location(
    save_manager: SaveManager, tmp_path: Path
) -> None:
    save_path = tmp_path / "foo.liberation.zip"
    assert not save_path.exists()
    save_manager.save_player(override_destination=save_path)
    assert save_path.exists()
    assert save_manager.last_saved_bundle is not None
    assert save_manager.last_saved_bundle.bundle_path == save_path


def test_player_save_location(save_manager: SaveManager, tmp_path: Path) -> None:
    assert save_manager.player_save_location is None
    save_manager.save_last_turn()
    assert save_manager.player_save_location is None
    save_manager.save_start_of_turn()
    assert save_manager.player_save_location is None
    expect_location = tmp_path / "player.liberation.zip"
    save_manager.save_player(override_destination=expect_location)
    assert save_manager.player_save_location == expect_location


def test_saving_updates_preferences_with_save_location(
    save_manager: SaveManager, mock_setup_last_save_file: Mock, mock_save_config: Mock
) -> None:
    save_manager.save_player()
    mock_setup_last_save_file.assert_called_once_with(
        str(save_manager.default_save_location)
    )
    mock_save_config.assert_called_once()


def test_non_player_saves_do_not_update_preferences(
    save_manager: SaveManager, mock_setup_last_save_file: Mock
) -> None:
    save_manager.save_last_turn()
    mock_setup_last_save_file.assert_not_called()
    save_manager.save_start_of_turn()
    mock_setup_last_save_file.assert_not_called()


def test_load_game_loads_correct_data(save_manager: SaveManager) -> None:
    test_date = datetime.date.today()
    assert save_manager.game.date != test_date
    save_manager.game.date = test_date
    save_manager.save_player()
    game = SaveManager.load_player_save(save_manager.default_save_location)
    assert game.date == test_date


def test_loading_missing_save_raises() -> None:
    with pytest.raises(FileNotFoundError):
        SaveManager.load_player_save(Path("does not exist"))


def test_saving_after_autosave_copies_autosave_members(
    save_manager: SaveManager, tmp_path: Path
) -> None:
    save_manager.save_start_of_turn()

    save_path = tmp_path / "foo.liberation.zip"
    save_manager.save_player(override_destination=save_path)

    SaveManager.load_start_of_turn(save_path)


def test_failed_save_does_not_update_last_saved_path(
    save_manager: SaveManager, tmp_path: Path
) -> None:
    expect_date = datetime.date.today()
    save_manager.game.date = expect_date
    save_manager.save_player()
    assert save_manager.last_saved_bundle is not None
    expect_path = save_manager.last_saved_bundle.bundle_path

    # Add some non-pickleable member to the game to cause an error on save.
    def local_f() -> None:
        pass

    save_manager.game.garbage = local_f  # type: ignore
    with pytest.raises(AttributeError):
        save_manager.save_player(
            override_destination=tmp_path / "badsave.liberation.zip"
        )

    assert save_manager.last_saved_bundle.bundle_path == expect_path


def test_load_reads_correct_data(save_manager: SaveManager) -> None:
    last_turn_date = datetime.date.today() - datetime.timedelta(days=2)
    save_manager.game.date = last_turn_date
    save_manager.save_last_turn()

    start_of_turn_date = datetime.date.today() - datetime.timedelta(days=1)
    save_manager.game.date = start_of_turn_date
    save_manager.save_start_of_turn()

    player_date = datetime.date.today()
    save_manager.game.date = player_date
    save_manager.save_player()

    assert save_manager.last_saved_bundle is not None
    bundle_path = save_manager.last_saved_bundle.bundle_path
    assert SaveManager.load_last_turn(bundle_path).date == last_turn_date
    assert SaveManager.load_start_of_turn(bundle_path).date == start_of_turn_date
    assert SaveManager.load_player_save(bundle_path).date == player_date


def test_save_after_loading_foreign_save(
    save_manager: SaveManager, tmp_path: Path
) -> None:
    """Tests that we can save games that were copied from another machine.

    Regression test for https://github.com/dcs-liberation/dcs_liberation/issues/2756.
    """
    # To simulate the situation from the bug, we save a game to a directory, move it out
    # of that directory, delete the directory, then attempt to load and save the game.
    # It should save to the new location. If it tries to save to the old location, it
    # will fail because the directory does not exist.

    # Create the save on "the other machine"...
    bad_directory = tmp_path / "other-machine"
    bad_directory.mkdir()
    bad_save_path = bad_directory / "foo.liberation.zip"
    save_manager.save_player(override_destination=bad_save_path)

    good_save_path = tmp_path / "foo.liberation.zip"
    bad_save_path.rename(good_save_path)
    bad_directory.rmdir()

    game = SaveManager.load_player_save(good_save_path)
    assert game.save_manager.player_save_location == good_save_path
    game.save_manager.save_player()
