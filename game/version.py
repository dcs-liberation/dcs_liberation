from pathlib import Path


def _build_version_string() -> str:
    components = ["2.6"]
    build_number_path = Path("resources/buildnumber")
    if build_number_path.exists():
        with build_number_path.open("r") as build_number_file:
            components.append(build_number_file.readline())

    if not Path("resources/final").exists():
        components.append("preview")

    return "-".join(components)


#: Current version of Liberation.
VERSION = _build_version_string()

#: The latest version of the campaign format. Increment this version whenever all
#: existing campaigns should be flagged as incompatible in the UI. We will still attempt
#: to load old campaigns, but this provides a warning to the user that the campaign may
#: not work correctly.
#:
#: There is no verification that the campaign author updated their campaign correctly
#: this is just a UI hint.
#:
#: Version history:
#:
#: Version 0
#: * Unknown compatibility.
#:
#: Version 1
#: * Compatible with Liberation 2.5.
#:
#: Version 2
#: * Front line endpoints now define convoy origin/destination waypoints. They should be
#:   placed on or near roads.
#: * Factories (Warehouse_A) define factory objectives. Only control points with
#:   factories will be able to recruit ground units, so they should exist in sufficient
#:   number and be protected by IADS.
CAMPAIGN_FORMAT_VERSION = 2
