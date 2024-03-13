import os
from pathlib import Path
import shutil

THIS_DIR = Path(__file__).resolve()
SRC_DIR = THIS_DIR.parents[1]


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


def _zip_dir(archive, path):
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
            archive.write(os.path.join(path, file))


def main():
    try:
        shutil.rmtree("./dist")
    except FileNotFoundError:
        pass
    os.system("pyinstaller.exe --clean pyinstaller.spec")


if __name__ == "__main__":
    main()
