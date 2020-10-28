import inspect
import dcs

DEFAULT_AVAILABLE_BUILDINGS = ['fuel', 'ammo', 'comms', 'oil', 'ware', 'farp', 'fob', 'power', 'factory', 'derrick', 'aa', 'iads-controlcenter', 'iads-ewr', 'iads-commnode', 'iads-power']

WW2_GERMANY_BUILDINGS = ['fuel', 'factory', 'ww2bunker', 'ww2bunker', 'ww2bunker', 'allycamp', 'allycamp', 'aa']
WW2_ALLIES_BUILDINGS = ['fuel', 'factory', 'allycamp', 'allycamp', 'allycamp', 'allycamp', 'allycamp', 'aa']

FORTIFICATION_BUILDINGS = ['Siegfried Line', 'Concertina wire', 'Concertina Wire', 'Czech hedgehogs 1', 'Czech hedgehogs 2',
                           'Dragonteeth 1', 'Dragonteeth 2', 'Dragonteeth 3', 'Dragonteeth 4', 'Dragonteeth 5',
                           'Haystack 1', 'Haystack 2', 'Haystack 3', 'Haystack 4', 'Hemmkurvenvenhindernis',
                           'Log posts 1', 'Log posts 2', 'Log posts 3', 'Log ramps 1', 'Log ramps 2', 'Log ramps 3',
                           'Belgian Gate', 'Container white']

FORTIFICATION_UNITS = [c for c in vars(dcs.vehicles.Fortification).values() if inspect.isclass(c)]
FORTIFICATION_UNITS_ID = [c.id for c in vars(dcs.vehicles.Fortification).values() if inspect.isclass(c)]