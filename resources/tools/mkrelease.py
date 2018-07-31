import os

from zipfile import *


IGNORED_PATHS = [
    "__pycache__",
    ".gitignore",
    ".gitmodules",
    ".git",
    ".idea",
    ".DS_Store",

    "build",
]

VERSION = "1.3.2"


def _mk_archieve():
    archieve = ZipFile("build/dcs_liberation_{}.zip".format(VERSION), "w")
    archieve.writestr("start.bat", "py.exe __init__.py \"%UserProfile%\" \"{}\"".format(VERSION))

    for path, directories, files in os.walk("."):
        is_ignored = False
        for ignored_path in IGNORED_PATHS:
            if ignored_path in path:
                is_ignored = True
                break

        if is_ignored:
            continue

        for file in files:
            archieve.write(os.path.join(path, file))


_mk_archieve()