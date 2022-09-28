from __future__ import annotations

import datetime
import logging
from collections.abc import Iterable
from typing import Iterator, Mapping, Optional, TYPE_CHECKING, Type

from dcs.unittype import FlyingType

from game.data.weapons import Pylon, Weapon, WeaponType
from game.dcs.aircrafttype import AircraftType
from .flighttype import FlightType

if TYPE_CHECKING:
    from .flight import Flight


class Loadout:
    def __init__(
        self,
        name: str,
        pylons: Mapping[int, Optional[Weapon]],
        date: Optional[datetime.date],
        is_custom: bool = False,
    ) -> None:
        self.name = name
        # We clear unused pylon entries on initialization, but UI actions can still
        # cause a pylon to be emptied, so make the optional type explicit.
        self.pylons: Mapping[int, Optional[Weapon]] = {
            k: v for k, v in pylons.items() if v is not None
        }
        self.date = date
        self.is_custom = is_custom

    def derive_custom(self, name: str) -> Loadout:
        return Loadout(name, self.pylons, self.date, is_custom=True)

    def has_weapon_of_type(self, weapon_type: WeaponType) -> bool:
        for weapon in self.pylons.values():
            if weapon is not None and weapon.weapon_group.type is weapon_type:
                return True
        return False

    @staticmethod
    def _fallback_for(
        weapon: Weapon,
        pylon: Pylon,
        date: datetime.date,
        skip_types: Optional[Iterable[WeaponType]] = None,
    ) -> Optional[Weapon]:
        if skip_types is None:
            skip_types = set()
        for fallback in weapon.fallbacks:
            if not pylon.can_equip(fallback):
                continue
            if not fallback.available_on(date):
                continue
            if fallback.weapon_group.type in skip_types:
                continue
            return fallback
        return None

    def degrade_for_date(self, unit_type: AircraftType, date: datetime.date) -> Loadout:
        if self.date is not None and self.date <= date:
            return Loadout(self.name, self.pylons, self.date, self.is_custom)

        new_pylons = dict(self.pylons)
        for pylon_number, weapon in self.pylons.items():
            if weapon is None:
                del new_pylons[pylon_number]
                continue
            if not weapon.available_on(date):
                pylon = Pylon.for_aircraft(unit_type, pylon_number)
                fallback = self._fallback_for(weapon, pylon, date)
                if fallback is None:
                    del new_pylons[pylon_number]
                else:
                    new_pylons[pylon_number] = fallback
        loadout = Loadout(self.name, new_pylons, date, self.is_custom)
        # If this is not a custom loadout, we should replace any LGBs with iron bombs if
        # the loadout lost its TGP.
        #
        # If the loadout was chosen explicitly by the user, assume they know what
        # they're doing. They may be coordinating buddy-lase.
        if not loadout.is_custom:
            loadout.replace_lgbs_if_no_tgp(unit_type, date)
        return loadout

    def replace_lgbs_if_no_tgp(
        self, unit_type: AircraftType, date: datetime.date
    ) -> None:
        if self.has_weapon_of_type(WeaponType.TGP):
            return

        new_pylons = dict(self.pylons)
        for pylon_number, weapon in self.pylons.items():
            if weapon is not None and weapon.weapon_group.type is WeaponType.LGB:
                pylon = Pylon.for_aircraft(unit_type, pylon_number)
                fallback = self._fallback_for(
                    weapon, pylon, date, skip_types={WeaponType.LGB}
                )
                if fallback is None:
                    del new_pylons[pylon_number]
                else:
                    new_pylons[pylon_number] = fallback
        self.pylons = new_pylons

    @classmethod
    def iter_for(cls, flight: Flight) -> Iterator[Loadout]:
        return cls.iter_for_aircraft(flight.unit_type)

    @classmethod
    def iter_for_aircraft(cls, aircraft: AircraftType) -> Iterator[Loadout]:
        # Dict of payload ID (numeric) to:
        #
        # {
        #   "name": The name the user set in the ME
        #   "pylons": List (as a dict) of dicts of:
        #       {"CLSID": class ID, "num": pylon number}
        #   "tasks": List (as a dict) of task IDs the payload is used by.
        # }
        payloads = aircraft.dcs_unit_type.load_payloads()
        for payload in payloads.values():
            name = payload["name"]
            pylons = payload["pylons"]
            try:
                pylon_assignments = {
                    p["num"]: Weapon.with_clsid(p["CLSID"]) for p in pylons.values()
                }
            except KeyError:
                logging.exception(
                    "Ignoring %s loadout with invalid weapons: %s", aircraft.name, name
                )
                continue

            yield Loadout(
                name,
                pylon_assignments,
                date=None,
            )

    @classmethod
    def default_loadout_names_for(cls, task: FlightType) -> Iterator[str]:
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
            FlightType.TARCAP: ("CAP HEAVY", "CAP", "Liberation BARCAP"),
            FlightType.BARCAP: ("CAP HEAVY", "CAP", "Liberation TARCAP"),
            FlightType.CAS: ("CAS MAVERICK F", "CAS"),
            FlightType.STRIKE: ("STRIKE",),
            FlightType.ANTISHIP: ("ANTISHIP",),
            FlightType.DEAD: ("DEAD",),
            FlightType.SEAD: ("SEAD",),
            FlightType.BAI: ("BAI",),
            FlightType.OCA_RUNWAY: ("RUNWAY_ATTACK", "RUNWAY_STRIKE"),
            FlightType.OCA_AIRCRAFT: ("OCA",),
        }
        for flight_type, names in legacy_names.items():
            loadout_names[flight_type].extend(names)
        # A SEAD escort typically does not need a different loadout than a regular
        # SEAD flight, so fall back to SEAD if needed.
        loadout_names[FlightType.SEAD_ESCORT].extend(loadout_names[FlightType.SEAD])
        # Sweep and escort can fall back to TARCAP.
        loadout_names[FlightType.ESCORT].extend(loadout_names[FlightType.TARCAP])
        loadout_names[FlightType.SWEEP].extend(loadout_names[FlightType.TARCAP])
        # Intercept can fall back to BARCAP.
        loadout_names[FlightType.INTERCEPTION].extend(loadout_names[FlightType.BARCAP])
        # OCA/Aircraft falls back to BAI, which falls back to CAS.
        loadout_names[FlightType.BAI].extend(loadout_names[FlightType.CAS])
        loadout_names[FlightType.OCA_AIRCRAFT].extend(loadout_names[FlightType.BAI])
        # DEAD also falls back to BAI.
        loadout_names[FlightType.DEAD].extend(loadout_names[FlightType.BAI])
        # OCA/Runway falls back to Strike
        loadout_names[FlightType.OCA_RUNWAY].extend(loadout_names[FlightType.STRIKE])
        yield from loadout_names[task]

    @classmethod
    def default_for(cls, flight: Flight) -> Loadout:
        return cls.default_for_task_and_aircraft(
            flight.flight_type, flight.unit_type.dcs_unit_type
        )

    @classmethod
    def default_for_task_and_aircraft(
        cls, task: FlightType, dcs_unit_type: Type[FlyingType]
    ) -> Loadout:
        # Iterate through each possible payload type for a given aircraft.
        # Some aircraft have custom loadouts that in aren't the standard set.
        for name in cls.default_loadout_names_for(task):
            # This operation is cached, but must be called before load_by_name will
            # work.
            dcs_unit_type.load_payloads()
            payload = dcs_unit_type.loadout_by_name(name)
            if payload is not None:
                try:
                    pylons = {i: Weapon.with_clsid(d["clsid"]) for i, d in payload}
                except KeyError:
                    logging.exception(
                        "Ignoring %s loadout with invalid weapons: %s",
                        dcs_unit_type.id,
                        name,
                    )
                    continue
                return Loadout(name, pylons, date=None)

        # TODO: Try group.load_task_default_loadout(loadout_for_task)
        return cls.empty_loadout()

    @classmethod
    def empty_loadout(cls) -> Loadout:
        return Loadout("Empty", {}, date=None)
