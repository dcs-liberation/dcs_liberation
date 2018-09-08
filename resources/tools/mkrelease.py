import os

from zipfile import *


IGNORED_PATHS = [
    "__pycache__",
    ".gitignore",
    ".gitmodules",
    ".git",
    ".idea",
    ".DS_Store",
    "submodules",

    "build",
    "venv",
]

VERSION = input("version str:")


def _zip_dir(archieve, path):
    for path, directories, files in os.walk(path):
        is_ignored = False
        for ignored_path in IGNORED_PATHS:
            if ignored_path in path:
                is_ignored = True
                break

        if is_ignored:
            continue

        for file in files:
            if file in IGNORED_PATHS:
                continue
            archieve.write(os.path.join(path, file))


def _mk_archieve():
    path = os.path.join("build", "dcs_liberation_{}.zip".format(VERSION))
    if os.path.exists(path):
        print("version already exists")
        return

    archieve = ZipFile(path, "w")
    archieve.writestr("start.bat", "py.exe __init__.py \"%UserProfile%\" \"{}\"".format(VERSION))
    _zip_dir(archieve, ".")
    os.chdir("submodules\\dcs")
    _zip_dir(archieve, "dcs")


_mk_archieve()