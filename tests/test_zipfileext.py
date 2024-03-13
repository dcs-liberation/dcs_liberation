from pathlib import Path
from zipfile import ZipFile

import pytest

from game.zipfileext import ZipFileExt


def test_remove_member_does_nothing_if_member_is_not_present(tmp_zip: Path) -> None:
    expect_mtime = tmp_zip.stat().st_mtime
    ZipFileExt.remove_member(tmp_zip, "c", missing_ok=True)
    assert tmp_zip.stat().st_mtime == expect_mtime


def test_remove_member_raises_if_missing_not_ok(tmp_zip: Path) -> None:
    with pytest.raises(ValueError):
        ZipFileExt.remove_member(tmp_zip, "c")


def test_remove_member(tmp_zip: Path) -> None:
    with ZipFile(tmp_zip, "w") as zip_file:
        zip_file.writestr("a", "foo")
        zip_file.writestr("b", "bar")

    ZipFileExt.remove_member(tmp_zip, "a")

    with ZipFile(tmp_zip, "r") as zip_file:
        with pytest.raises(KeyError):
            zip_file.read("a")
        # Yes, we wrote a str, but ZipFile.read always returns bytes, and ZipFile.write
        # requires an intermediate file. It's hard to write bytes, and hard to read str.
        # This is all the single-byte range of UTF-8 anyway, so it doesn't matter.
        assert zip_file.read("b") == b"bar"
