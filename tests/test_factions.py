import json
from pathlib import Path
import unittest
import pytest

from dcs.helicopters import UH_1H, AH_64A
from dcs.planes import (
    F_15C,
    F_15E,
    F_14B,
    FA_18C_hornet,
    F_16C_50,
    A_10A,
    AV8BNA,
    B_52H,
    B_1B,
    F_117A,
    MQ_9_Reaper,
    E_3A,
    E_2C,
    KC130,
    KC_135,
    A_10C,
    A_10C_2,
)
from dcs.ships import (
    Stennis,
    LHA_Tarawa,
    PERRY,
    USS_Arleigh_Burke_IIa,
    TICONDEROG,
)
from dcs.vehicles import Armor, Unarmed, Infantry, Artillery

from game.factions.faction import Faction


THIS_DIR = Path(__file__).parent
RESOURCES_DIR = THIS_DIR / "resources"


class TestFactionLoader(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @pytest.mark.skip(reason="Faction unit names in the json files are outdated")
    def test_load_valid_faction(self) -> None:
        with (RESOURCES_DIR / "valid_faction.json").open("r") as data:
            faction = Faction.from_json(json.load(data))

            self.assertEqual(faction.country, "USA")
            self.assertEqual(faction.name, "USA 2005")
            self.assertEqual(faction.authors, "Khopa")
            self.assertEqual(faction.description, "This is a test description")

            self.assertIn(F_15C, faction.aircrafts)
            self.assertIn(F_15E, faction.aircrafts)
            self.assertIn(F_14B, faction.aircrafts)
            self.assertIn(FA_18C_hornet, faction.aircrafts)
            self.assertIn(F_16C_50, faction.aircrafts)
            self.assertIn(A_10A, faction.aircrafts)
            self.assertIn(AV8BNA, faction.aircrafts)
            self.assertIn(UH_1H, faction.aircrafts)
            self.assertIn(AH_64A, faction.aircrafts)
            self.assertIn(B_52H, faction.aircrafts)
            self.assertIn(B_1B, faction.aircrafts)
            self.assertIn(F_117A, faction.aircrafts)
            self.assertIn(A_10C, faction.aircrafts)
            self.assertIn(A_10C_2, faction.aircrafts)

            self.assertEqual(len(faction.awacs), 1)
            self.assertIn(E_3A, faction.awacs)
            self.assertIn(E_2C, faction.awacs)

            self.assertEqual(len(faction.tankers), 2)
            self.assertIn(KC_135, faction.tankers)
            self.assertIn(KC130, faction.tankers)

            self.assertTrue(faction.has_jtac)
            self.assertEqual(faction.jtac_unit, MQ_9_Reaper)

            self.assertIn(Armor.M_1_Abrams, faction.frontline_units)
            self.assertIn(Armor.M1134_Stryker_ATGM, faction.frontline_units)
            self.assertIn(Armor.M1126_Stryker_ICV, faction.frontline_units)
            self.assertIn(Armor.M_2_Bradley, faction.frontline_units)
            self.assertIn(Armor.LAV_25, faction.frontline_units)
            self.assertIn(Armor.M1043_HMMWV_Armament, faction.frontline_units)
            self.assertIn(Armor.M1045_HMMWV_TOW, faction.frontline_units)

            self.assertIn(Artillery.MLRS, faction.artillery_units)
            self.assertIn(Artillery.M_109, faction.artillery_units)

            self.assertIn(Unarmed.M_818, faction.logistics_units)

            self.assertIn(Infantry.Soldier_M4, faction.infantry_units)
            self.assertIn(Infantry.Soldier_M249, faction.infantry_units)

            self.assertIn(Stennis.name, faction.naval_units)
            self.assertIn(LHA_Tarawa.name, faction.naval_units)

            self.assertIn("mod", faction.requirements.keys())
            self.assertIn("Some mod is required", faction.requirements.values())

            self.assertEqual(4, len(faction.carrier_names))
            self.assertEqual(5, len(faction.helicopter_carrier_names))

    @pytest.mark.skip(reason="Faction unit names in the json files are outdated")
    def test_load_valid_faction_with_invalid_country(self) -> None:

        with (RESOURCES_DIR / "invalid_faction_country.json").open("r") as data:
            try:
                Faction.from_json(json.load(data))
                self.fail("Should have thrown assertion error")
            except AssertionError as e:
                pass
