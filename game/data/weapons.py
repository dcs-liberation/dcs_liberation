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
    # ADM-141 TALD
    (Weapons.ADM_141A, None),
    (Weapons.ADM_141A_, None),
    (Weapons.ADM_141A__, None),
    (Weapons.ADM_141B, None),
    
    # AGM-114K Hellfire
    (Weapons.AGM114x2_OH_58, Weapons.M260_HYDRA), # assuming OH-58 and not MQ-9
    (Weapons.AGM_114K, None), # Only for RQ-1
    (Weapons.AGM_114K___4, Weapons.LAU_61___19_2_75__rockets_MK151_HE),
    
    # AGM-119 Penguin
    (Weapons.AGM_119B_Penguin, Weapons.Mk_82),
    
    # AGM-122 Sidearm
    (Weapons.AGM_122, None), # No known aircraft carries this
    (Weapons.AGM_122_Sidearm, Weapons.GBU_12), # outer pylons harrier
    (Weapons.AGM_122_Sidearm_, Weapons.LAU_117_AGM_65E), # internal pylons harrier
    
    # AGM-154 JSOW
    (Weapons.AGM_154A, Weapons.GBU_12),
    (Weapons.BRU_55___2_x_AGM_154A, Weapons.BRU_33___2_x_GBU_12),
    (Weapons.BRU_57___2_x_AGM_154A, None), # doesn't exist on any aircraft yet
    
    (Weapons.AGM_154B, Weapons.CBU_105),
    
    (Weapons.AGM_154C, Weapons.GBU_12),
    (Weapons.AGM_154C_4, Weapons.GBU_31_8),
    (Weapons.BRU_55___2_x_AGM_154C, Weapons.BRU_33___2_x_GBU_12),
    
    # AGM-45 Shrike
    (Weapons.AGM_45A, None),
    (Weapons.AGM_45B, Weapons.AGM_45A),
    (Weapons.AGM_45B_, Weapons.AGM_45A),
    
    # AGM-62 Walleye
    (Weapons.AGM_62, Weapons.Mk_84),
    
    # AGM-65 Maverick
    (Weapons.AGM_65D, None), # doesn't exist
    (Weapons.AGM_65E, None), # doesn't exist
    (Weapons.AGM_65F, None), # doesn't exist
    (Weapons.LAU_117_AGM_65A, None), # doesn't exist
    (Weapons.LAU_117_AGM_65B, None), # doesn't exist
    
    (Weapons.LAU_117_AGM_65D, Weapons.AGM_62), # Walleye is the predecessor to the maverick
    (Weapons.LAU_117_AGM_65E, Weapons.LAU_117_AGM_65D),
    (Weapons.LAU_117_AGM_65F, Weapons.LAU_117_AGM_65D),
    (Weapons.LAU_117_AGM_65G, Weapons.LAU_117_AGM_65D),
    (Weapons.LAU_117_AGM_65H, Weapons.LAU_117_AGM_65D),
    (Weapons.LAU_117_AGM_65K, Weapons.LAU_117_AGM_65D),
    (Weapons.LAU_117_AGM_65L, Weapons.LAU_117_AGM_65D),
    
    (Weapons.LAU_88_AGM_65D_2, None),
    (Weapons.LAU_88_AGM_65D_2_, None),
    (Weapons.LAU_88_AGM_65D_3, None),
    (Weapons.LAU_88_AGM_65D_ONE, None),
    
    (Weapons.LAU_88_AGM_65E_2, Weapons.LAU_88_AGM_65D_2),
    (Weapons.LAU_88_AGM_65E_2_, Weapons.LAU_88_AGM_65D_2_),
    (Weapons.LAU_88_AGM_65E_3, Weapons.LAU_88_AGM_65D_3),
    
    (Weapons.LAU_88_AGM_65H, Weapons.LAU_88_AGM_65D_2),
    (Weapons.LAU_88_AGM_65H_2_L, Weapons.LAU_88_AGM_65D_2_),
    (Weapons.LAU_88_AGM_65H_2_R, Weapons.LAU_88_AGM_65D_2_),
    (Weapons.LAU_88_AGM_65H_3, Weapons.LAU_88_AGM_65D_3),
    
    (Weapons.LAU_88_AGM_65K_2, Weapons.LAU_88_AGM_65D_2),
    (Weapons.LAU_88_AGM_65K_2_, Weapons.LAU_88_AGM_65D_2_),
    (Weapons.LAU_88_AGM_65K_3, Weapons.LAU_88_AGM_65D_3),
    
    # AGM-84 Harpoon
    (Weapons.AGM_84, None), # doesn't exist
    (Weapons.AGM_84A, Weapons.Mk_82),
    (Weapons.AGM_84A_8, Weapons._27_Mk_82),
    (Weapons.AGM_84D, Weapons.AGM_62),
    (Weapons.AGM_84E, Weapons.LAU_117_AGM_65F),
    (Weapons.AGM_84H, Weapons.AGM_84E),
    
    # AGM-86 ALCM
    (Weapons.AGM_86C, Weapons._27_Mk_82),
    (Weapons.AGM_86C_20, Weapons._27_Mk_82),
    (Weapons.AGM_86C_8, Weapons._27_Mk_82),
    (Weapons.MER_6_AGM_86C, Weapons.MER_12_Mk_82),
    
    # AGM-88 HARM
    (Weapons.AGM_88C, Weapons.AGM_65D),
    (Weapons.AGM_88C_, Weapons.AGM_65D),
    
    # AIM-120 AMRAAM    
    (Weapons.AIM_120B, Weapons.AIM_7MH),
    (Weapons.LAU_115___AIM_120B, Weapons.LAU_115C_AIM_7MH),
    (Weapons.LAU_115_2_LAU_127_AIM_120B, Weapons.LAU_115C_AIM_7MH),
    
    (Weapons.AIM_120C, Weapons.AIM_120B),
    (Weapons.LAU_115___AIM_120C, Weapons.LAU_115___AIM_120B),
    (Weapons.LAU_115_2_LAU_127_AIM_120C, Weapons.LAU_115_2_LAU_127_AIM_120B),
    
    # AIM-54 Phoenix
    (Weapons.AIM_54A_Mk47, None),
    (Weapons.AIM_54A_Mk47_, None),
    (Weapons.AIM_54A_Mk47__, None),
    
    (Weapons.AIM_54A_Mk60, Weapons.AIM_54A_Mk47),
    (Weapons.AIM_54A_Mk60_, Weapons.AIM_54A_Mk47_),
    (Weapons.AIM_54A_Mk60__, Weapons.AIM_54A_Mk47__),
    
    (Weapons.AIM_54C_Mk47, Weapons.AIM_54A_Mk60),
    (Weapons.AIM_54C_Mk47_, Weapons.AIM_54A_Mk60_),
    (Weapons.AIM_54C_Mk47__, Weapons.AIM_54A_Mk60__),
    
    # AIM-7 Sparrow
    (Weapons.AIM_7E),
    (Weapons.AIM_7F, Weapons.AIM_7E),
    (Weapons.AIM_7F_, None),
    (Weapons.AIM_7F__, None),
    (Weapons.AIM_7M, Weapons.AIM_7F),
    (Weapons.AIM_7M_, Weapons.AIM_7F_),
    (Weapons.AIM_7M__, Weapons.AIM_7F__),
    (Weapons.AIM_7MH, AIM_7M),
    (Weapons.AIM_7MH_, AIM_7M_),
    (Weapons.AIM_7MH__, AIM_7M__),
    
    (Weapons.LAU_115C_AIM_7E, None),
    (Weapons.LAU_115C_AIM_7F, Weapons.LAU_115C_AIM_7E),
    (Weapons.LAU_115___AIM_7M, Weapons.LAU_115C_AIM_7F),
    (Weapons.LAU_115C_AIM_7MH, Weapons.LAU_115___AIM_7M),
    
    # AIM-9 Sidewinder
    (Weapons.AIM_9L_Sidewinder_IR_AAM, None),
    (Weapons.AIM_9M_Sidewinder_IR_AAM, Weapons.AIM_9P5_Sidewinder_IR_AAM),
    (Weapons.AIM_9P5_Sidewinder_IR_AAM, Weapons.AIM_9P_Sidewinder_IR_AAM),
    (Weapons.AIM_9P_Sidewinder_IR_AAM, Weapons.AIM_9L_Sidewinder_IR_AAM),
    (Weapons.AIM_9X_Sidewinder_IR_AAM, Weapons.AIM_9P_Sidewinder_IR_AAM),
    
    (Weapons.LAU_105_1_AIM_9L_L, None),
    (Weapons.LAU_105_1_AIM_9L_R, None),
    (Weapons.LAU_105_1_AIM_9M_L, Weapons.LAU_105_1_AIM_9L_L),
    (Weapons.LAU_105_1_AIM_9M_R, Weapons.LAU_105_1_AIM_9L_R),
    
    (Weapons.LAU_105_2_AIM_9L, None),
    (Weapons.LAU_105_2_AIM_9P5, LAU_105___2_AIM_9P_Sidewinder_IR_AAM),
    
    (Weapons.LAU_105___2_AIM_9M_Sidewinder_IR_AAM, LAU_105_2_AIM_9L),
    (Weapons.LAU_105___2_AIM_9P_Sidewinder_IR_AAM, LAU_105___2_AIM_9M_Sidewinder_IR_AAM),
    
    (Weapons.LAU_115_2_LAU_127_AIM_9L, None),
    (Weapons.LAU_115_2_LAU_127_AIM_9M, Weapons.LAU_115_2_LAU_127_AIM_9L),
    (Weapons.LAU_115_2_LAU_127_AIM_9X, Weapons.LAU_115_2_LAU_127_AIM_9M),
    
    (Weapons.LAU_115_LAU_127_AIM_9L, None),
    (Weapons.LAU_115_LAU_127_AIM_9M, Weapons.LAU_115_LAU_127_AIM_9L),
    (Weapons.LAU_115_LAU_127_AIM_9X, Weapons.LAU_115_LAU_127_AIM_9M),
    
    (Weapons.LAU_127_AIM_9L, None),
    (Weapons.LAU_127_AIM_9M, Weapons.LAU_127_AIM_9L),
    (Weapons.LAU_127_AIM_9X, Weapons.LAU_127_AIM_9M),
    
    (Weapons.LAU_138_AIM_9L, None),
    (Weapons.LAU_138_AIM_9M, Weapons.LAU_138_AIM_9L),
    
    (Weapons.LAU_7_AIM_9L, None),
    (Weapons.LAU_7_AIM_9M, Weapons.LAU_7_AIM_9L),
    (Weapons.LAU_7_AIM_9M_Sidewinder_IR_AAM, Weapons.LAU_7_AIM_9P5_Sidewinder_IR_AAM),
    (Weapons.LAU_7_AIM_9P5_Sidewinder_IR_AAM, Weapons.LAU_7_AIM_9P_Sidewinder_IR_AAM),
    (Weapons.LAU_7_AIM_9P_Sidewinder_IR_AAM, Weapons.LAU_7_AIM_9L),
    (Weapons.LAU_7_AIM_9X_Sidewinder_IR_AAM, Weapons.LAU_7_AIM_9M_Sidewinder_IR_AAM),
    
    (Weapons.LAU_7___2_AIM_9L_Sidewinder_IR_AAM, None),
    (Weapons.LAU_7___2_AIM_9M_Sidewinder_IR_AAM, Weapons.LAU_7___2_AIM_9P5_Sidewinder_IR_AAM),
    (Weapons.LAU_7___2_AIM_9P5_Sidewinder_IR_AAM, Weapons.LAU_7___2_AIM_9P_Sidewinder_IR_AAM),
    (Weapons.LAU_7___2_AIM_9P_Sidewinder_IR_AAM, Weapons.LAU_7___2_AIM_9L_Sidewinder_IR_AAM),
    
    # ALQ ECM Pods
    (Weapons.ALQ_131, None),
    (Weapons.ALQ_184, Weapons.ALQ_131),
    (Weapons.AN_ALQ_164_DECM_Pod, None),
    
    # TGP Pods
    (Weapons.AN_AAQ_28_LITENING_, None),
    (Weapons.AN_AAQ_28_LITENING, Weapons.Lantirn_F_16),
    (Weapons.AN_AAS_38_FLIR, None),
    (Weapons.AN_ASQ_173_LST_SCAM, None),
    (Weapons.AWW_13_DATALINK_POD, None),
    (Weapons.LANTIRN_Targeting_Pod, None),
    (Weapons.Lantirn_F_16, None),
    (Weapons.Lantirn_Target_Pod, None),
    (Weapons.Pavetack_F_111, None),
    
    # BLU-107
    (Weapons.BLU_107, None),
    (Weapons.MER_6_BLU_107, Weapons.MER_6_Mk_82),

    # GBU-10 LGB
    (Weapons.DIS_GBU_10, Weapons.Mk_84),
    (Weapons.GBU_10, Weapons.Mk_84),
    (Weapons.GBU_10_, Weapons.Mk_84),
    (Weapons.GBU_10_2, Weapons.Mk_84),
    
    # GBU-12 LGB
    (Weapons.AUF2_GBU_12_x_2, None),
    (Weapons.BRU_33___2_x_GBU_12, Weapons.BRU_33___2_x_Mk_82_),
    (Weapons.BRU_42_3_GBU_12, Weapons._3_Mk_82),
    (Weapons.DIS_GBU_12, Weapons.Mk_82),
    (Weapons.DIS_GBU_12_DUAL, Weapons.BRU_33___2_x_Mk_82_),
    (Weapons.DIS_GBU_12_DUAL_L, Weapons.BRU_33___2_x_Mk_82_),
    (Weapons.DIS_GBU_12_DUAL_R, Weapons.BRU_33___2_x_Mk_82_),
    (Weapons.GBU_12, Weapons.Mk_82),
    (Weapons.GBU_12_, Weapons.Mk_82_),
    (Weapons.TER_9A___2_x_GBU_12, Weapons.TER_9A___2_x_Mk_82),
    (Weapons.TER_9A___2_x_GBU_12_, Weapons.TER_9A___2_x_Mk_82_),
    (Weapons._2xGBU_12, Weapons.Mk_82),
    (Weapons._2xGBU_12_, Weapons.Mk_82_),
    (Weapons._2_GBU_12, Weapons._2_Mk_82),
    (Weapons._2_GBU_12_, Weapons._2_Mk_82_),
    (Weapons._3_GBU_12, Weapons._3_Mk_82_),
    
    # GBU-15 LGB
    (Weapons.GBU_15, Weapons.Mk_84),
    
    # GBU-16 LGB
    (Weapons.BRU_33___2_x_GBU_16, None),
    (Weapons.DIS_GBU_16,  Weapons.Mk_83),
    (Weapons.GBU_16,  Weapons.Mk_83),
    (Weapons.GBU_16_,  Weapons.Mk_83_),
    
    # GBU-24 LGB
    (Weapons.GBU_24, Weapons.GBU_10),
    (Weapons.GBU_24_, Weapons.GBU_10_),
    (Weapons.GBU_24__, Weapons.GBU_10_),
    
    # GBU-27 LGB
    (Weapons.GBU_24, Weapons.GBU_10),
    (Weapons.GBU_24_, Weapons.GBU_10_),
    (Weapons.GBU_24__, Weapons.GBU_10_),
    
    # GBU-28 LGB
    (Weapons.GBU_28, Weapons.GBU_15),
    
    # GBU-31 JDAM
    (Weapons.GBU_31V3B_8, Weapons.B_1B_Mk_84_8),
    (Weapons.GBU_31_8, Weapons.B_1B_Mk_84_8),
    (Weapons.GBU_31_V_1_B, Weapons.Mk_84),
    (Weapons.GBU_31_V_2_B, Weapons.Mk_84),
    (Weapons.GBU_31_V_3_B, Weapons.Mk_84),
    (Weapons.GBU_31_V_4_B, Weapons.Mk_84),
    
    # GBU-32 JDAM
    (Weapons.GBU_32_V_2_B, Weapons.Mk_83),
    
    # GBU-32 JDAM
    (Weapons.BRU_55___2_x_GBU_38, Weapons.BRU_33___2_x_Mk_82_),
    (Weapons.BRU_57___2_x_GBU_38, None), # Doesn't exist
    (Weapons.GBU_38, Weapons.Mk_82),
    (Weapons.GBU_38_16, Weapons.MK_82_28),
    (Weapons._2_GBU_38, Weapons._2_Mk_82),
    (Weapons._2_GBU_38_, Weapons._2_Mk_82_),
    (Weapons._3_GBU_38, Weapons._3_Mk_82_),
    
    # GBU-54 LJDAM
    (Weapons.GBU_54_V_1_B, Weapons.GBU_38),
    (Weapons._2_GBU_54_V_1_B, Weapons._2_GBU_38),
    (Weapons._2_GBU_54_V_1_B_, Weapons._2_GBU_38_),
    (Weapons._3_GBU_54_V_1_B, Weapons._3_GBU_38),
    
    # CBU-52
    (Weapons.CBU_52B, None),
    
    # CBU-87 CEM
    (Weapons.CBU_87, Weapons.Mk_82),
    (Weapons.TER_9A___2_x_CBU_87, Weapons.TER_9A___2_x_Mk_82),
    (Weapons.TER_9A___2_x_CBU_87_, Weapons.TER_9A___2_x_Mk_82_),
    (Weapons.TER_9A___3_x_CBU_87, Weapons.TER_9A___3_x_Mk_82),
    
    # CBU-97
    (Weapons.CBU_97, Weapons.Mk_82),
    (Weapons.TER_9A___2_x_CBU_97, Weapons.TER_9A___2_x_Mk_82),
    (Weapons.TER_9A___2_x_CBU_97_, Weapons.TER_9A___2_x_Mk_82_),
    (Weapons.TER_9A___3_x_CBU_97, Weapons.TER_9A___3_x_Mk_82),
    
    # CBU-99 (It's a bomb made in 1968, I'm not bothering right now with backups)
    
    # CBU-103
    (Weapons.BRU_57___2_x_CBU_103, None), # doesn't exist...
    (Weapons.CBU_103, Weapons.CBU_87),
    
    # CBU-105
    (Weapons.BRU_57___2_x_CBU_105, None), # doesn't exist...
    (Weapons.CBU_105, Weapons.CBU_97),
    
]

WEAPON_FALLBACK_MAP: Dict[Weapon, Optional[Weapon]] = defaultdict(
    lambda: cast(Optional[Weapon], None),
    ((Weapon.from_pydcs(a), b if b is None else Weapon.from_pydcs(b))
     for a, b in _WEAPON_FALLBACKS))


WEAPON_INTRODUCTION_YEARS = {
    # USA
    # ADM-141 TALD
    Weapon.from_pydcs(Weapons.ADM_141A): 1987,
    Weapon.from_pydcs(Weapons.ADM_141A_): 1987,
    Weapon.from_pydcs(Weapons.ADM_141A__): 1987,
    Weapon.from_pydcs(Weapons.ADM_141B): 1987,
    
    # AGM-114K Hellfire
    Weapon.from_pydcs(Weapons.AGM114x2_OH_58): 1993,
    Weapon.from_pydcs(Weapons.AGM_114K): 1993,
    Weapon.from_pydcs(Weapons.AGM_114K___4): 1993,
    
    # AGM-119 Penguin
    Weapon.from_pydcs(Weapons.AGM_119B_Penguin): 1972,
    
    # AGM-122 Sidearm
    Weapon.from_pydcs(Weapons.AGM_122): 1986,
    Weapon.from_pydcs(Weapons.AGM_122_Sidearm): 1986,
    Weapon.from_pydcs(Weapons.AGM_122_Sidearm_): 1986,
    
    # AGM-154 JSOW
    Weapon.from_pydcs(Weapons.AGM_154A): 1998,
    Weapon.from_pydcs(Weapons.BRU_55___2_x_AGM_154A): 1998,
    Weapon.from_pydcs(Weapons.BRU_57___2_x_AGM_154A): 1998,
    
    Weapon.from_pydcs(Weapons.AGM_154B): 2005,
    
    Weapon.from_pydcs(Weapons.AGM_154C): 2005,
    Weapon.from_pydcs(Weapons.AGM_154C_4): 2005,
    Weapon.from_pydcs(Weapons.BRU_55___2_x_AGM_154C): 2005,
    
    # AGM-45 Shrike
    Weapon.from_pydcs(Weapons.AGM_45A): 1965,
    Weapon.from_pydcs(Weapons.AGM_45B): 1970,
    Weapon.from_pydcs(Weapons.AGM_45B_): 1970,
    
    # AGM-62 Walleye
    Weapon.from_pydcs(Weapons.AGM_62): 1967,
    
    # AGM-65 Maverick
    Weapon.from_pydcs(Weapons.AGM_65D): 1983,
    Weapon.from_pydcs(Weapons.AGM_65E): 1985,
    Weapon.from_pydcs(Weapons.AGM_65K): 2007,
    
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65A): 1972,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65B): 1972,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65D): 1983,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65E): 1985,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65F): 1989,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65G): 1989,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65H): 2007,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65K): 2007,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65L): 1985,
    
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65D_2): 1983,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65D_2_): 1983,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65D_3): 1983,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65D_ONE): 1983,
    
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65E_2): 1985,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65E_2_): 1985,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65E_3): 1985,
    
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65H): 2007,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65H_2_L): 2007,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65H_2_R): 2007,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65H_3): 2007,
    
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65K_2): 2007,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65K_2_): 2007,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65K_3): 2007,
    
    # AGM-84 Harpoon
    Weapon.from_pydcs(Weapons.AGM_84): 1979,
    Weapon.from_pydcs(Weapons.AGM_84A): 1979,
    Weapon.from_pydcs(Weapons.AGM_84A_8): 1979,
    Weapon.from_pydcs(Weapons.AGM_84D): 1979,
    Weapon.from_pydcs(Weapons.AGM_84E): 1990,
    Weapon.from_pydcs(Weapons.AGM_84E_SLAM): 1990,
    Weapon.from_pydcs(Weapons.AGM_84H): 1998,
    
    # AGM-86 ALCM
    Weapon.from_pydcs(Weapons.AGM_86C): 1986,
    Weapon.from_pydcs(Weapons.AGM_86C_20): 1986,
    Weapon.from_pydcs(Weapons.AGM_86C_8): 1986,
    Weapon.from_pydcs(Weapons.MER_6_AGM_86C): 1986,
    
    # AGM-88 HARM
    Weapon.from_pydcs(Weapons.AGM_88C): 1985,
    Weapon.from_pydcs(Weapons.AGM_88C_): 1985,
    
    # AIM-120 AMRAAM
    Weapon.from_pydcs(Weapons.AIM_120B): 1994,
    Weapon.from_pydcs(Weapons.AIM_120C): 1996,
    
    Weapon.from_pydcs(Weapons.LAU_115_2_LAU_127_AIM_120B): 1994,
    Weapon.from_pydcs(Weapons.LAU_115___AIM_120B): 1994,
    Weapon.from_pydcs(Weapons.LAU_115_2_LAU_127_AIM_120C): 1996,
    Weapon.from_pydcs(Weapons.LAU_115___AIM_120C): 1996,
    
    # AIM-54 Phoenix
    Weapon.from_pydcs(Weapons.AIM_54A_Mk47): 1974,
    Weapon.from_pydcs(Weapons.AIM_54A_Mk47_): 1974,
    Weapon.from_pydcs(Weapons.AIM_54A_Mk47__): 1974,
    
    Weapon.from_pydcs(Weapons.AIM_54A_Mk60): 1974,
    Weapon.from_pydcs(Weapons.AIM_54A_Mk60_): 1974,
    Weapon.from_pydcs(Weapons.AIM_54A_Mk60__): 1974,
    
    Weapon.from_pydcs(Weapons.AIM_54C): 1974,
    Weapon.from_pydcs(Weapons.AIM_54C_Mk47): 1974,
    Weapon.from_pydcs(Weapons.AIM_54C_Mk47_): 1974,
    Weapon.from_pydcs(Weapons.AIM_54C_Mk47__): 1974,
    
    # AIM-7 Sparrow
    Weapon.from_pydcs(Weapons.AIM_7E): 1963,
    Weapon.from_pydcs(Weapons.AIM_7F): 1976,
    Weapon.from_pydcs(Weapons.AIM_7F_): 1976,
    Weapon.from_pydcs(Weapons.AIM_7F__): 1976,
    Weapon.from_pydcs(Weapons.AIM_7M): 1982,
    Weapon.from_pydcs(Weapons.AIM_7M_): 1982,
    Weapon.from_pydcs(Weapons.AIM_7M__): 1982,
    Weapon.from_pydcs(Weapons.AIM_7MH): 1987,
    Weapon.from_pydcs(Weapons.AIM_7MH_): 1987,
    Weapon.from_pydcs(Weapons.AIM_7MH__): 1987,
    
    Weapon.from_pydcs(Weapons.LAU_115C_AIM_7E): 1963,
    Weapon.from_pydcs(Weapons.LAU_115C_AIM_7F): 1976,
    Weapon.from_pydcs(Weapons.LAU_115___AIM_7M): 1982,
    Weapon.from_pydcs(Weapons.LAU_115C_AIM_7MH): 1987,
    
    # AIM-9 Sidewinder
    Weapon.from_pydcs(Weapons.AIM_9L_Sidewinder_IR_AAM): 1977,
    Weapon.from_pydcs(Weapons.AIM_9M_Sidewinder_IR_AAM): 1982,
    Weapon.from_pydcs(Weapons.AIM_9P5_Sidewinder_IR_AAM): 1980,
    Weapon.from_pydcs(Weapons.AIM_9P_Sidewinder_IR_AAM): 1978,
    Weapon.from_pydcs(Weapons.AIM_9X_Sidewinder_IR_AAM): 2003,
    
    Weapon.from_pydcs(Weapons.LAU_105_1_AIM_9L_L): 1977,
    Weapon.from_pydcs(Weapons.LAU_105_1_AIM_9L_R): 1977,
    Weapon.from_pydcs(Weapons.LAU_105_1_AIM_9M_L): 1982,
    Weapon.from_pydcs(Weapons.LAU_105_1_AIM_9M_R): 1982,
    
    Weapon.from_pydcs(Weapons.LAU_105_2_AIM_9L): 1977,
    Weapon.from_pydcs(Weapons.LAU_105_2_AIM_9P5): 1980,
    
    Weapon.from_pydcs(Weapons.LAU_105___2_AIM_9M_Sidewinder_IR_AAM): 1982,
    Weapon.from_pydcs(Weapons.LAU_105___2_AIM_9P_Sidewinder_IR_AAM): 1978,
    
    Weapon.from_pydcs(Weapons.LAU_115_2_LAU_127_AIM_9L): 1977,
    Weapon.from_pydcs(Weapons.LAU_115_2_LAU_127_AIM_9M): 1982,
    Weapon.from_pydcs(Weapons.LAU_115_2_LAU_127_AIM_9X): 2003,
    
    Weapon.from_pydcs(Weapons.LAU_115_LAU_127_AIM_9L): 1977,
    Weapon.from_pydcs(Weapons.LAU_115_LAU_127_AIM_9M): 1982,
    Weapon.from_pydcs(Weapons.LAU_115_LAU_127_AIM_9X): 2003,
    
    Weapon.from_pydcs(Weapons.LAU_127_AIM_9L): 1977,
    Weapon.from_pydcs(Weapons.LAU_127_AIM_9M): 1982,
    Weapon.from_pydcs(Weapons.LAU_127_AIM_9X): 2003,
    
    Weapon.from_pydcs(Weapons.LAU_138_AIM_9L): 1977,
    Weapon.from_pydcs(Weapons.LAU_138_AIM_9M): 1982,
    
    Weapon.from_pydcs(Weapons.LAU_7_AIM_9L): 1977,
    Weapon.from_pydcs(Weapons.LAU_7_AIM_9M): 1982,
    Weapon.from_pydcs(Weapons.LAU_7_AIM_9M_Sidewinder_IR_AAM): 1982,
    Weapon.from_pydcs(Weapons.LAU_7_AIM_9P5_Sidewinder_IR_AAM): 1980,
    Weapon.from_pydcs(Weapons.LAU_7_AIM_9P_Sidewinder_IR_AAM): 1978,
    Weapon.from_pydcs(Weapons.LAU_7_AIM_9X_Sidewinder_IR_AAM): 2003,
    
    Weapon.from_pydcs(Weapons.LAU_7___2_AIM_9L_Sidewinder_IR_AAM): 1977,
    Weapon.from_pydcs(Weapons.LAU_7___2_AIM_9M_Sidewinder_IR_AAM): 1982,
    Weapon.from_pydcs(Weapons.LAU_7___2_AIM_9P5_Sidewinder_IR_AAM): 1980,
    Weapon.from_pydcs(Weapons.LAU_7___2_AIM_9P_Sidewinder_IR_AAM): 1978,
    
    # ALQ ECM Pods
    Weapon.from_pydcs(Weapons.ALQ_131): 1970,
    Weapon.from_pydcs(Weapons.ALQ_184): 1989,
    Weapon.from_pydcs(Weapons.AN_ALQ_164_DECM_Pod): 1984,
    
    # TGP Pods
    Weapon.from_pydcs(Weapons.AN_AAQ_28_LITENING): 1995,
    Weapon.from_pydcs(Weapons.AN_AAQ_28_LITENING_): 1995,
    Weapon.from_pydcs(Weapons.AN_AAS_38_FLIR): 1993,
    Weapon.from_pydcs(Weapons.AN_ASQ_173_LST_SCAM): 1993,
    Weapon.from_pydcs(Weapons.AWW_13_DATALINK_POD): 1967,
    Weapon.from_pydcs(Weapons.LANTIRN_Targeting_Pod): 1985,
    Weapon.from_pydcs(Weapons.Lantirn_F_16): 1985,
    Weapon.from_pydcs(Weapons.Lantirn_Target_Pod): 1985,
    Weapon.from_pydcs(Weapons.Pavetack_F_111): 1982,
    
    # BLU-107
    Weapon.from_pydcs(Weapons.BLU_107): 1983,
    Weapon.from_pydcs(Weapons.MER_6_BLU_107): 1983,

    # GBU-10 LGB
    Weapon.from_pydcs(Weapons.DIS_GBU_10): 1976,
    Weapon.from_pydcs(Weapons.GBU_10): 1976,
    Weapon.from_pydcs(Weapons.GBU_10_): 1976,
    Weapon.from_pydcs(Weapons.GBU_10_2): 1976,
    
    # GBU-12 LGB
    Weapon.from_pydcs(Weapons.AUF2_GBU_12_x_2): 1976,
    Weapon.from_pydcs(Weapons.BRU_33___2_x_GBU_12): 1976,
    Weapon.from_pydcs(Weapons.BRU_42_3_GBU_12): 1976,
    Weapon.from_pydcs(Weapons.DIS_GBU_12): 1976,
    Weapon.from_pydcs(Weapons.DIS_GBU_12_DUAL): 1976,
    Weapon.from_pydcs(Weapons.DIS_GBU_12_DUAL_L): 1976,
    Weapon.from_pydcs(Weapons.DIS_GBU_12_DUAL_R): 1976,
    Weapon.from_pydcs(Weapons.GBU_12): 1976,
    Weapon.from_pydcs(Weapons.GBU_12_): 1976,
    Weapon.from_pydcs(Weapons.TER_9A___2_x_GBU_12): 1976,
    Weapon.from_pydcs(Weapons.TER_9A___2_x_GBU_12_): 1976,
    Weapon.from_pydcs(Weapons._2xGBU_12): 1976,
    Weapon.from_pydcs(Weapons._2xGBU_12_): 1976,
    Weapon.from_pydcs(Weapons._2_GBU_12): 1976,
    Weapon.from_pydcs(Weapons._2_GBU_12_): 1976,
    Weapon.from_pydcs(Weapons._3_GBU_12): 1976,
    
    # GBU-15 LGB
    Weapon.from_pydcs(Weapons.GBU_15): 1975,
    
    # GBU-16 LGB
    Weapon.from_pydcs(Weapons.BRU_33___2_x_GBU_16): 1976,
    Weapon.from_pydcs(Weapons.DIS_GBU_16): 1976,
    Weapon.from_pydcs(Weapons.GBU_16): 1976,
    Weapon.from_pydcs(Weapons.GBU_16_): 1976,
    Weapon.from_pydcs(Weapons._2_GBU_16): 1976,
    Weapon.from_pydcs(Weapons._2_GBU_16_): 1976,
    Weapon.from_pydcs(Weapons._3_GBU_16): 1976,
    Weapon.from_pydcs(Weapons._3_GBU_16_): 1976,
    
    # GBU-24 LGB
    Weapon.from_pydcs(Weapons.GBU_24): 1983,
    Weapon.from_pydcs(Weapons.GBU_24_): 1983,
    Weapon.from_pydcs(Weapons.GBU_24__): 1983,
    
    # GBU-27 LGB
    Weapon.from_pydcs(Weapons.GBU_27): 1991,
    Weapon.from_pydcs(Weapons.GBU_27_2): 1991,
    Weapon.from_pydcs(Weapons.GBU_27_4): 1991,
    
    # GBU-28
    Weapon.from_pydcs(Weapons.GBU_28): 1991,
    
    # GBU-31 JDAM
    Weapon.from_pydcs(Weapons.GBU_31V3B_8): 1997,
    Weapon.from_pydcs(Weapons.GBU_31_8): 1997,
    Weapon.from_pydcs(Weapons.GBU_31_V_1_B): 1997,
    Weapon.from_pydcs(Weapons.GBU_31_V_2_B): 1997,
    Weapon.from_pydcs(Weapons.GBU_31_V_3_B): 1997,
    Weapon.from_pydcs(Weapons.GBU_31_V_4_B): 1997,
    
    # GBU-32 JDAM
    Weapon.from_pydcs(Weapons.GBU_32_V_2_B): 1997,
    
    # GBU-38 JDAM
    Weapon.from_pydcs(Weapons.BRU_55___2_x_GBU_38): 2002,
    Weapon.from_pydcs(Weapons.BRU_57___2_x_GBU_38): 2002,
    Weapon.from_pydcs(Weapons.GBU_38): 2002,
    Weapon.from_pydcs(Weapons.GBU_38_16): 2002,
    Weapon.from_pydcs(Weapons._2_GBU_38): 2002,
    Weapon.from_pydcs(Weapons._2_GBU_38_): 2002,
    Weapon.from_pydcs(Weapons._3_GBU_38): 2002,
    
    # GBU-54 LJDAM
    Weapon.from_pydcs(Weapons.GBU_54_V_1_B): 2008,
    Weapon.from_pydcs(Weapons._2_GBU_54_V_1_B): 2008,
    Weapon.from_pydcs(Weapons._2_GBU_54_V_1_B_): 2008,
    Weapon.from_pydcs(Weapons._3_GBU_54_V_1_B): 2008,
    
    # CBU-52
    Weapon.from_pydcs(Weapons.CBU_52B): 1970,
    
    # CBU-87 CEM
    Weapon.from_pydcs(Weapons.CBU_87): 1986,
    Weapon.from_pydcs(Weapons.TER_9A___2_x_CBU_87): 1986,
    Weapon.from_pydcs(Weapons.TER_9A___2_x_CBU_87_): 1986,
    Weapon.from_pydcs(Weapons.TER_9A___3_x_CBU_87): 1986,
    
    # CBU-97
    Weapon.from_pydcs(Weapons.CBU_97): 1986,
    Weapon.from_pydcs(Weapons.TER_9A___2_x_CBU_97): 1986,
    Weapon.from_pydcs(Weapons.TER_9A___2_x_CBU_97_): 1986,
    Weapon.from_pydcs(Weapons.TER_9A___3_x_CBU_97): 1986,
    
    # CBU-99
    Weapon.from_pydcs(Weapons.BRU_33___2_x_CBU_99): 1968,
    Weapon.from_pydcs(Weapons.CBU_99): 1968,
    
    Weapon.from_pydcs(Weapons.BRU_33___2_x_Mk_20_Rockeye): 1968,
    
    Weapon.from_pydcs(Weapons.DIS_MK_20): 1968,
    Weapon.from_pydcs(Weapons.DIS_MK_20_DUAL_L): 1968,
    Weapon.from_pydcs(Weapons.DIS_MK_20_DUAL_R): 1968,
    
    Weapon.from_pydcs(Weapons.HSAB_9_Mk_20_Rockeye): 1968,
    
    Weapon.from_pydcs(Weapons.MAK79_2_MK_20): 1968,
    Weapon.from_pydcs(Weapons.MAK79_2_MK_20_): 1968,
    
    Weapon.from_pydcs(Weapons.MAK79_MK_20): 1968,
    Weapon.from_pydcs(Weapons.MAK79_MK_20_): 1968,
    
    Weapon.from_pydcs(Weapons.MER_6_Mk_20_Rockeye): 1968,
    
    Weapon.from_pydcs(Weapons.Mk_20): 1968,
    Weapon.from_pydcs(Weapons.Mk_20_): 1968,
    Weapon.from_pydcs(Weapons.Mk_20_18): 1968,
    Weapon.from_pydcs(Weapons.Mk_20_Rockeye__6): 1968,
    
    Weapon.from_pydcs(Weapons._2_MK_20): 1968,
    Weapon.from_pydcs(Weapons._2_MK_20_): 1968,
    Weapon.from_pydcs(Weapons._2_MK_20__): 1968,
    Weapon.from_pydcs(Weapons._2_MK_20___): 1968,
    Weapon.from_pydcs(Weapons._2_MK_20____): 1968,
    Weapon.from_pydcs(Weapons._2_MK_20_____): 1968,
    Weapon.from_pydcs(Weapons._2_Mk_20_Rockeye): 1968,
    Weapon.from_pydcs(Weapons._2_Mk_20_Rockeye_): 1968,
    Weapon.from_pydcs(Weapons._2_Mk_20_Rockeye__): 1968,
    
    Weapon.from_pydcs(Weapons._3_Mk_20_Rockeye): 1968,
    Weapon.from_pydcs(Weapons._3_Mk_20_Rockeye_): 1968,
    
    # CBU-103
    Weapon.from_pydcs(Weapons.BRU_57___2_x_CBU_103): 1997,
    Weapon.from_pydcs(Weapons.CBU_103): 1997,
    
    # CBU-105
    Weapon.from_pydcs(Weapons.BRU_57___2_x_CBU_105): 1997,
    Weapon.from_pydcs(Weapons.CBU_105): 1997,
    
    # APKWS
    Weapon.from_pydcs(Weapons.LAU_131_pod___7_x_2_75__Hydra___Laser_Guided_Rkts_M151___HE_APKWS): 2012,
    Weapon.from_pydcs(Weapons.LAU_131_pod___7_x_2_75__Hydra___Laser_Guided_Rkts_M282___MPP_APKWS): 2012,
    Weapon.from_pydcs(Weapons._3_x_LAU_131_pods___21_x_2_75__Hydra___Laser_Guided_M151___HE_APKWS): 2012,
    Weapon.from_pydcs(Weapons._3_x_LAU_131_pods___21_x_2_75__Hydra___Laser_Guided_M282___MPP_APKWS): 2012,
    
    # Russia
    # 9A1472 Vikhr-1
    Weapon.from_pydcs(Weapons.APU_6___6_9A4172_Vikhr): 1985,
    Weapon.from_pydcs(Weapons.APU_8___8_9A4172_Vikhr): 1985,
    Weapon.from_pydcs(Weapons.APU_8___8_9A4172_Vikhr): 1985,
    
    # KAB-1500
    Weapon.from_pydcs(Weapons.KAB_1500Kr): 1985,
    Weapon.from_pydcs(Weapons.KAB_1500L): 1995,
    Weapon.from_pydcs(Weapons.KAB_1500LG_Pr): 1990,
    
    # KAB-500
    Weapon.from_pydcs(Weapons.KAB_500kr): 1980,
    Weapon.from_pydcs(Weapons.KAB_500L): 1995,
    Weapon.from_pydcs(Weapons.KAB_500S): 2000,
    
    # Kh Series
    Weapon.from_pydcs(Weapons.Kh_22N): 1962,
    Weapon.from_pydcs(Weapons.Kh_23L): 1975,
    
    Weapon.from_pydcs(Weapons.Kh_25ML): 1975,
    Weapon.from_pydcs(Weapons.Kh_25ML_): 1975,
    Weapon.from_pydcs(Weapons.Kh_25ML__): 1975,
    
    Weapon.from_pydcs(Weapons.Kh_25MP): 1975,
    
    Weapon.from_pydcs(Weapons.Kh_25MPU): 1980,
    Weapon.from_pydcs(Weapons.Kh_25MPU_): 1980,
    Weapon.from_pydcs(Weapons.Kh_25MPU__): 1980,
    
    Weapon.from_pydcs(Weapons.Kh_25MR): 1975,
    Weapon.from_pydcs(Weapons.Kh_25MR_): 1975,
    
    Weapon.from_pydcs(Weapons.Kh_28__AS_9_Kyle_): 1973,
    
    Weapon.from_pydcs(Weapons.Kh_29L): 1980,
    Weapon.from_pydcs(Weapons.Kh_29L_): 1980,
    Weapon.from_pydcs(Weapons.Kh_29L__): 1980,
    Weapon.from_pydcs(Weapons.Kh_29T): 1980,
    Weapon.from_pydcs(Weapons.Kh_29T_): 1980,
    Weapon.from_pydcs(Weapons.Kh_29T__): 1980,
    
    Weapon.from_pydcs(Weapons.Kh_31A): 1980,
    Weapon.from_pydcs(Weapons.Kh_31A_): 1980,
    Weapon.from_pydcs(Weapons.Kh_31A__): 1980,
    Weapon.from_pydcs(Weapons.Kh_31P): 1980,
    Weapon.from_pydcs(Weapons.Kh_31P_): 1980,
    Weapon.from_pydcs(Weapons.Kh_31P__): 1980,
    
    Weapon.from_pydcs(Weapons.Kh_35): 2003,
    Weapon.from_pydcs(Weapons.Kh_35_): 2003,
    Weapon.from_pydcs(Weapons.Kh_35_6): 2003,
    
    Weapon.from_pydcs(Weapons.Kh_41): 1984,
    
    Weapon.from_pydcs(Weapons.Kh_58U): 1985,
    Weapon.from_pydcs(Weapons.Kh_58U_): 1985,
    
    Weapon.from_pydcs(Weapons.Kh_59M): 1990,
    
    Weapon.from_pydcs(Weapons.Kh_65): 1992,
    Weapon.from_pydcs(Weapons.Kh_65_6): 1992,
    Weapon.from_pydcs(Weapons.Kh_65_8): 1992,
    
    Weapon.from_pydcs(Weapons.Kh_66_Grom__21__APU_68): 1968,
    
    # ECM
    Weapon.from_pydcs(Weapons.L175V_Khibiny_ECM_pod): 1982,
    
    # R-13
    Weapon.from_pydcs(Weapons.R_13M): 1961,
    Weapon.from_pydcs(Weapons.R_13M1): 1965,
    
    # R-24
    Weapon.from_pydcs(Weapons.R_24R): 1981,
    Weapon.from_pydcs(Weapons.R_24T): 1981,
    
    # R-27
    Weapon.from_pydcs(Weapons.R_27ER): 1983,
    Weapon.from_pydcs(Weapons.R_27ET): 1986,
    Weapon.from_pydcs(Weapons.R_27R): 1983,
    Weapon.from_pydcs(Weapons.R_27T): 1983,
    
    # R-33
    Weapon.from_pydcs(Weapons.R_33): 1981,
    
    # R-3
    Weapon.from_pydcs(Weapons.R_3R): 1961,
    Weapon.from_pydcs(Weapons.R_3S): 1963,
    
    # R-40
    Weapon.from_pydcs(Weapons.R_40R): 1976,
    Weapon.from_pydcs(Weapons.R_40T): 1976,
    
    # R-55
    Weapon.from_pydcs(Weapons.R_55): 1967,
    
    # R-60
    Weapon.from_pydcs(Weapons.R_60): 1973,
    Weapon.from_pydcs(Weapons.R_60_x_2): 1973,
    Weapon.from_pydcs(Weapons.R_60_x_2_): 1973,
    
    Weapon.from_pydcs(Weapons.APU_60_1_R_60M): 1982,
    Weapon.from_pydcs(Weapons.R_60M): 1982,
    Weapon.from_pydcs(Weapons.R_60M_): 1982,
    Weapon.from_pydcs(Weapons.R_60M_2): 1982,
    Weapon.from_pydcs(Weapons.R_60M_2_): 1982,
    Weapon.from_pydcs(Weapons.R_60M_x_2): 1982,
    Weapon.from_pydcs(Weapons.R_60M_x_2_): 1982,
    
    # R-73
    Weapon.from_pydcs(Weapons.R_73): 1984,
    Weapon.from_pydcs(Weapons.R_73_): 1984,
    
    # R-77
    Weapon.from_pydcs(Weapons.R_77): 2002,
    Weapon.from_pydcs(Weapons.R_77_): 2002,
    
    # UK
    # ALARM
    Weapon.from_pydcs(Weapons.ALARM): 1990,
    Weapon.from_pydcs(Weapons.ALARM_2): 1990,
    
    # BL-755
    Weapon.from_pydcs(Weapons.BL755): 1973,
    Weapon.from_pydcs(Weapons.BL_755_2): 1973,
    
    # France
    # BLG-66 Belouga
    Weapon.from_pydcs(Weapons.AUF2_BLG_66_AC_x_2): 1979,
    Weapon.from_pydcs(Weapons.BLG_66_AC_Belouga): 1979,
    Weapon.from_pydcs(Weapons.BLG_66_AC_Belouga_): 1979,
    
    # HOT-3
    Weapon.from_pydcs(Weapons.HOT3): 1998,
    Weapon.from_pydcs(Weapons.HOT3_): 1998,
    
    # Magic 2
    Weapon.from_pydcs(Weapons.Matra_Magic_II): 1986,
    Weapon.from_pydcs(Weapons.R_550_Magic_2): 1986,
    
    # Super 530D
    Weapon.from_pydcs(Weapons.Matra_Super_530D): 1988,
    Weapon.from_pydcs(Weapons.Super_530D): 1988,
    
}
