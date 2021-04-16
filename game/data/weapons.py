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
                f"No introduction year for {self}, assuming always available"
            )
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
            cast(int, weapon_data["weight"]),
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
        pylons = [
            v
            for v in aircraft.__dict__.values()
            if inspect.isclass(v) and v.__name__.startswith("Pylon")
        ]

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
    (Weapons.ADM_141A_TALD, None),
    (Weapons.ADM_141B_TALD, None),
    # AGM-114K Hellfire
    (Weapons.AGM114x2_OH_58, Weapons.M260_HYDRA),  # assuming OH-58 and not MQ-9
    (Weapons.AGM_114K, None),  # Only for RQ-1
    (Weapons.AGM_114K___4, Weapons.LAU_61_pod___19_x_2_75_Hydra__UnGd_Rkts_M151__HE),
    # AGM-119 Penguin
    (Weapons.AGM_119B_Penguin_ASM, Weapons.Mk_82),
    # AGM-122 Sidearm
    (Weapons.AGM_122_Sidearm, Weapons.GBU_12),  # outer pylons harrier
    (Weapons.AGM_122_Sidearm_, Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_),  # internal pylons harrier
    # AGM-154 JSOW
    (Weapons.AGM_154A___JSOW_CEB__CBU_type_, Weapons.GBU_12),
    (Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_, Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb),
    (Weapons.BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_, None),  # doesn't exist on any aircraft yet
    (Weapons.AGM_154B___JSOW_Anti_Armour, Weapons.CBU_105___10_x_CEM__CBU_with_WCMD),
    (Weapons.AGM_154C___JSOW_Unitary_BROACH, Weapons.GBU_12),
    (Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH, Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb),
    # AGM-45 Shrike
    (Weapons.AGM_45A_Shrike_ARM, None),
    (Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_, Weapons.AGM_45A_Shrike_ARM),
    (Weapons.AGM_45B_Shrike_ARM__Imp_, Weapons.AGM_45A_Shrike_ARM),
    # AGM-62 Walleye
    (Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_, Weapons.Mk_84),
    # AGM-65 Maverick
    (
        Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_,
    ),  # Walleye is the predecessor to the maverick
    (Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_, None),
    (Weapons.LAU_117_AGM_65F, Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_),
    (Weapons.LAU_117_AGM_65G, Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_),
    (Weapons.LAU_117_AGM_65H, Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_),
    (Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_, Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_),
    (Weapons.LAU_117_AGM_65L, None),
    (Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_, None),
    (Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__, None),
    (Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_, None),
    (Weapons.LAU_88_AGM_65D_ONE, None),
    (Weapons.LAU_88_with_2_x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_, Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_),
    (Weapons.LAU_88_with_2_x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__, Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__),
    (Weapons.LAU_88_with_3_x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_, Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_),
    (Weapons.LAU_88_AGM_65H, Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_),
    (Weapons.LAU_88_AGM_65H_2_L, Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__),
    (Weapons.LAU_88_AGM_65H_2_R, Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__),
    (Weapons.LAU_88_AGM_65H_3, Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_),
    (Weapons.LAU_88_with_2_x_AGM_65K___Maverick_K__CCD_Imp_ASM_, Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_),
    (Weapons.LAU_88_with_2_x_AGM_65K___Maverick_K__CCD_Imp_ASM__, Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__),
    (Weapons.LAU_88_with_3_x_AGM_65K___Maverick_K__CCD_Imp_ASM_, Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_),
    # AGM-84 Harpoon
    (Weapons.AGM_84A_Harpoon_ASM, Weapons.Mk_82),
    (Weapons._8_x_AGM_84A_Harpoon_ASM, Weapons._27_x_Mk_82___500lb_GP_Bombs_LD),
    (Weapons.AGM_84D_Harpoon_AShM, Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_),
    (Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_, Weapons.LAU_117_AGM_65F),
    (Weapons.AGM_84H_SLAM_ER__Expanded_Response_, Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_),
    # AGM-86 ALCM
    (Weapons.AGM_86C_ALCM, Weapons._27_x_Mk_82___500lb_GP_Bombs_LD),
    (Weapons._8_x_AGM_86C_ALCM, Weapons._27_x_Mk_82___500lb_GP_Bombs_LD),
    (Weapons._6_x_AGM_86C_ALCM_on_MER, Weapons.MER12_with_12_x_Mk_82___500lb_GP_Bombs_LD),
    # AGM-88 HARM
    (Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile, Weapons.LAU_88_AGM_65D_ONE),
    (Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_, Weapons.LAU_88_AGM_65D_ONE),
    # AIM-120 AMRAAM
    (Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM, Weapons.AIM_7MH),
    (Weapons.LAU_115_with_1_x_LAU_127_AIM_120B_AMRAAM___Active_Rdr_AAM, Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar),
    (Weapons.LAU_115_with_1_x_LAU_127_AIM_120B_AMRAAM___Active_Rdr_AAM_, Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar),
    (Weapons.LAU_115_2_LAU_127_AIM_120B, Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar),
    (Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM),
    (Weapons.LAU_115_with_1_x_LAU_127_AIM_120C_5_AMRAAM___Active_Rdr_AAM, Weapons.LAU_115_with_1_x_LAU_127_AIM_120B_AMRAAM___Active_Rdr_AAM),
    (Weapons.LAU_115_with_1_x_LAU_127_AIM_120C_5_AMRAAM___Active_Rdr_AAM_, Weapons.LAU_115_with_1_x_LAU_127_AIM_120B_AMRAAM___Active_Rdr_AAM_),
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
    (Weapons.AIM_7E_Sparrow_Semi_Active_Radar, None),
    (Weapons.AIM_7F_Sparrow_Semi_Active_Radar, Weapons.AIM_7E_Sparrow_Semi_Active_Radar),
    (Weapons.AIM_7F_, None),
    (Weapons.AIM_7M, Weapons.AIM_7F_Sparrow_Semi_Active_Radar),
    (Weapons.AIM_7M_, Weapons.AIM_7F_),
    (Weapons.AIM_7MH, Weapons.AIM_7M),
    (Weapons.AIM_7MH_, Weapons.AIM_7M_),
    (Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar, None),
    (Weapons.LAU_115_with_AIM_7M_Sparrow_Semi_Active_Radar, Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar),
    (Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar, Weapons.LAU_115_with_AIM_7M_Sparrow_Semi_Active_Radar),
    (Weapons.LAU_115C_with_AIM_7E_Sparrow_Semi_Active_Radar, None),
    # AIM-9 Sidewinder
    (Weapons.AIM_9M_Sidewinder_IR_AAM, Weapons.AIM_9P5_Sidewinder_IR_AAM),
    (Weapons.AIM_9P5_Sidewinder_IR_AAM, Weapons.AIM_9P_Sidewinder_IR_AAM),
    (Weapons.AIM_9P_Sidewinder_IR_AAM, Weapons.AIM_9L_Sidewinder_IR_AAM),
    (Weapons.AIM_9X_Sidewinder_IR_AAM, Weapons.AIM_9P_Sidewinder_IR_AAM),
    (Weapons.LAU_105_1_AIM_9L_L, None),
    (Weapons.LAU_105_1_AIM_9L_R, None),
    (Weapons.LAU_105_1_AIM_9M_L, Weapons.LAU_105_1_AIM_9L_L),
    (Weapons.LAU_105_1_AIM_9M_R, Weapons.LAU_105_1_AIM_9L_R),
    (Weapons.LAU_105_2_AIM_9L, None),
    (Weapons.LAU_105_2_AIM_9P5, Weapons.LAU_105_with_2_x_AIM_9P_Sidewinder_IR_AAM),
    (Weapons.LAU_105_with_2_x_AIM_9M_Sidewinder_IR_AAM, Weapons.LAU_105_2_AIM_9L),
    (
        Weapons.LAU_105_with_2_x_AIM_9P_Sidewinder_IR_AAM,
        Weapons.LAU_105_with_2_x_AIM_9M_Sidewinder_IR_AAM,
    ),
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
    (Weapons.LAU_7_with_AIM_9M_Sidewinder_IR_AAM, Weapons.LAU_7_with_AIM_9P5_Sidewinder_IR_AAM),
    (Weapons.LAU_7_with_AIM_9P5_Sidewinder_IR_AAM, Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM),
    (Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM, Weapons.LAU_7_AIM_9L),
    (Weapons.LAU_7_with_AIM_9X_Sidewinder_IR_AAM, Weapons.LAU_7_with_AIM_9M_Sidewinder_IR_AAM),
    (
        Weapons.LAU_7_with_2_x_AIM_9M_Sidewinder_IR_AAM,
        Weapons.LAU_7_with_2_x_AIM_9P5_Sidewinder_IR_AAM,
    ),
    (
        Weapons.LAU_7_with_2_x_AIM_9P5_Sidewinder_IR_AAM,
        Weapons.LAU_7_with_2_x_AIM_9P_Sidewinder_IR_AAM,
    ),
    (
        Weapons.LAU_7_with_2_x_AIM_9P_Sidewinder_IR_AAM,
        Weapons.LAU_7_with_2_x_AIM_9L_Sidewinder_IR_AAM,
    ),
    # ALQ ECM Pods
    (Weapons.ALQ_131___ECM_Pod, None),
    (Weapons.ALQ_184, Weapons.ALQ_131___ECM_Pod),
    (Weapons.AN_ALQ_164_DECM_Pod, None),
    # TGP Pods
    (Weapons.AN_AAQ_28_LITENING___Targeting_Pod_, None),
    (Weapons.AN_AAQ_28_LITENING___Targeting_Pod, Weapons.Lantirn_F_16),
    (Weapons.AN_ASQ_228_ATFLIR___Targeting_Pod, None),
    (Weapons.AN_ASQ_173_Laser_Spot_Tracker_Strike_CAMera__LST_SCAM_, None),
    (Weapons.AWW_13_DATALINK_POD, None),
    (Weapons.LANTIRN_Targeting_Pod, None),
    (Weapons.Lantirn_F_16, None),
    (Weapons.Lantirn_Target_Pod, None),
    (Weapons.Pavetack_F_111, None),
    # BLU-107
    (Weapons.BLU_107___440lb_Anti_Runway_Penetrator_Bomb, None),
    (Weapons.MER6_with_6_x_BLU_107___440lb_Anti_Runway_Penetrator_Bombs, Weapons.MER6_with_6_x_Mk_82___500lb_GP_Bombs_LD),
    # GBU-10 LGB
    (Weapons.DIS_GBU_10, Weapons.Mk_84),
    (Weapons.GBU_10, Weapons.Mk_84),
    (Weapons.BRU_42_with_2_x_GBU_10___2000lb_Laser_Guided_Bombs, Weapons.Mk_84),
    (Weapons.DIS_GBU_10, Weapons.Mk_84),
    # GBU-12 LGB
    (Weapons.AUF2_GBU_12_x_2, None),
    (Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb, Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD),
    (Weapons.BRU_42_3_GBU_12, Weapons._3_Mk_82),
    (Weapons.DIS_GBU_12, Weapons.Mk_82),
    (Weapons.DIS_GBU_12_DUAL_GDJ_II19_L, Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD),
    (Weapons.DIS_GBU_12_DUAL_GDJ_II19_R, Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD),
    (Weapons.GBU_12, Weapons.Mk_82),
    (Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb, Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD),
    (Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_, Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_),
    (Weapons._2_GBU_12, Weapons._2_Mk_82),
    (Weapons._2_GBU_12_, Weapons._2_Mk_82_),
    # GBU-16 LGB
    (Weapons.BRU_33_with_2_x_GBU_16___1000lb_Laser_Guided_Bomb, None),
    (Weapons.DIS_GBU_16, Weapons.Mk_83),
    (Weapons.GBU_16, Weapons.Mk_83),
    (Weapons.BRU_42_with_3_x_GBU_16___1000lb_Laser_Guided_Bombs, None),
    # GBU-24 LGB
    (Weapons.GBU_24, Weapons.GBU_10),
    (Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb, Weapons.GBU_16___1000lb_Laser_Guided_Bomb),
    (Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_, Weapons.GBU_10___2000lb_Laser_Guided_Bomb),
    # GBU-27 LGB
    (Weapons.GBU_27___2000lb_Laser_Guided_Penetrator_Bomb, Weapons.GBU_16___1000lb_Laser_Guided_Bomb),
    # GBU-28 LGB
    (Weapons.GBU_28___5000lb_Laser_Guided_Penetrator_Bomb, None),
    # GBU-31 JDAM
    (Weapons.GBU_31V3B_8, Weapons.B_1B_Mk_84_8),
    (Weapons.GBU_31_8, Weapons.B_1B_Mk_84_8),
    (Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb, Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb),
    (Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb, Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb),
    (Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb, Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb),
    (Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb, Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb),
    # GBU-32 JDAM
    (Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb, Weapons.GBU_16),
    # GBU-32 JDAM
    (Weapons.BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb, Weapons.BRU_33_with_2_x_Mk_82___500lb_GP_Bomb_LD),
    (Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb, None),  # Doesn't exist
    (Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb, Weapons.Mk_82),
    (Weapons.GBU_38_16, Weapons.MK_82_28),
    (Weapons._2_GBU_38, Weapons._2_Mk_82),
    (Weapons._2_GBU_38_, Weapons._2_Mk_82_),
    (Weapons._3_GBU_38, Weapons._3_Mk_82),
    # GBU-54 LJDAM
    (Weapons.GBU_54B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD, Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb),
    (Weapons._2_GBU_54_V_1_B, Weapons._2_GBU_38),
    (Weapons._2_GBU_54_V_1_B_, Weapons._2_GBU_38_),
    (Weapons._3_GBU_54_V_1_B, Weapons._3_GBU_38),
    # CBU-52
    (Weapons.CBU_52B___220_x_HE_Frag_bomblets, None),
    # CBU-87 CEM
    (Weapons.CBU_87___202_x_CEM_Cluster_Bomb, Weapons.Mk_82),
    (Weapons.TER_9A_with_2_x_CBU_87___202_x_Anti_Armor_Skeet_SFW_Cluster_Bomb, Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD),
    (Weapons.TER_9A_with_2_x_CBU_87___202_x_Anti_Armor_Skeet_SFW_Cluster_Bomb_, Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD),
    (Weapons.TER_9A_with_3_x_CBU_87___202_x_Anti_Armor_Skeet_SFW_Cluster_Bomb, Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD),
    # CBU-97
    (Weapons.CBU_97___10_x_CEM_Cluster_Bomb, Weapons.Mk_82),
    (Weapons.TER_9A_with_2_x_CBU_97___10_x_Anti_Armor_Skeet_SFW_Cluster_Bomb, Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD),
    (Weapons.TER_9A_with_2_x_CBU_97___10_x_Anti_Armor_Skeet_SFW_Cluster_Bomb_, Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_),
    (Weapons.TER_9A_with_3_x_CBU_97___10_x_Anti_Armor_Skeet_SFW_Cluster_Bomb, Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD),
    # CBU-99 (It's a bomb made in 1968, I'm not bothering right now with backups)
    # CBU-103
    (Weapons.CBU_103___202_x_CEM__CBU_with_WCMD, Weapons.CBU_87___202_x_CEM_Cluster_Bomb),
    # CBU-105
    (Weapons.CBU_105___10_x_CEM__CBU_with_WCMD, Weapons.CBU_97___10_x_CEM_Cluster_Bomb),
    (
        Weapons.LAU_131_pod___7_x_2_75_Hydra__Laser_Guided_Rkts_M151__HE_APKWS,
        Weapons.LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
    ),
    (
        Weapons.LAU_131_pod___7_x_2_75_Hydra__Laser_Guided_Rkts_M282__MPP_APKWS,
        Weapons.LAU_131_pod___7_x_2_75_Hydra__UnGd_Rkts_M151__HE,
    ),
    (
        Weapons.BRU_42_with_3_x_LAU_131_pods___7_x_2_75_Hydra__Laser_Guided_Rkts_M151__HE_APKWS,
        Weapons.BRU_42_with_3_x_LAU_68_pods___21_x_2_75_Hydra__UnGd_Rkts_M151__HE,
    ),
    (
        Weapons.BRU_42_with_3_x_LAU_131_pods___7_x_2_75_Hydra__Laser_Guided_Rkts_M282__MPP_APKWS,
        Weapons.BRU_42_with_3_x_LAU_68_pods___21_x_2_75_Hydra__UnGd_Rkts_M151__HE,
    ),
    # Russia
    # KAB-1500
    (Weapons.KAB_1500Kr___1500kg_TV_Guided_Bomb, None),
    (Weapons.KAB_1500LG_Pr___1500kg_Laser_Guided_Penetrator_Bomb, Weapons.KAB_1500Kr___1500kg_TV_Guided_Bomb),
    (Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb, Weapons.KAB_1500LG_Pr___1500kg_Laser_Guided_Penetrator_Bomb),
    # KAB-500
    (Weapons.KAB_500Kr___500kg_TV_Guided_Bomb, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD),
    (Weapons.KAB_500LG___500kg_Laser_Guided_Bomb, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb),
    (Weapons.KAB_500S___500kg_GPS_Guided_Bomb, Weapons.KAB_500LG___500kg_Laser_Guided_Bomb),
    # KH Series
    (Weapons.Kh_22__AS_4_Kitchen____1000kg__AShM__IN__Act_Pas_Rdr, None),
    (Weapons.Kh_23L_Grom__AS_7_Kerry____286kg__ASM__Laser_Guided, None),
    (Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser, None),
    (Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_, None),
    (Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser__, None),
    (Weapons.Kh_25MP__AS_12_Kegler____320kg__ARM__Pas_Rdr, None),
    (Weapons.Kh_25MPU__Updated_AS_12_Kegler____320kg__ARM__IN__Pas_Rdr, Weapons.Kh_25MP__AS_12_Kegler____320kg__ARM__Pas_Rdr),
    (Weapons.Kh_25MR__AS_10_Karen____300kg__ASM__10km__RC_Guided, None),
    (Weapons.Kh_25MR__AS_10_Karen____300kg__ASM__RC_Guided, None),
    (Weapons.Kh_28__AS_9_Kyle____720kg__ARM__Pas_Rdr, None),
    (Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser, Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser),
    (Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser_, Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_),
    (Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser__, Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser__),
    (Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided, Weapons.Kh_25MR__AS_10_Karen____300kg__ASM__10km__RC_Guided),
    (Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_, Weapons.Kh_25MR__AS_10_Karen____300kg__ASM__RC_Guided),
    (Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_, Weapons.Kh_25MR__AS_10_Karen____300kg__ASM__RC_Guided),
    (Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr, None),
    (Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr_, None),
    (Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr__, None),
    (Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr, Weapons.Kh_25MP__AS_12_Kegler____320kg__ARM__Pas_Rdr),
    (Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr_, Weapons.Kh_25MP__AS_12_Kegler____320kg__ARM__Pas_Rdr),
    (Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr__, Weapons.Kh_25MP__AS_12_Kegler____320kg__ARM__Pas_Rdr),
    (Weapons.Kh_35__AS_20_Kayak____520kg__AShM__IN__Act_Rdr, Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr),
    (Weapons.Kh_35__AS_20_Kayak____520kg__AShM__IN__Act_Rdr_, Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr_),
    (Weapons._6_x_Kh_35__AS_20_Kayak____520kg__AShM__IN__Act_Rdr, None),
    (Weapons.Kh_41__SS_N_22_Sunburn____4500kg__AShM__IN__Act_Rdr, None),
    (Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr, Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr),
    (Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_, Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr_),
    (Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN, Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr),
    (Weapons.Kh_65__AS_15B_Kent____1250kg__ASM__IN__MCC, None),
    (Weapons._6_x_Kh_65__AS_15B_Kent____1250kg__ASM__IN__MCC, None),
    (Weapons._8_x_Kh_65__AS_15B_Kent____1250kg__ASM__IN__MCC, None),
    (Weapons.Kh_66_Grom__21__APU_68, None),
    # ECM
    (Weapons.L175V_Khibiny_ECM_pod, None),
    # R-13
    (Weapons.R_13M, None),
    (Weapons.R_13M1, Weapons.R_13M),
    # R-24
    (Weapons.R_24R__AA_7_Apex_SA____Semi_Act_Rdr, None),
    (Weapons.R_24T__AA_7_Apex_IR____Infra_Red, None),
    # R-27
    (Weapons.R_27T__AA_10_Alamo_B____Infra_Red, Weapons.R_24T__AA_7_Apex_IR____Infra_Red),
    (Weapons.R_27R__AA_10_Alamo_A____Semi_Act_Rdr, Weapons.R_24R__AA_7_Apex_SA____Semi_Act_Rdr),
    (Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range, Weapons.R_27R__AA_10_Alamo_A____Semi_Act_Rdr),
    (Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range, Weapons.R_27T__AA_10_Alamo_B____Infra_Red),
    # R-33
    (Weapons.R_33__AA_9_Amos____Semi_Act_Rdr, None),
    # R-3
    (Weapons.R_3S, Weapons.R_13M),
    (Weapons.R_3R, Weapons.R_3S),
    # R-40
    (Weapons.R_40R__AA_6_Acrid____Semi_Act_Rdr, None),
    (Weapons.R_40T__AA_6_Acrid____Infra_Red, None),
    # R-55
    (Weapons.R_55, None),
    (Weapons.RS2US, None),
    # R-60
    (Weapons.R_60, Weapons.R_13M1),
    (Weapons.R_60_x_2, Weapons.R_13M1),
    (Weapons.R_60_x_2_, Weapons.R_13M1),
    (Weapons.R_60M, Weapons.R_60),
    (Weapons.APU_60_1M_with_R_60M__AA_8_Aphid____Infra_Red, Weapons.R_60),
    (Weapons.APU_60_2M_with_2_x_R_60M__AA_8_Aphid____Infra_Red, Weapons.R_60M),
    (Weapons.APU_60_2M_with_2_x_R_60M__AA_8_Aphid____Infra_Red_, Weapons.R_60M),
    (Weapons.R_60M_x_2, Weapons.R_60M),
    (Weapons.R_60M_x_2_, Weapons.R_60M),
    # R-73
    (Weapons.R_73__AA_11_Archer____Infra_Red, Weapons.R_60M),
    (Weapons.R_73__AA_11_Archer____Infra_Red_, None),
    # R-77
    (Weapons.R_77__AA_12_Adder____Active_Rdr, Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range),
    (Weapons.R_77__AA_12_Adder____Active_Rdr_, None),
    # UK
    # ALARM
    (Weapons.ALARM, None),
    # France
    # BLG-66 Belouga
    (Weapons.AUF2_BLG_66_AC_x_2, Weapons.AUF2_MK_82_x_2),
    (Weapons.BLG_66_AC_Belouga, Weapons.Mk_82),
    (Weapons.BLG_66_Belouga___290kg_CBU__151_Frag_Pen_bomblets, Weapons.Mk_82),
    # HOT-3
    (Weapons.HOT3, None),
    (Weapons.HOT3_, None),
    # Magic 2
    (Weapons.Matra_Magic_II, None),
    (Weapons.R_550_Magic_2, None),
    # Super 530D
    (Weapons.Matra_Super_530D, Weapons.Matra_Magic_II),
    (Weapons.Super_530D, None),
]

WEAPON_FALLBACK_MAP: Dict[Weapon, Optional[Weapon]] = defaultdict(
    lambda: cast(Optional[Weapon], None),
    (
        (Weapon.from_pydcs(a), b if b is None else Weapon.from_pydcs(b))
        for a, b in _WEAPON_FALLBACKS
    ),
)


WEAPON_INTRODUCTION_YEARS = {
    # USA
    # ADM-141 TALD
    Weapon.from_pydcs(Weapons.ADM_141A): 1987,
    Weapon.from_pydcs(Weapons.ADM_141A_): 1987,
    Weapon.from_pydcs(Weapons.ADM_141A_TALD): 1987,
    Weapon.from_pydcs(Weapons.ADM_141B_TALD): 1987,
    # AGM-114K Hellfire
    Weapon.from_pydcs(Weapons.AGM114x2_OH_58): 1993,
    Weapon.from_pydcs(Weapons.AGM_114K): 1993,
    Weapon.from_pydcs(Weapons.AGM_114K___4): 1993,
    # AGM-119 Penguin
    Weapon.from_pydcs(Weapons.AGM_119B_Penguin_ASM): 1972,
    # AGM-122 Sidearm
    Weapon.from_pydcs(Weapons.AGM_122_Sidearm___light_ARM): 1986,
    Weapon.from_pydcs(Weapons.AGM_122_Sidearm): 1986,
    Weapon.from_pydcs(Weapons.AGM_122_Sidearm_): 1986,
    # AGM-154 JSOW
    Weapon.from_pydcs(Weapons.AGM_154A___JSOW_CEB__CBU_type_): 1998,
    Weapon.from_pydcs(Weapons.BRU_55_with_2_x_AGM_154A___JSOW_CEB__CBU_type_): 1998,
    Weapon.from_pydcs(Weapons.BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_): 1998,
    Weapon.from_pydcs(Weapons.AGM_154B___JSOW_Anti_Armour): 2005,
    Weapon.from_pydcs(Weapons.AGM_154C___JSOW_Unitary_BROACH): 2005,
    Weapon.from_pydcs(Weapons._4_x_AGM_154C___JSOW_Unitary_BROACH): 2005,
    Weapon.from_pydcs(Weapons.BRU_55_with_2_x_AGM_154C___JSOW_Unitary_BROACH): 2005,
    # AGM-45 Shrike
    Weapon.from_pydcs(Weapons.AGM_45A_Shrike_ARM): 1965,
    Weapon.from_pydcs(Weapons.AGM_45B_Shrike_ARM__Imp_): 1970,
    Weapon.from_pydcs(Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_): 1970,
    # AGM-62 Walleye
    Weapon.from_pydcs(Weapons.AGM_62_Walleye_II___Guided_Weapon_Mk_5__TV_Guided_): 1972,
    # AGM-65 Maverick
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65D_ONE): 1983,
    Weapon.from_pydcs(Weapons.AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_): 1985,
    Weapon.from_pydcs(Weapons.AGM_65K___Maverick_K__CCD_Imp_ASM_): 2007,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65A): 1972,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65B): 1972,
    Weapon.from_pydcs(Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_): 1986,
    Weapon.from_pydcs(Weapons.LAU_117_with_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_): 1990,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65F): 1991,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65G): 1989,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65H): 2002,
    Weapon.from_pydcs(Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_): 2002,
    Weapon.from_pydcs(Weapons.LAU_117_AGM_65L): 1985,
    Weapon.from_pydcs(Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_): 1983,
    Weapon.from_pydcs(Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__): 1983,
    Weapon.from_pydcs(Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_): 1983,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65D_ONE): 1983,
    Weapon.from_pydcs(Weapons.LAU_88_with_2_x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_): 1985,
    Weapon.from_pydcs(Weapons.LAU_88_with_2_x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd__): 1985,
    Weapon.from_pydcs(Weapons.LAU_88_with_3_x_AGM_65E___Maverick_E__Laser_ASM___Lg_Whd_): 1985,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65H): 2007,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65H_2_L): 2007,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65H_2_R): 2007,
    Weapon.from_pydcs(Weapons.LAU_88_AGM_65H_3): 2007,
    Weapon.from_pydcs(Weapons.LAU_88_with_2_x_AGM_65K___Maverick_K__CCD_Imp_ASM_): 2007,
    Weapon.from_pydcs(Weapons.LAU_88_with_2_x_AGM_65K___Maverick_K__CCD_Imp_ASM__): 2007,
    Weapon.from_pydcs(Weapons.LAU_88_with_3_x_AGM_65K___Maverick_K__CCD_Imp_ASM_): 2007,
    # AGM-84 Harpoon
    Weapon.from_pydcs(Weapons.AGM_84): 1979,
    Weapon.from_pydcs(Weapons.AGM_84A_Harpoon_ASM): 1979,
    Weapon.from_pydcs(Weapons._8_x_AGM_84A_Harpoon_ASM): 1979,
    Weapon.from_pydcs(Weapons.AGM_84D_Harpoon_AShM): 1979,
    Weapon.from_pydcs(Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile_): 1990,
    Weapon.from_pydcs(Weapons.AGM_84E_Harpoon_SLAM__Stand_Off_Land_Attack_Missile__): 1990,
    Weapon.from_pydcs(Weapons.AGM_84H_SLAM_ER__Expanded_Response_): 1998,
    # AGM-86 ALCM
    Weapon.from_pydcs(Weapons.AGM_86C_ALCM): 1986,
    Weapon.from_pydcs(Weapons._20_x_AGM_86C_ALCM): 1986,
    Weapon.from_pydcs(Weapons._8_x_AGM_86C_ALCM): 1986,
    Weapon.from_pydcs(Weapons._6_x_AGM_86C_ALCM_on_MER): 1986,
    # AGM-88 HARM
    Weapon.from_pydcs(Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile): 1983,
    Weapon.from_pydcs(Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_): 1983,
    # for future reference: 1983 is the A model IOC. B model in 1986 and C model in 1994.
    # AIM-120 AMRAAM
    Weapon.from_pydcs(Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM): 1994,
    Weapon.from_pydcs(Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM): 1996,
    Weapon.from_pydcs(Weapons.LAU_115_2_LAU_127_AIM_120B): 1994,
    Weapon.from_pydcs(Weapons.LAU_115_with_1_x_LAU_127_AIM_120B_AMRAAM___Active_Rdr_AAM): 1994,
    Weapon.from_pydcs(Weapons.LAU_115_2_LAU_127_AIM_120C): 1996,
    Weapon.from_pydcs(Weapons.LAU_115_with_1_x_LAU_127_AIM_120C_5_AMRAAM___Active_Rdr_AAM): 1996,
    # AIM-54 Phoenix
    Weapon.from_pydcs(Weapons.AIM_54A_Mk47): 1974,
    Weapon.from_pydcs(Weapons.AIM_54A_Mk47_): 1974,
    Weapon.from_pydcs(Weapons.AIM_54A_Mk47__): 1974,
    Weapon.from_pydcs(Weapons.AIM_54A_Mk60): 1974,
    Weapon.from_pydcs(Weapons.AIM_54A_Mk60_): 1974,
    Weapon.from_pydcs(Weapons.AIM_54A_Mk60__): 1974,
    Weapon.from_pydcs(Weapons.AIM_54C_Mk47_Phoenix_IN__Semi_Active_Radar): 1974,
    Weapon.from_pydcs(Weapons.AIM_54C_Mk47): 1974,
    Weapon.from_pydcs(Weapons.AIM_54C_Mk47_): 1974,
    Weapon.from_pydcs(Weapons.AIM_54C_Mk47__): 1974,
    # AIM-7 Sparrow
    Weapon.from_pydcs(Weapons.AIM_7E_Sparrow_Semi_Active_Radar): 1963,
    Weapon.from_pydcs(Weapons.AIM_7F_Sparrow_Semi_Active_Radar): 1976,
    Weapon.from_pydcs(Weapons.AIM_7F_): 1976,
    Weapon.from_pydcs(Weapons.AIM_7F): 1976,
    Weapon.from_pydcs(Weapons.AIM_7M): 1982,
    Weapon.from_pydcs(Weapons.AIM_7M_): 1982,
    Weapon.from_pydcs(Weapons.LAU_115_with_AIM_7M_Sparrow_Semi_Active_Radar): 1982,
    Weapon.from_pydcs(Weapons.AIM_7MH): 1987,
    Weapon.from_pydcs(Weapons.AIM_7MH_): 1987,
    Weapon.from_pydcs(Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar): 1987,
    Weapon.from_pydcs(Weapons.LAU_115C_with_AIM_7E_Sparrow_Semi_Active_Radar): 1963,
    Weapon.from_pydcs(Weapons.LAU_115C_with_AIM_7F_Sparrow_Semi_Active_Radar): 1976,
    Weapon.from_pydcs(Weapons.LAU_115C_with_AIM_7MH_Sparrow_Semi_Active_Radar): 1987,
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
    Weapon.from_pydcs(Weapons.LAU_105_with_2_x_AIM_9M_Sidewinder_IR_AAM): 1982,
    Weapon.from_pydcs(Weapons.LAU_105_with_2_x_AIM_9P_Sidewinder_IR_AAM): 1978,
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
    Weapon.from_pydcs(Weapons.LAU_7_with_AIM_9M_Sidewinder_IR_AAM): 1982,
    Weapon.from_pydcs(Weapons.LAU_7_with_AIM_9P5_Sidewinder_IR_AAM): 1980,
    Weapon.from_pydcs(Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM): 1978,
    Weapon.from_pydcs(Weapons.LAU_7_with_AIM_9X_Sidewinder_IR_AAM): 2003,
    Weapon.from_pydcs(Weapons.LAU_7_with_2_x_AIM_9L_Sidewinder_IR_AAM): 1977,
    Weapon.from_pydcs(Weapons.LAU_7_with_2_x_AIM_9M_Sidewinder_IR_AAM): 1982,
    Weapon.from_pydcs(Weapons.LAU_7_with_2_x_AIM_9P5_Sidewinder_IR_AAM): 1980,
    Weapon.from_pydcs(Weapons.LAU_7_with_2_x_AIM_9P_Sidewinder_IR_AAM): 1978,
    # ALQ ECM Pods
    Weapon.from_pydcs(Weapons.ALQ_131___ECM_Pod): 1970,
    Weapon.from_pydcs(Weapons.ALQ_184): 1989,
    Weapon.from_pydcs(Weapons.AN_ALQ_164_DECM_Pod): 1984,
    # TGP Pods
    Weapon.from_pydcs(Weapons.AN_AAQ_28_LITENING___Targeting_Pod): 1995,
    Weapon.from_pydcs(Weapons.AN_AAQ_28_LITENING___Targeting_Pod_): 1995,
    Weapon.from_pydcs(Weapons.AN_ASQ_228_ATFLIR___Targeting_Pod): 1993,
    Weapon.from_pydcs(Weapons.AN_ASQ_173_Laser_Spot_Tracker_Strike_CAMera__LST_SCAM_): 1993,
    Weapon.from_pydcs(Weapons.AWW_13_DATALINK_POD): 1967,
    Weapon.from_pydcs(Weapons.LANTIRN_Targeting_Pod): 1985,
    Weapon.from_pydcs(Weapons.Lantirn_F_16): 1985,
    Weapon.from_pydcs(Weapons.Lantirn_Target_Pod): 1985,
    Weapon.from_pydcs(Weapons.Pavetack_F_111): 1982,
    # BLU-107
    Weapon.from_pydcs(Weapons.BLU_107___440lb_Anti_Runway_Penetrator_Bomb): 1983,
    Weapon.from_pydcs(Weapons.MER6_with_6_x_BLU_107___440lb_Anti_Runway_Penetrator_Bombs): 1983,
    # GBU-10 LGB
    Weapon.from_pydcs(Weapons.DIS_GBU_10): 1976,
    Weapon.from_pydcs(Weapons.GBU_10): 1976,
    Weapon.from_pydcs(Weapons.BRU_42_with_2_x_GBU_10___2000lb_Laser_Guided_Bombs): 1976,
    Weapon.from_pydcs(Weapons.GBU_10___2000lb_Laser_Guided_Bomb): 1976,
    # GBU-12 LGB
    Weapon.from_pydcs(Weapons.AUF2_GBU_12_x_2): 1976,
    Weapon.from_pydcs(Weapons.BRU_33_with_2_x_GBU_12___500lb_Laser_Guided_Bomb): 1976,
    Weapon.from_pydcs(Weapons.BRU_42_3_GBU_12): 1976,
    Weapon.from_pydcs(Weapons.DIS_GBU_12): 1976,
    Weapon.from_pydcs(Weapons.DIS_GBU_12_DUAL_GDJ_II19_L): 1976,
    Weapon.from_pydcs(Weapons.DIS_GBU_12_DUAL_GDJ_II19_R): 1976,
    Weapon.from_pydcs(Weapons.GBU_12): 1976,
    Weapon.from_pydcs(Weapons.GBU_12): 1976,
    Weapon.from_pydcs(Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb): 1976,
    Weapon.from_pydcs(Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_): 1976,
    Weapon.from_pydcs(Weapons._2_GBU_12): 1976,
    Weapon.from_pydcs(Weapons._2_GBU_12_): 1976,
    Weapon.from_pydcs(Weapons._3_GBU_12): 1976,
    # GBU-16 LGB
    Weapon.from_pydcs(Weapons.BRU_33_with_2_x_GBU_16___1000lb_Laser_Guided_Bomb): 1976,
    Weapon.from_pydcs(Weapons.DIS_GBU_16): 1976,
    Weapon.from_pydcs(Weapons.GBU_16): 1976,
    Weapon.from_pydcs(Weapons.GBU_16___1000lb_Laser_Guided_Bomb): 1976,
    Weapon.from_pydcs(Weapons._2_GBU_16): 1976,
    Weapon.from_pydcs(Weapons._2_GBU_16_): 1976,
    Weapon.from_pydcs(Weapons._3_GBU_16): 1976,
    Weapon.from_pydcs(Weapons.BRU_42_with_3_x_GBU_16___1000lb_Laser_Guided_Bombs): 1976,
    # GBU-24 LGB
    Weapon.from_pydcs(Weapons.GBU_24): 1986,
    Weapon.from_pydcs(Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb): 1986,
    Weapon.from_pydcs(Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_): 1986,
    # GBU-27 LGB
    Weapon.from_pydcs(Weapons.GBU_27___2000lb_Laser_Guided_Penetrator_Bomb): 1991,
    Weapon.from_pydcs(Weapons.BRU_42_with_2_x_GBU_27___2000lb_Laser_Guided_Penetrator_Bombs): 1991,
    # GBU-28
    Weapon.from_pydcs(Weapons.GBU_28___5000lb_Laser_Guided_Penetrator_Bomb): 1991,
    # GBU-31 JDAM
    Weapon.from_pydcs(Weapons.GBU_31V3B_8): 2001,
    Weapon.from_pydcs(Weapons.GBU_31_8): 2001,
    Weapon.from_pydcs(Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb): 2001,
    Weapon.from_pydcs(Weapons.GBU_31_V_2_B___JDAM__2000lb_GPS_Guided_Bomb): 2001,
    Weapon.from_pydcs(Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb): 2001,
    Weapon.from_pydcs(Weapons.GBU_31_V_4_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb): 2001,
    # GBU-32 JDAM
    Weapon.from_pydcs(Weapons.GBU_32_V_2_B___JDAM__1000lb_GPS_Guided_Bomb): 2002,
    # GBU-38 JDAM
    Weapon.from_pydcs(Weapons.BRU_55_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb): 2005,
    Weapon.from_pydcs(Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb): 2005,
    Weapon.from_pydcs(Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb): 2005,
    Weapon.from_pydcs(Weapons.GBU_38_16): 2005,
    Weapon.from_pydcs(Weapons._2_GBU_38): 2005,
    Weapon.from_pydcs(Weapons._2_GBU_38_): 2005,
    Weapon.from_pydcs(Weapons._3_GBU_38): 2005,
    # GBU-54 LJDAM
    Weapon.from_pydcs(Weapons.GBU_54B___LJDAM__500lb_Laser__GPS_Guided_Bomb_LD): 2008,
    Weapon.from_pydcs(Weapons._2_GBU_54_V_1_B): 2008,
    Weapon.from_pydcs(Weapons._2_GBU_54_V_1_B_): 2008,
    Weapon.from_pydcs(Weapons._3_GBU_54_V_1_B): 2008,
    # CBU-52
    Weapon.from_pydcs(Weapons.CBU_52B___220_x_HE_Frag_bomblets): 1970,
    # CBU-87 CEM
    Weapon.from_pydcs(Weapons.CBU_87___202_x_CEM_Cluster_Bomb): 1986,
    Weapon.from_pydcs(Weapons.TER_9A_with_2_x_CBU_87___202_x_Anti_Armor_Skeet_SFW_Cluster_Bomb): 1986,
    Weapon.from_pydcs(Weapons.TER_9A_with_2_x_CBU_87___202_x_Anti_Armor_Skeet_SFW_Cluster_Bomb_): 1986,
    Weapon.from_pydcs(Weapons.TER_9A_with_3_x_CBU_87___202_x_Anti_Armor_Skeet_SFW_Cluster_Bomb): 1986,
    # CBU-97
    Weapon.from_pydcs(Weapons.CBU_97___10_x_CEM_Cluster_Bomb): 1992,
    Weapon.from_pydcs(Weapons.TER_9A_with_2_x_CBU_97___10_x_Anti_Armor_Skeet_SFW_Cluster_Bomb): 1992,
    Weapon.from_pydcs(Weapons.TER_9A_with_2_x_CBU_97___10_x_Anti_Armor_Skeet_SFW_Cluster_Bomb_): 1992,
    Weapon.from_pydcs(Weapons.TER_9A_with_3_x_CBU_97___10_x_Anti_Armor_Skeet_SFW_Cluster_Bomb): 1992,
    # CBU-99
    Weapon.from_pydcs(Weapons.BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets): 1968,
    Weapon.from_pydcs(Weapons.BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets): 1968,
    Weapon.from_pydcs(Weapons.BRU_33_with_2_x_CBU_99___490lbs__247_x_HEAT_Bomblets): 1968,
    Weapon.from_pydcs(Weapons.DIS_MK_20): 1968,
    Weapon.from_pydcs(Weapons.DIS_MK_20_DUAL_GDJ_II19_L): 1968,
    Weapon.from_pydcs(Weapons.DIS_MK_20_DUAL_GDJ_II19_R): 1968,
    Weapon.from_pydcs(Weapons.HSAB_with_9_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets): 1968,
    Weapon.from_pydcs(Weapons.MAK79_2_MK_20): 1968,
    Weapon.from_pydcs(Weapons.MAK79_2_MK_20_): 1968,
    Weapon.from_pydcs(Weapons.MAK79_MK_20): 1968,
    Weapon.from_pydcs(Weapons.MAK79_MK_20_): 1968,
    Weapon.from_pydcs(Weapons.MER6_with_6_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets): 1968,
    Weapon.from_pydcs(Weapons.Mk_20): 1968,
    Weapon.from_pydcs(Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets): 1968,
    Weapon.from_pydcs(Weapons.Mk_20_18): 1968,
    Weapon.from_pydcs(Weapons._6_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets): 1968,
    Weapon.from_pydcs(Weapons._2_MK_20): 1968,
    Weapon.from_pydcs(Weapons._2_MK_20_): 1968,
    Weapon.from_pydcs(Weapons._2_MK_20__): 1968,
    Weapon.from_pydcs(Weapons._2_MK_20___): 1968,
    Weapon.from_pydcs(Weapons._2_MK_20____): 1968,
    Weapon.from_pydcs(Weapons._2_MK_20_____): 1968,
    Weapon.from_pydcs(Weapons._2_Mk_20_Rockeye): 1968,
    Weapon.from_pydcs(Weapons._2_Mk_20_Rockeye_): 1968,
    Weapon.from_pydcs(Weapons.MER2_with_2_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets): 1968,
    # CBU-103
    Weapon.from_pydcs(Weapons.BRU_57_with_2_x_CBU_103): 2000,
    Weapon.from_pydcs(Weapons.CBU_103___202_x_CEM__CBU_with_WCMD): 2000,
    # CBU-105
    Weapon.from_pydcs(Weapons.BRU_57_with_2_x_CBU_105): 2000,
    Weapon.from_pydcs(Weapons.CBU_105___10_x_CEM__CBU_with_WCMD): 2000,
    # APKWS
    Weapon.from_pydcs(
        Weapons.LAU_131_pod___7_x_2_75_Hydra__Laser_Guided_Rkts_M151__HE_APKWS
    ): 2016,
    Weapon.from_pydcs(
        Weapons.LAU_131_pod___7_x_2_75_Hydra__Laser_Guided_Rkts_M282__MPP_APKWS
    ): 2016,
    Weapon.from_pydcs(
        Weapons.BRU_42_with_3_x_LAU_131_pods___7_x_2_75_Hydra__Laser_Guided_Rkts_M151__HE_APKWS
    ): 2016,
    Weapon.from_pydcs(
        Weapons.BRU_42_with_3_x_LAU_131_pods___7_x_2_75_Hydra__Laser_Guided_Rkts_M282__MPP_APKWS
    ): 2016,
    # Russia
    # KAB-1500
    Weapon.from_pydcs(Weapons.KAB_1500Kr___1500kg_TV_Guided_Bomb): 1985,
    Weapon.from_pydcs(Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb): 1995,
    Weapon.from_pydcs(Weapons.KAB_1500LG_Pr___1500kg_Laser_Guided_Penetrator_Bomb): 1990,
    # KAB-500
    Weapon.from_pydcs(Weapons.KAB_500Kr___500kg_TV_Guided_Bomb): 1980,
    Weapon.from_pydcs(Weapons.KAB_500LG___500kg_Laser_Guided_Bomb): 1995,
    Weapon.from_pydcs(Weapons.KAB_500S___500kg_GPS_Guided_Bomb): 2000,
    # Kh Series
    Weapon.from_pydcs(Weapons.Kh_22__AS_4_Kitchen____1000kg__AShM__IN__Act_Pas_Rdr): 1962,
    Weapon.from_pydcs(Weapons.Kh_23L_Grom__AS_7_Kerry____286kg__ASM__Laser_Guided): 1975,
    Weapon.from_pydcs(Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser): 1975,
    Weapon.from_pydcs(Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser_): 1975,
    Weapon.from_pydcs(Weapons.Kh_25ML__AS_10_Karen____300kg__ASM__Semi_Act_Laser__): 1975,
    Weapon.from_pydcs(Weapons.Kh_25MP__AS_12_Kegler____320kg__ARM__Pas_Rdr): 1975,
    Weapon.from_pydcs(Weapons.Kh_25MPU__Updated_AS_12_Kegler____320kg__ARM__IN__Pas_Rdr): 1980,
    Weapon.from_pydcs(Weapons.Kh_25MPU__Updated_AS_12_Kegler____320kg__ARM__IN__Pas_Rdr_): 1980,
    Weapon.from_pydcs(Weapons.Kh_25MPU__Updated_AS_12_Kegler____320kg__ARM__IN__Pas_Rdr__): 1980,
    Weapon.from_pydcs(Weapons.Kh_25MR__AS_10_Karen____300kg__ASM__10km__RC_Guided): 1975,
    Weapon.from_pydcs(Weapons.Kh_25MR__AS_10_Karen____300kg__ASM__RC_Guided): 1975,
    Weapon.from_pydcs(Weapons.Kh_28__AS_9_Kyle____720kg__ARM__Pas_Rdr): 1973,
    Weapon.from_pydcs(Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser): 1980,
    Weapon.from_pydcs(Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser_): 1980,
    Weapon.from_pydcs(Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser__): 1980,
    Weapon.from_pydcs(Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided): 1980,
    Weapon.from_pydcs(Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_): 1980,
    Weapon.from_pydcs(Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided__): 1980,
    Weapon.from_pydcs(Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr): 1980,
    Weapon.from_pydcs(Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr_): 1980,
    Weapon.from_pydcs(Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr__): 1980,
    Weapon.from_pydcs(Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr): 1980,
    Weapon.from_pydcs(Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr_): 1980,
    Weapon.from_pydcs(Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr__): 1980,
    Weapon.from_pydcs(Weapons.Kh_35__AS_20_Kayak____520kg__AShM__IN__Act_Rdr): 2003,
    Weapon.from_pydcs(Weapons.Kh_35__AS_20_Kayak____520kg__AShM__IN__Act_Rdr_): 2003,
    Weapon.from_pydcs(Weapons._6_x_Kh_35__AS_20_Kayak____520kg__AShM__IN__Act_Rdr): 2003,
    Weapon.from_pydcs(Weapons.Kh_41__SS_N_22_Sunburn____4500kg__AShM__IN__Act_Rdr): 1984,
    Weapon.from_pydcs(Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr): 1985,
    Weapon.from_pydcs(Weapons.Kh_58U__AS_11_Kilter____640kg__ARM__IN__Pas_Rdr_): 1985,
    Weapon.from_pydcs(Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN): 1990,
    Weapon.from_pydcs(Weapons.Kh_65__AS_15B_Kent____1250kg__ASM__IN__MCC): 1992,
    Weapon.from_pydcs(Weapons._6_x_Kh_65__AS_15B_Kent____1250kg__ASM__IN__MCC): 1992,
    Weapon.from_pydcs(Weapons._8_x_Kh_65__AS_15B_Kent____1250kg__ASM__IN__MCC): 1992,
    Weapon.from_pydcs(Weapons.Kh_66_Grom__21__APU_68): 1968,
    # ECM
    Weapon.from_pydcs(Weapons.L175V_Khibiny_ECM_pod): 1982,
    # R-13
    Weapon.from_pydcs(Weapons.R_13M): 1961,
    Weapon.from_pydcs(Weapons.R_13M1): 1965,
    # R-24
    Weapon.from_pydcs(Weapons.R_24R__AA_7_Apex_SA____Semi_Act_Rdr): 1981,
    Weapon.from_pydcs(Weapons.R_24T__AA_7_Apex_IR____Infra_Red): 1981,
    # R-27
    Weapon.from_pydcs(Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range): 1983,
    Weapon.from_pydcs(Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range): 1986,
    Weapon.from_pydcs(Weapons.R_27R__AA_10_Alamo_A____Semi_Act_Rdr): 1983,
    Weapon.from_pydcs(Weapons.R_27T__AA_10_Alamo_B____Infra_Red): 1983,
    # R-33
    Weapon.from_pydcs(Weapons.R_33__AA_9_Amos____Semi_Act_Rdr): 1981,
    # R-3
    Weapon.from_pydcs(Weapons.R_3R): 1966,
    Weapon.from_pydcs(Weapons.R_3S): 1962,
    # R-40
    Weapon.from_pydcs(Weapons.R_40R__AA_6_Acrid____Semi_Act_Rdr): 1976,
    Weapon.from_pydcs(Weapons.R_40T__AA_6_Acrid____Infra_Red): 1976,
    # R-55
    Weapon.from_pydcs(Weapons.R_55): 1957,
    Weapon.from_pydcs(Weapons.RS2US): 1957,
    # R-60
    Weapon.from_pydcs(Weapons.R_60): 1973,
    Weapon.from_pydcs(Weapons.R_60_x_2): 1973,
    Weapon.from_pydcs(Weapons.R_60_x_2_): 1973,
    Weapon.from_pydcs(Weapons.APU_60_1M_with_R_60M__AA_8_Aphid____Infra_Red): 1982,
    Weapon.from_pydcs(Weapons.R_60M): 1982,
    Weapon.from_pydcs(Weapons.R_60M__AA_8_Aphid____Infra_Red): 1982,
    Weapon.from_pydcs(Weapons.APU_60_2M_with_2_x_R_60M__AA_8_Aphid____Infra_Red): 1982,
    Weapon.from_pydcs(Weapons.APU_60_2M_with_2_x_R_60M__AA_8_Aphid____Infra_Red_): 1982,
    Weapon.from_pydcs(Weapons.R_60M_x_2): 1982,
    Weapon.from_pydcs(Weapons.R_60M_x_2_): 1982,
    # R-73
    Weapon.from_pydcs(Weapons.R_73__AA_11_Archer____Infra_Red): 1984,
    Weapon.from_pydcs(Weapons.R_73__AA_11_Archer____Infra_Red_): 1984,
    # R-77
    Weapon.from_pydcs(Weapons.R_77__AA_12_Adder____Active_Rdr): 2002,
    Weapon.from_pydcs(Weapons.R_77__AA_12_Adder____Active_Rdr_): 2002,
    # UK
    # ALARM
    Weapon.from_pydcs(Weapons.ALARM): 1990,
    # France
    # BLG-66 Belouga
    Weapon.from_pydcs(Weapons.AUF2_BLG_66_AC_x_2): 1979,
    Weapon.from_pydcs(Weapons.BLG_66_AC_Belouga): 1979,
    Weapon.from_pydcs(Weapons.BLG_66_Belouga___290kg_CBU__151_Frag_Pen_bomblets): 1979,
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
