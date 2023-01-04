import datetime
from pathlib import Path
from zipfile import ZipFile

import pytest

from game import Game
from game.persistence.savegamebundle import SaveGameBundle


@pytest.fixture
def tmp_bundle(tmp_zip: Path) -> SaveGameBundle:
    return SaveGameBundle(tmp_zip)


def test_save_player_new_save(game: Game, tmp_bundle: SaveGameBundle) -> None:
    with ZipFile(tmp_bundle.bundle_path, "r") as zip_file:
        with pytest.raises(KeyError):
            zip_file.read(SaveGameBundle.MANUAL_SAVE_NAME)
    tmp_bundle.save_player(game, copy_from=None)

    with ZipFile(tmp_bundle.bundle_path, "r") as zip_file:
        assert zip_file.namelist() == [SaveGameBundle.MANUAL_SAVE_NAME]


def test_save_player_existing_save(game: Game, tmp_bundle: SaveGameBundle) -> None:
    game.date = datetime.date.min
    tmp_bundle.save_start_of_turn(game)
    tmp_bundle.save_player(game, copy_from=tmp_bundle)

    test_date = datetime.date.today()
    game.date = test_date
    tmp_bundle.save_player(game, copy_from=tmp_bundle)

    assert tmp_bundle.load_start_of_turn().date == datetime.date.min
    assert tmp_bundle.load_player().date == test_date


def test_save_last_turn(game: Game, tmp_bundle: SaveGameBundle) -> None:
    with ZipFile(tmp_bundle.bundle_path, "r") as zip_file:
        with pytest.raises(KeyError):
            zip_file.read(SaveGameBundle.LAST_TURN_SAVE_NAME)
    tmp_bundle.save_last_turn(game)

    with ZipFile(tmp_bundle.bundle_path, "r") as zip_file:
        assert zip_file.namelist() == [SaveGameBundle.LAST_TURN_SAVE_NAME]


def test_save_start_of_turn(game: Game, tmp_bundle: SaveGameBundle) -> None:
    with ZipFile(tmp_bundle.bundle_path, "r") as zip_file:
        with pytest.raises(KeyError):
            zip_file.read(SaveGameBundle.START_OF_TURN_SAVE_NAME)
    tmp_bundle.save_start_of_turn(game)

    with ZipFile(tmp_bundle.bundle_path, "r") as zip_file:
        assert zip_file.namelist() == [SaveGameBundle.START_OF_TURN_SAVE_NAME]


def test_failed_save_leaves_original_intact(
    game: Game, tmp_bundle: SaveGameBundle
) -> None:
    expect_date = datetime.date.today()
    game.date = expect_date
    tmp_bundle.save_player(game, copy_from=None)

    # Add some non-pickleable member to the game to cause an error on save.
    def local_f() -> None:
        pass

    game.garbage = local_f  # type: ignore
    with pytest.raises(AttributeError):
        tmp_bundle.save_player(game, copy_from=tmp_bundle)

    assert tmp_bundle.load_player().date == expect_date


def test_load_reads_correct_data(game: Game, tmp_bundle: SaveGameBundle) -> None:
    last_turn_date = datetime.date.today() - datetime.timedelta(days=2)
    game.date = last_turn_date
    tmp_bundle.save_last_turn(game)

    start_of_turn_date = datetime.date.today() - datetime.timedelta(days=1)
    game.date = start_of_turn_date
    tmp_bundle.save_start_of_turn(game)

    player_date = datetime.date.today()
    game.date = player_date
    tmp_bundle.save_player(game, copy_from=tmp_bundle)

    assert tmp_bundle.load_last_turn().date == last_turn_date
    assert tmp_bundle.load_start_of_turn().date == start_of_turn_date
    assert tmp_bundle.load_player().date == player_date


def test_load_from_absent_file_raises(tmp_bundle: SaveGameBundle) -> None:
    tmp_bundle.bundle_path.unlink(missing_ok=True)
    with pytest.raises(FileNotFoundError):
        tmp_bundle.load_last_turn()


def test_load_from_absent_member_raises(game: Game, tmp_bundle: SaveGameBundle) -> None:
    tmp_bundle.save_start_of_turn(game)
    with pytest.raises(KeyError):
        tmp_bundle.load_last_turn()
