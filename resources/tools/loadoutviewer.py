"""Command-line utility for displaying human readable loadout configurations."""
import argparse
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Type

from dcs.helicopters import helicopter_map
from dcs.planes import plane_map
from dcs.unittype import FlyingType

from game import persistency
from game.ato import FlightType
from game.ato.loadouts import Loadout
from game.dcs.aircrafttype import AircraftType

# TODO: Move this logic out of the UI.
from qt_ui import liberation_install
from qt_ui.main import inject_custom_payloads


def non_empty_loadouts_for(
    aircraft: Type[FlyingType],
) -> Iterator[tuple[FlightType, Loadout]]:
    for task in FlightType:
        try:
            loadout = Loadout.default_for_task_and_aircraft(task, aircraft)
        except KeyError:
            # Not all aircraft have a unitPayloads field. This should maybe be handled
            # in pydcs, but I'm not sure about the cause. For now, just ignore the field
            # since we can be less robust in optional tooling.
            continue

        if loadout.name != "Empty":
            yield task, loadout


def print_pylons(loadout: Loadout, prefix: str = "\t") -> None:
    pylons = dict(sorted(loadout.pylons.items()))
    for pylon_id, weapon in pylons.items():
        if weapon is not None:
            print(f"{prefix}{pylon_id}: {weapon.name}")


def show_all_loadouts(aircraft: Type[FlyingType]) -> None:
    loadouts = list(non_empty_loadouts_for(aircraft))
    if not loadouts:
        return

    print(f"Loadouts for {aircraft.id}:")
    for task, loadout in loadouts:
        print(f"\t{task.value}: {loadout.name}")
        print_pylons(loadout, prefix="\t\t")


def task_by_name(name: str) -> FlightType:
    for task in FlightType:
        if task.value == name:
            return task
    raise KeyError(f"No FlightType named {name}")


def show_single_loadout(aircraft: Type[FlyingType], task_name: str) -> None:
    task = task_by_name(task_name)
    try:
        loadout = Loadout.default_for_task_and_aircraft(task, aircraft)
    except KeyError:
        # Not all aircraft have a unitPayloads field. This should maybe be handled
        # in pydcs, but I'm not sure about the cause. For now, just ignore the field
        # since we can be less robust in optional tooling.
        return
    if loadout.pylons:
        print(f"{aircraft.id} {loadout.name}:")
        print_pylons(loadout)


def show_loadouts_for(aircraft: Type[FlyingType], task_name: str | None) -> None:
    if task_name is None:
        show_all_loadouts(aircraft)
    else:
        show_single_loadout(aircraft, task_name)


def show_all_aircraft(task_name: str | None) -> None:
    for aircraft in AircraftType.each_dcs_type():
        show_loadouts_for(aircraft, task_name)


def show_single_aircraft(aircraft_id: str, task_name: str | None) -> None:
    try:
        aircraft: Type[FlyingType] = plane_map[aircraft_id]
    except KeyError:
        aircraft = helicopter_map[aircraft_id]
    show_loadouts_for(aircraft, task_name)


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--aircraft-id",
        help=(
            "ID of the aircraft to display loadouts for. By default all aircraft will "
            + "be displayed."
        ),
    )

    parser.add_argument(
        "--task",
        help=(
            "Name of the mission type to display. By default loadouts for all mission "
            + "types will be displayed."
        ),
    )

    args = parser.parse_args()

    first_start = liberation_install.init()
    if first_start:
        sys.exit(
            "Cannot view payloads without configuring DCS Liberation. Start the UI for "
            "the first run configuration."
        )

    inject_custom_payloads(Path(persistency.base_path()))

    if args.aircraft_id is None:
        show_all_aircraft(args.task)
    else:
        show_single_aircraft(args.aircraft_id, args.task)


if __name__ == "__main__":
    main()
