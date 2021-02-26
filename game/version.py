from pathlib import Path


def _build_version_string() -> str:
    components = ["2.4.4"]
    build_number_path = Path("resources/buildnumber")
    if build_number_path.exists():
        with build_number_path.open("r") as build_number_file:
            components.append(build_number_file.readline())

    if not Path("resources/final").exists():
        components.append("preview")

    return "-".join(components)


#: Current version of Liberation.
VERSION = _build_version_string()
