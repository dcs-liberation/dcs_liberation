from __future__ import annotations

import datetime
from typing import Optional, List, Iterator, Type, TYPE_CHECKING, Mapping

from dcs.unittype import FlyingType

from game.data.weapons import Weapon, Pylon

if TYPE_CHECKING:
    from gen.flights.flight import Flight


class Loadout:
    def __init__(
        self,
        name: str,
        pylons: Mapping[int, Optional[Weapon]],
        date: Optional[datetime.date],
        is_custom: bool = False,
    ) -> None:
        self.name = name
        self.pylons = {k: v for k, v in pylons.items() if v is not None}
        self.date = date
        self.is_custom = is_custom

    def derive_custom(self, name: str) -> Loadout:
        return Loadout(name, self.pylons, self.date, is_custom=True)

    def degrade_for_date(
        self, unit_type: Type[FlyingType], date: datetime.date
    ) -> Loadout:
        if self.date is not None and self.date <= date:
            return Loadout(self.name, self.pylons, self.date)

        new_pylons = dict(self.pylons)
        for pylon_number, weapon in self.pylons.items():
            if weapon is None:
                del new_pylons[pylon_number]
                continue
            if not weapon.available_on(date):
                pylon = Pylon.for_aircraft(unit_type, pylon_number)
                for fallback in weapon.fallbacks:
                    if not pylon.can_equip(fallback):
                        continue
                    if not fallback.available_on(date):
                        continue
                    new_pylons[pylon_number] = fallback
                    break
                else:
                    del new_pylons[pylon_number]
        return Loadout(f"{self.name} ({date.year})", new_pylons, date)

    @classmethod
    def iter_for(cls, flight: Flight) -> Iterator[Loadout]:
        # Dict of payload ID (numeric) to:
        #
        # {
        #   "name": The name the user set in the ME
        #   "pylons": List (as a dict) of dicts of:
        #       {"CLSID": class ID, "num": pylon number}
        #   "tasks": List (as a dict) of task IDs the payload is used by.
        # }
        payloads = flight.unit_type.load_payloads()
        for payload in payloads["payloads"].values():
            name = payload["name"]
            pylons = payload["pylons"]
            yield Loadout(
                name,
                {p["num"]: Weapon.from_clsid(p["CLSID"]) for p in pylons.values()},
                date=None,
            )

    @classmethod
    def all_for(cls, flight: Flight) -> List[Loadout]:
        return list(cls.iter_for(flight))

    @classmethod
    def default_loadout_names_for(cls, flight: Flight) -> Iterator[str]:
        from gen.flights.flight import FlightType

        # This is a list of mappings from the FlightType of a Flight to the type of
        # payload defined in the resources/payloads/UNIT_TYPE.lua file. A Flight has no
        # concept of a PyDCS task, so COMMON_OVERRIDE cannot be used here. This is used
        # in the payload editor, for setting the default loadout of an object. The left
        # element is the FlightType name, and the right element is a tuple containing
        # what is used in the lua file. Some aircraft differ from the standard loadout
        # names, so those have been included here too. The priority goes from first to
        # last - the first element in the tuple will be tried first, then the second,
        # etc.
        loadout_names = {t: [f"Liberation {t.value}"] for t in FlightType}
        legacy_names = {
            FlightType.TARCAP: ("CAP HEAVY", "CAP"),
            FlightType.BARCAP: ("CAP HEAVY", "CAP"),
            FlightType.CAS: ("CAS MAVERICK F", "CAS"),
            FlightType.INTERCEPTION: ("CAP HEAVY", "CAP"),
            FlightType.STRIKE: ("STRIKE",),
            FlightType.ANTISHIP: ("ANTISHIP",),
            FlightType.SEAD: ("SEAD",),
            FlightType.DEAD: ("SEAD",),
            FlightType.ESCORT: ("CAP HEAVY", "CAP"),
            FlightType.BAI: ("BAI", "CAS MAVERICK F", "CAS"),
            FlightType.SWEEP: ("CAP HEAVY", "CAP"),
            FlightType.OCA_RUNWAY: ("RUNWAY_ATTACK", "RUNWAY_STRIKE", "STRIKE"),
            FlightType.OCA_AIRCRAFT: ("OCA", "CAS MAVERICK F", "CAS"),
        }
        for flight_type, names in legacy_names.items():
            loadout_names[flight_type].extend(names)
        # A SEAD escort typically does not need a different loadout than a regular
        # SEAD flight, so fall back to SEAD if needed.
        loadout_names[FlightType.SEAD_ESCORT].extend(loadout_names[FlightType.SEAD])
        yield from loadout_names[flight.flight_type]

    @classmethod
    def default_for(cls, flight: Flight) -> Loadout:
        # Iterate through each possible payload type for a given aircraft.
        # Some aircraft have custom loadouts that in aren't the standard set.
        for name in cls.default_loadout_names_for(flight):
            # This operation is cached, but must be called before load_by_name will
            # work.
            flight.unit_type.load_payloads()
            payload = flight.unit_type.loadout_by_name(name)
            if payload is not None:
                return Loadout(
                    name,
                    {i: Weapon.from_clsid(d["clsid"]) for i, d in payload},
                    date=None,
                )

        # TODO: Try group.load_task_default_loadout(loadout_for_task)
        return Loadout("Empty", {}, date=None)
