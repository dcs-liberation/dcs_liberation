import json
import unittest

from dcs.helicopters import UH_1H, AH_64A
from dcs.planes import F_15C, F_15E, F_14B, FA_18C_hornet, F_16C_50, A_10A, AV8BNA, B_52H, B_1B, F_117A

from game.factions.faction import Faction


class TestFactionLoader(unittest.TestCase):

    def setUp(self):
        pass

    def test_load_valid_faction(self):
        with open("./resources/valid_faction.json", 'r') as data:
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
