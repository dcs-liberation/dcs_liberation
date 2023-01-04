import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile


class ZipFileExt:
    @staticmethod
    def remove_member(path: Path, name: str, missing_ok: bool = False) -> None:
        """Replaces the archive with a copy that excludes one member.

        This is needed to workaround Python's lack of a ZipFile.remove() or a way to
        overwrite existing members. Attempting to update a member in a zipfile will
        write a duplicate entry: https://github.com/python/cpython/issues/51067.
        """
        with ZipFile(path, "r") as zip_file:
            if name not in zip_file.namelist():
                if missing_ok:
                    return
                raise ValueError(f"Cannot override {name} as it does not exist")

        # Doing this by extracting all the files to a temporary directory is faster than
        # reading and writing a file at a time (1-5 seconds vs 0.5 seconds for a save
        # bundle).
        with TemporaryDirectory() as temp_dir_str:
            temp_dir = Path(temp_dir_str)
            shutil.unpack_archive(path, temp_dir)
            (temp_dir / name).unlink()
            shutil.make_archive(
                # shutil.make_archive automatically adds the extension
                str(path.with_suffix("")),
                "zip",
                root_dir=temp_dir_str,
            )
