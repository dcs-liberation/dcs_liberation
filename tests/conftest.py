from pathlib import Path
from zipfile import ZipFile

import pytest


@pytest.fixture
def tmp_zip(tmp_path: Path) -> Path:
    zip_path = tmp_path / "test.zip"
    with ZipFile(zip_path, "w"):
        pass
    return zip_path
