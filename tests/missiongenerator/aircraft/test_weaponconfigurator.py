import unittest
from unittest.mock import Mock, patch

from dcs.vehicles import AirDefence
from game.missiongenerator.aircraft.weaponsconfigurator import (
    WeaponsConfigurator,
    PassthroughConfigurator,
    ShrikeConfigurator,
    WeaponsConfigurator,
)
from game.theater import MissionTarget, TheaterGroundObject


class TestPassthroughConfigurator(unittest.TestCase):

    def test_passthrough_configurator_settings(self) -> None:
        """
        Test PassthroughConfigurator settings method
        """
        # Create a mock weapon with settings
        weapon_group = Mock()
        weapon_group.settings = {"test_setting": "test_value"}

        weapon = Mock()
        weapon.weapon_group = weapon_group

        target = Mock(spec=MissionTarget)

        configurator = PassthroughConfigurator()
        result = configurator.settings(target, weapon)

        self.assertEqual(result, {"test_setting": "test_value"})

    def test_passthrough_configurator_settings_no_settings(self) -> None:
        """
        Test PassthroughConfigurator when weapon group has no settings
        """
        weapon_group = Mock()
        weapon_group.settings = None

        weapon = Mock()
        weapon.weapon_group = weapon_group

        target = Mock(spec=MissionTarget)

        configurator = PassthroughConfigurator()
        result = configurator.settings(target, weapon)

        self.assertIsNone(result)


class TestShrikeConfigurator(unittest.TestCase):

    def test_shrike_configurator_settings_non_ground_object(self) -> None:
        """
        Test ShrikeConfigurator with non-TheaterGroundObject target
        """
        target = Mock(spec=MissionTarget)

        weapon = Mock()
        weapon.weapon_group = Mock()
        weapon.weapon_group.settings = None

        configurator = ShrikeConfigurator()
        result = configurator.settings(target, weapon)

        self.assertIsNone(result)

    def test_shrike_configurator_settings_dead_object(self) -> None:
        """
        Test ShrikeConfigurator with dead target
        """
        # Create a ground object with SNR-125 target
        group = Mock()
        unit = Mock()
        unit.alive = False
        unit.type = AirDefence.Snr_s_125_tr
        group.units = [unit]

        target = Mock(spec=TheaterGroundObject)
        target.groups = [group]

        weapon = Mock()
        weapon.weapon_group = Mock()
        weapon.weapon_group.settings = None

        configurator = ShrikeConfigurator()
        result = configurator.settings(target, weapon)

        self.assertIsNone(result)

    def test_shrike_configurator_settings_snr_125_target(self) -> None:
        """
        Test ShrikeConfigurator with SNR-125 target
        """

        # Create a ground object with SNR-125 target
        group = Mock()
        unit = Mock()
        unit.alive = True
        unit.type = AirDefence.Snr_s_125_tr
        group.units = [unit]

        target = Mock(spec=TheaterGroundObject)
        target.groups = [group]

        weapon = Mock()
        weapon.weapon_group = Mock()
        weapon.weapon_group.settings = None

        configurator = ShrikeConfigurator()
        result = configurator.settings(target, weapon)

        # Check that the correct settings are returned
        expected_settings = {
            "EAS_bypass_ctrl": 0,
            "G_bias": True,
            "NFP_PRESID": "AGM_45",
            "NFP_PRESVER": 1,
            "NFP_rfgu_type": 9,
            "rf_lower_limit_ctrl_Mk49Mod1": 6000000000,
            "rf_upper_limit_ctrl_Mk49Mod1": 10000000000,
            "smoke_marker": 0,
        }

        self.assertEqual(result, expected_settings)

    def test_shrike_configurator_settings_snr_75_target(self) -> None:
        """
        Test ShrikeConfigurator with SNR-75 target
        """

        # Create a ground object with SNR-75 target
        group = Mock()
        unit = Mock()
        unit.alive = True
        unit.type = AirDefence.SNR_75V
        group.units = [unit]

        target = Mock(spec=TheaterGroundObject)
        target.groups = [group]

        weapon = Mock()
        weapon.weapon_group = Mock()
        weapon.weapon_group.settings = None

        configurator = ShrikeConfigurator()
        result = configurator.settings(target, weapon)

        # Check that the correct settings are returned
        expected_settings = {
            "EAS_bypass_ctrl": 0,
            "NFP_PRESID": "AGM_45",
            "NFP_PRESVER": 1,
            "NFP_rfgu_type": 1,
            "rf_lower_limit_ctrl_Mk22Mod2": 4800000000,
            "rf_upper_limit_ctrl_Mk22Mod2": 5200000000,
            "smoke_marker": 0,
        }

        self.assertEqual(result, expected_settings)

    def test_shrike_configurator_settings_son_9_target(self) -> None:
        """
        Test ShrikeConfigurator with SON-9 target
        """
        # Create a ground object with SON-9 target
        group = Mock()
        unit = Mock()
        unit.alive = True
        unit.type = AirDefence.SON_9
        group.units = [unit]

        target = Mock(spec=TheaterGroundObject)
        target.groups = [group]

        weapon = Mock()
        weapon.weapon_group = Mock()
        weapon.weapon_group.settings = None

        configurator = ShrikeConfigurator()
        result = configurator.settings(target, weapon)

        # Check that the correct settings are returned
        expected_settings = {
            "EAS_bypass_ctrl": 0,
            "NFP_PRESID": "AGM_45",
            "NFP_PRESVER": 1,
            "NFP_rfgu_type": 2,
            "rf_lower_limit_ctrl_Mk22Mod2": 2000000000,
            "rf_upper_limit_ctrl_Mk22Mod2": 4000000000,
            "smoke_marker": 0,
        }

        self.assertEqual(result, expected_settings)


class TestSettingsForWeaponTarget(unittest.TestCase):

    def test_settings_for_weapon_target_with_configurator(self) -> None:
        """
        Test settings_for_weapon_target with configurator specified
        """

        # Create a weapon with configurator
        weapon_group = Mock()
        weapon_group.configurator = "Passthrough"
        weapon_group.settings = {"test": "value"}

        weapon = Mock()
        weapon.weapon_group = weapon_group

        target = Mock(spec=MissionTarget)

        result = WeaponsConfigurator.settings_for_weapon_target(weapon, target)

        self.assertEqual(result, {"test": "value"})

    def test_settings_for_weapon_target_no_configurator(self) -> None:
        """
        Test settings_for_weapon_target with no configurator specified
        """
        # Create a weapon without configurator
        weapon_group = Mock()
        weapon_group.configurator = None
        weapon_group.settings = None

        weapon = Mock()
        weapon.weapon_group = weapon_group

        target = Mock(spec=MissionTarget)

        result = WeaponsConfigurator.settings_for_weapon_target(weapon, target)

        self.assertIsNone(result)
