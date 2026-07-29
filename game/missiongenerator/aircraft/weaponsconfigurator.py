from abc import ABC, abstractmethod
from typing import Any, Optional

from dcs.vehicles import AirDefence

from game.theater import MissionTarget, TheaterGroundObject

from game.data.weapons import Weapon

WeaponSettings = dict[str, Any]


class WeaponsConfigurator(ABC):

    @abstractmethod
    def settings(
        self, target: MissionTarget, weapon: Weapon
    ) -> Optional[WeaponSettings]:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @staticmethod
    def settings_for_weapon_target(
        weapon: Optional[Weapon], target: MissionTarget
    ) -> Optional[WeaponSettings]:
        if weapon is None:  # empty pylon, nothing to do
            return None
        if weapon.weapon_group.configurator:
            for configurator_type in [PassthroughConfigurator, ShrikeConfigurator]:
                if configurator_type.name() == weapon.weapon_group.configurator:
                    configurator = configurator_type()
                    return configurator.settings(target, weapon)
        return None


class PassthroughConfigurator(WeaponsConfigurator):

    @staticmethod
    def name() -> str:
        return "Passthrough"

    def settings(
        self, target: MissionTarget, weapon: Weapon
    ) -> Optional[WeaponSettings]:
        if weapon.weapon_group.settings is None:
            return None
        return weapon.weapon_group.settings


class ShrikeConfigurator(WeaponsConfigurator):

    @staticmethod
    def name() -> str:
        return "Shrike"

    def settings(
        self, target: MissionTarget, weapon: Weapon
    ) -> Optional[WeaponSettings]:
        settings: dict[str, Any] = {}
        if not isinstance(target, TheaterGroundObject):
            return None
        for group in target.groups:
            for unit in group.units:
                if not unit.alive:
                    continue
                # SNR-125 Low Blow (SA-3)/1S91 Straight Flush: MK-49 Mod 1
                if unit.type in [AirDefence.Snr_s_125_tr, AirDefence.Kub_1S91_str]:
                    settings["EAS_bypass_ctrl"] = 0
                    settings["G_bias"] = True
                    settings["NFP_PRESID"] = "AGM_45"
                    settings["NFP_PRESVER"] = 1
                    settings["NFP_rfgu_type"] = 9
                    settings["rf_lower_limit_ctrl_Mk49Mod1"] = 6000000000
                    settings["rf_upper_limit_ctrl_Mk49Mod1"] = 10000000000
                    settings["smoke_marker"] = 0
                    return settings
                # SNR-75 Fan Song (SA-2): Mk-22
                if unit.type == AirDefence.SNR_75V:
                    settings["EAS_bypass_ctrl"] = 0
                    settings["NFP_PRESID"] = "AGM_45"
                    settings["NFP_PRESVER"] = 1
                    settings["NFP_rfgu_type"] = 1
                    settings["rf_lower_limit_ctrl_Mk22Mod2"] = 4800000000
                    settings["rf_upper_limit_ctrl_Mk22Mod2"] = 5200000000
                    settings["smoke_marker"] = 0
                    return settings
                # SON-9 Fire Can / ST-68U Tin Shield: Mk-23
                if unit.type in [AirDefence.SON_9, AirDefence.RLS_19J6]:
                    settings["EAS_bypass_ctrl"] = 0
                    settings["NFP_PRESID"] = "AGM_45"
                    settings["NFP_PRESVER"] = 1
                    settings["NFP_rfgu_type"] = 2
                    settings["rf_lower_limit_ctrl_Mk22Mod2"] = 2000000000
                    settings["rf_upper_limit_ctrl_Mk22Mod2"] = 4000000000
                    settings["smoke_marker"] = 0
                    return settings
        return None
