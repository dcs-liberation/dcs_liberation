import json
from pathlib import Path
import unittest

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
    CVN_74_John_C__Stennis,
    LHA_1_Tarawa,
    FFG_Oliver_Hazzard_Perry,
    DDG_Arleigh_Burke_IIa,
    CG_Ticonderoga,
)
from dcs.vehicles import Armor, Unarmed, Infantry, Artillery

from game.factions.faction import Faction


THIS_DIR = Path(__file__).parent
RESOURCES_DIR = THIS_DIR / "resources"


class TestFactionLoader(unittest.TestCase):
    def setUp(self):
        pass

    def test_load_valid_faction(self):
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

            self.assertIn(Armor.MBT_M1A2_Abrams, faction.frontline_units)
            self.assertIn(Armor.ATGM_Stryker, faction.frontline_units)
            self.assertIn(Armor.IFV_M1126_Stryker_ICV, faction.frontline_units)
            self.assertIn(Armor.IFV_M2A2_Bradley, faction.frontline_units)
            self.assertIn(Armor.IFV_LAV_25, faction.frontline_units)
            self.assertIn(Armor.APC_HMMWV__Scout, faction.frontline_units)
            self.assertIn(Armor.ATGM_HMMWV, faction.frontline_units)

            self.assertIn(Artillery.MLRS_M270_227mm, faction.artillery_units)
            self.assertIn(Artillery.SPH_M109_Paladin_155mm, faction.artillery_units)

            self.assertIn(Unarmed.Truck_M818_6x6, faction.logistics_units)

            self.assertIn(Infantry.Infantry_M4, faction.infantry_units)
            self.assertIn(Infantry.Infantry_M249, faction.infantry_units)

            self.assertIn("AvengerGenerator", faction.air_defenses)

            self.assertIn("HawkGenerator", faction.air_defenses)

            self.assertIn(CVN_74_John_C__Stennis, faction.aircraft_carrier)
            self.assertIn(LHA_1_Tarawa, faction.helicopter_carrier)
            self.assertIn(FFG_Oliver_Hazzard_Perry, faction.destroyers)
            self.assertIn(DDG_Arleigh_Burke_IIa, faction.destroyers)
            self.assertIn(CG_Ticonderoga, faction.cruisers)

            self.assertIn("mod", faction.requirements.keys())
            self.assertIn("Some mod is required", faction.requirements.values())

            self.assertEqual(4, len(faction.carrier_names))
            self.assertEqual(5, len(faction.helicopter_carrier_names))

            self.assertIn("OliverHazardPerryGroupGenerator", faction.navy_generators)
            self.assertIn("ArleighBurkeGroupGenerator", faction.navy_generators)

    def test_load_valid_faction_with_invalid_country(self):

        with (RESOURCES_DIR / "invalid_faction_country.json").open("r") as data:
            try:
                Faction.from_json(json.load(data))
                self.fail("Should have thrown assertion error")
            except AssertionError as e:
                pass
