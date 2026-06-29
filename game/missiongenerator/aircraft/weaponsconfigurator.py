from abc import ABC, abstractmethod
from typing import Any, Optional

from dcs.vehicles import AirDefence

from game.theater import MissionTarget, TheaterGroundObject

from game.data.weapons import Weapon

WeaponSettings = dict[str, Any]


class WeaponsConfigurator(ABC):

    def __init__(self, target: MissionTarget):
        self.target = target

    @abstractmethod
    def settings(self) -> Optional[WeaponSettings]:
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
            for configurator_type in [NoOpConfigurator, ShrikeConfigurator]:
                if configurator_type.name() == weapon.weapon_group.configurator:
                    configurator = configurator_type(target)
                    return configurator.settings()
        return None


class NoOpConfigurator(WeaponsConfigurator):

    @staticmethod
    def name() -> str:
        return "NoOp"

    def settings(self) -> Optional[WeaponSettings]:
        return None


class ShrikeConfigurator(WeaponsConfigurator):

    @staticmethod
    def name() -> str:
        return "Shrike"

    def settings(self) -> Optional[WeaponSettings]:
        settings: dict[str, Any] = {}
        if not isinstance(self.target, TheaterGroundObject):
            return None
        for group in self.target.groups:
            for unit in group.units:
                if not unit.alive:
                    continue
                # SNR-125 Low Blow (SA-3): MK-49 Mod 1
                if unit.type == AirDefence.Snr_s_125_tr:
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
