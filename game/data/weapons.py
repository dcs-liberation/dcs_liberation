from __future__ import annotations

import datetime
import inspect
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterator, Optional, Set, Tuple, Type, Union, cast

from dcs.unitgroup import FlyingGroup
from dcs.unittype import FlyingType
from dcs.weapons_data import Weapons, weapon_ids


PydcsWeapon = Dict[str, Union[int, str]]
PydcsWeaponAssignment = Tuple[int, PydcsWeapon]


@dataclass(frozen=True)
class Weapon:
    """Wraps a pydcs weapon dict in a hashable type."""

    cls_id: str
    name: str
    weight: int

    def available_on(self, date: datetime.date) -> bool:
        introduction_year = WEAPON_INTRODUCTION_YEARS.get(self)
        if introduction_year is None:
            logging.warning(
                f"No introduction year for {self}, assuming always available")
            return True
        return date >= datetime.date(introduction_year, 1, 1)

    @property
    def as_pydcs(self) -> PydcsWeapon:
        return {
            "clsid": self.cls_id,
            "name": self.name,
            "weight": self.weight,
        }

    @property
    def fallbacks(self) -> Iterator[Weapon]:
        yield self
        fallback = WEAPON_FALLBACK_MAP[self]
        if fallback is not None:
            yield from fallback.fallbacks

    @classmethod
    def from_pydcs(cls, weapon_data: PydcsWeapon) -> Weapon:
        return cls(
            cast(str, weapon_data["clsid"]),
            cast(str, weapon_data["name"]),
            cast(int, weapon_data["weight"])
        )

    @classmethod
    def from_clsid(cls, clsid: str) -> Optional[Weapon]:
        data = weapon_ids.get(clsid)
        if data is None:
            return None
        return cls.from_pydcs(data)


@dataclass(frozen=True)
class Pylon:
    number: int
    allowed: Set[Weapon]

    def can_equip(self, weapon: Weapon) -> bool:
        return weapon in self.allowed

    def equip(self, group: FlyingGroup, weapon: Weapon) -> None:
        if not self.can_equip(weapon):
            raise ValueError(f"Pylon {self.number} cannot equip {weapon.name}")
        group.load_pylon(self.make_pydcs_assignment(weapon), self.number)

    def make_pydcs_assignment(self, weapon: Weapon) -> PydcsWeaponAssignment:
        return self.number, weapon.as_pydcs

    def available_on(self, date: datetime.date) -> Iterator[Weapon]:
        for weapon in self.allowed:
            if weapon.available_on(date):
                yield weapon

    @classmethod
    def for_aircraft(cls, aircraft: Type[FlyingType], number: int) -> Pylon:
        # In pydcs these are all arbitrary inner classes of the aircraft type.
        # The only way to identify them is by their name.
        pylons = [v for v in aircraft.__dict__.values() if
                  inspect.isclass(v) and v.__name__.startswith("Pylon")]

        # And that Pylon class has members with irrelevant names that have
        # values of (pylon number, allowed weapon).
        allowed = set()
        for pylon in pylons:
            for key, value in pylon.__dict__.items():
                if key.startswith("__"):
                    continue
                pylon_number, weapon = value
                if pylon_number != number:
                    continue
                allowed.add(Weapon.from_pydcs(weapon))

        return cls(number, allowed)

    @classmethod
    def iter_pylons(cls, aircraft: Type[FlyingType]) -> Iterator[Pylon]:
        for pylon in sorted(list(aircraft.pylons)):
            yield cls.for_aircraft(aircraft, pylon)


_WEAPON_FALLBACKS = [
    # AIM-120C
    (Weapons.AIM_120C, Weapons.AIM_120B),
    (Weapons.LAU_115___AIM_120C, Weapons.LAU_115___AIM_120B),
    (Weapons.LAU_115_2_LAU_127_AIM_120C, Weapons.LAU_115_2_LAU_127_AIM_120B),

    # AIM-120B
    (Weapons.AIM_120B, Weapons.AIM_7MH),
    (Weapons.LAU_115___AIM_120B, Weapons.LAU_115C_AIM_7MH),
    (Weapons.LAU_115_2_LAU_127_AIM_120B, Weapons.LAU_115C_AIM_7MH),

    # AIM-7MH
    (Weapons.AIM_7MH, Weapons.AIM_7M),
    (Weapons.LAU_115C_AIM_7MH, Weapons.LAU_115___AIM_7M),

    # AIM-7M
    (Weapons.AIM_7M, Weapons.AIM_7F),
    (Weapons.LAU_115___AIM_7M, Weapons.LAU_115C_AIM_7F),

    # AIM-7F
    (Weapons.AIM_7F, Weapons.AIM_7E),
    (Weapons.LAU_115C_AIM_7F, Weapons.LAU_115C_AIM_7E),

    # AIM-7E
    (Weapons.AIM_7E, Weapons.AIM_9X_Sidewinder_IR_AAM),
    (Weapons.LAU_115C_AIM_7E, Weapons.LAU_115_LAU_127_AIM_9X),

    # AIM-9X
    (Weapons.AIM_9X_Sidewinder_IR_AAM, Weapons.AIM_9P5_Sidewinder_IR_AAM),
    (Weapons.LAU_7_AIM_9X_Sidewinder_IR_AAM, Weapons.LAU_7_AIM_9P5_Sidewinder_IR_AAM),
    (Weapons.LAU_115_LAU_127_AIM_9X, Weapons.LAU_115_LAU_127_AIM_9M),
    (Weapons.LAU_115_2_LAU_127_AIM_9X, Weapons.LAU_115_2_LAU_127_AIM_9M),
    (Weapons.LAU_127_AIM_9X, Weapons.LAU_127_AIM_9M),

    # AIM-9P5
    (Weapons.AIM_9P5_Sidewinder_IR_AAM, Weapons.AIM_9P_Sidewinder_IR_AAM),
    (Weapons.LAU_7_AIM_9P5_Sidewinder_IR_AAM, Weapons.LAU_7_AIM_9P_Sidewinder_IR_AAM),

    # AIM-9P
    (Weapons.AIM_9P_Sidewinder_IR_AAM, Weapons.AIM_9M_Sidewinder_IR_AAM),
    (Weapons.LAU_7_AIM_9P_Sidewinder_IR_AAM, Weapons.LAU_7_AIM_9M_Sidewinder_IR_AAM),

    # AIM-9M
    (Weapons.AIM_9M_Sidewinder_IR_AAM, Weapons.AIM_9L_Sidewinder_IR_AAM),
    (Weapons.LAU_7_AIM_9M_Sidewinder_IR_AAM, Weapons.LAU_7_AIM_9L),

    # AIM-9L
    (Weapons.AIM_9L_Sidewinder_IR_AAM, None),
    (Weapons.LAU_7_AIM_9L, None),

    # R-27 (AA-10 Alamo)
    (Weapons.R_27ER, Weapons.R_27R),
    (Weapons.R_27ET, Weapons.R_27T),

    # R-77 (AA-12)
    (Weapons.R_77, Weapons.R_27ER),
    (Weapons.R_77_, Weapons.R_27ER),

    # R-73 (AA-11)
    (Weapons.R_73, Weapons.R_60M),
    (Weapons.R_73_, Weapons.R_60M_),

    # GBU-38 (JDAM)
    (Weapons.GBU_38, Weapons.GBU_12),
    (Weapons.GBU_38_16, Weapons.MK_82_28), # B1-B only
    (Weapons._2_GBU_38_, Weapons._2_GBU_12),
    (Weapons._2_GBU_38, Weapons._2_GBU_12),
    (Weapons._3_GBU_38, Weapons._3_GBU_12),
    (Weapons.BRU_55___2_x_GBU_38, Weapons.BRU_33___2_x_GBU_12),
    (Weapons.BRU_57___2_x_GBU_38, Weapons.BRU_33___2_x_GBU_12),

    # AGM-154A (JSOW)
    (Weapons.AGM_154A, Weapons.GBU_12),
    (Weapons.BRU_55___2_x_AGM_154A, Weapons.BRU_33___2_x_GBU_12),
    (Weapons.BRU_57___2_x_AGM_154A, Weapons.BRU_33___2_x_GBU_12),

    # AGM-154C (JSOW)
    (Weapons.AGM_154C, Weapons.GBU_12),
    (Weapons.AGM_154C_4, Weapons.MK_82_28), # B1-B only
    (Weapons.BRU_55___2_x_AGM_154C, Weapons.BRU_33___2_x_GBU_12),

    # AGM-84E (SLAM)
    (Weapons.AGM_84E, Weapons.LAU_117_AGM_65F),

    # CBU-97
    (Weapons.CBU_97, Weapons.GBU_12),
    (Weapons.TER_9A___2_x_CBU_97, Weapons.TER_9A___2_x_GBU_12),
    (Weapons.TER_9A___2_x_CBU_97_, Weapons.TER_9A___2_x_GBU_12),
    (Weapons.TER_9A___3_x_CBU_97, Weapons.TER_9A___2_x_GBU_12),

]

WEAPON_FALLBACK_MAP: Dict[Weapon, Optional[Weapon]] = defaultdict(
    lambda: cast(Optional[Weapon], None),
    ((Weapon.from_pydcs(a), b if b is None else Weapon.from_pydcs(b))
     for a, b in _WEAPON_FALLBACKS))


WEAPON_INTRODUCTION_YEARS = {
    # AIM-120C
    Weapon.from_pydcs(Weapons.AIM_120C): 1996,
    Weapon.from_pydcs(Weapons.LAU_115_2_LAU_127_AIM_120C): 1996,
    Weapon.from_pydcs(Weapons.LAU_115___AIM_120C): 1996,

    # AIM-120B
    Weapon.from_pydcs(Weapons.AIM_120B): 1994,
    Weapon.from_pydcs(Weapons.LAU_115_2_LAU_127_AIM_120B): 1994,
    Weapon.from_pydcs(Weapons.LAU_115___AIM_120B): 1994,

    # AIM-7MH
    Weapon.from_pydcs(Weapons.AIM_7MH): 1987,
    Weapon.from_pydcs(Weapons.LAU_115C_AIM_7MH): 1987,

    # AIM-7M
    Weapon.from_pydcs(Weapons.AIM_7M): 1982,
    Weapon.from_pydcs(Weapons.LAU_115___AIM_7M): 1982,

    # AIM-7F
    Weapon.from_pydcs(Weapons.AIM_7F): 1976,
    Weapon.from_pydcs(Weapons.LAU_115C_AIM_7F): 1976,

    # AIM-7E
    Weapon.from_pydcs(Weapons.AIM_7E): 1963,
    Weapon.from_pydcs(Weapons.LAU_115C_AIM_7E): 1963,

    # AIM-9X
    Weapon.from_pydcs(Weapons.AIM_9X_Sidewinder_IR_AAM): 2003,
    Weapon.from_pydcs(Weapons.LAU_7_AIM_9X_Sidewinder_IR_AAM): 2003,
    Weapon.from_pydcs(Weapons.LAU_115_LAU_127_AIM_9X): 2003,
    Weapon.from_pydcs(Weapons.LAU_115_2_LAU_127_AIM_9X): 2003,
    Weapon.from_pydcs(Weapons.LAU_127_AIM_9X): 2003,

    # AIM-9P5
    Weapon.from_pydcs(Weapons.AIM_9P5_Sidewinder_IR_AAM): 1963,
    Weapon.from_pydcs(Weapons.LAU_7_AIM_9P5_Sidewinder_IR_AAM): 1963,

    # AIM-9P
    Weapon.from_pydcs(Weapons.AIM_9P_Sidewinder_IR_AAM): 1978,
    Weapon.from_pydcs(Weapons.LAU_7_AIM_9P_Sidewinder_IR_AAM): 1978,

    # AIM-9M
    Weapon.from_pydcs(Weapons.AIM_9M_Sidewinder_IR_AAM): 1983,
    Weapon.from_pydcs(Weapons.LAU_7_AIM_9M_Sidewinder_IR_AAM): 1983,

    # AIM-9L
    Weapon.from_pydcs(Weapons.AIM_9L_Sidewinder_IR_AAM): 1977,
    Weapon.from_pydcs(Weapons.LAU_7_AIM_9L): 1977,

    # R-77 (AA-12)
    Weapon.from_pydcs(Weapons.R_77): 2002,
    Weapon.from_pydcs(Weapons.R_77_): 2002,

    # R-73 (AA-11)
    Weapon.from_pydcs(Weapons.R_73): 1989,
    Weapon.from_pydcs(Weapons.R_73_): 1989,

    # GBU-38 (JDAM)
    Weapon.from_pydcs(Weapons.GBU_38): 1998,
    Weapon.from_pydcs(Weapons.GBU_38_16): 1998,
    Weapon.from_pydcs(Weapons._2_GBU_38_): 1998,
    Weapon.from_pydcs(Weapons._2_GBU_38): 1998,
    Weapon.from_pydcs(Weapons._3_GBU_38): 1998,
    Weapon.from_pydcs(Weapons.BRU_55___2_x_GBU_38): 1998,
    Weapon.from_pydcs(Weapons.BRU_57___2_x_GBU_38): 1998,

    # AGM-154A (JSOW)
    Weapon.from_pydcs(Weapons.AGM_154A): 1999,
    Weapon.from_pydcs(Weapons.BRU_55___2_x_AGM_154A): 1999,
    Weapon.from_pydcs(Weapons.BRU_57___2_x_AGM_154A): 1999,

    # AGM-154C (JSOW)
    Weapon.from_pydcs(Weapons.AGM_154C): 2005,
    Weapon.from_pydcs(Weapons.AGM_154C_4): 2005,
    Weapon.from_pydcs(Weapons.BRU_55___2_x_AGM_154C): 2005,

    # AGM-84E
    Weapon.from_pydcs(Weapons.AGM_84E): 1990,

    # CBU-97
    Weapons.CBU_97: 1995,
    Weapons.TER_9A___2_x_CBU_97: 1995,
    Weapons.TER_9A___2_x_CBU_97_: 1995,
    Weapons.TER_9A___3_x_CBU_97: 1995

}
