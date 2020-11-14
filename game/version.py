from pathlib import Path


def _build_version_string() -> str:
    components = ["2.2.0"]
    if Path("buildnumber").exists():
        with open("buildnumber", "r") as file:
            components.append(file.readline())

    if not Path("final").exists():
        components.append("preview")

    return "-".join(components)


#: Current version of Liberation.
VERSION = _build_version_string()
