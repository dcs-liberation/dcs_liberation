import os
import shutil

from zipfile import *


IGNORED_PATHS = [
    "__pycache__",
    ".gitignore",
    ".git",
    ".idea",
    ".DS_Store",
    "requirements.txt",
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
    path = os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
        "build",
        "dcs_liberation_{}.zip".format(VERSION),
    )
    if os.path.exists(path):
        print("version already exists")
        return

    try:
        shutil.rmtree("./dist")
    except FileNotFoundError:
        pass
    os.system("pyinstaller.exe --clean pyinstaller.spec")
    # archieve = ZipFile(path, "w")
    # archieve.writestr("dcs_liberation.bat", "cd dist\\dcs_liberation\r\nliberation_main \"%UserProfile%\\Saved Games\" \"{}\"".format(VERSION))
    # _zip_dir(archieve, "./dist/dcs_liberation")


_mk_archieve()
