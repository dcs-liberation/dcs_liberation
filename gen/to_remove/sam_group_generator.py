import random
from typing import Dict, Iterable, List, Optional, Sequence, Set, Type

from dcs.unitgroup import VehicleGroup

from game import Game
from game.factions.faction import Faction
from game.theater.theatergroundobject import SamGroundObject, AirDefenseRange
from gen.to_remove.aaa_bofors import BoforsGenerator
from gen.to_remove.aaa_flak import FlakGenerator
from gen.to_remove.aaa_flak18 import Flak18Generator
from gen.to_remove.aaa_ks19 import KS19Generator
from gen.to_remove.aaa_ww2_ally_flak import AllyWW2FlakGenerator
from gen.to_remove.aaa_zsu57 import ZSU57Generator
from gen.to_remove.aaa_zu23_insurgent import ZU23InsurgentGenerator
from gen.to_remove.airdefensegroupgenerator import (
    AirDefenseGroupGenerator,
)
from gen.to_remove.cold_war_flak import (
    ColdWarFlakGenerator,
    EarlyColdWarFlakGenerator,
)
from gen.to_remove.freya_ewr import FreyaGenerator
from gen.to_remove.sam_avenger import AvengerGenerator
from gen.to_remove.sam_chaparral import ChaparralGenerator
from gen.to_remove.sam_gepard import GepardGenerator
from gen.to_remove.sam_hawk import HawkGenerator
from gen.to_remove.sam_hq7 import HQ7Generator
from gen.to_remove.sam_linebacker import LinebackerGenerator
from gen.to_remove.sam_nasams import NasamBGenerator, NasamCGenerator
from gen.to_remove.sam_patriot import PatriotGenerator
from gen.to_remove.sam_rapier import RapierGenerator
from gen.to_remove.sam_roland import RolandGenerator
from gen.to_remove.sam_sa10 import (
    SA10Generator,
    Tier2SA10Generator,
    Tier3SA10Generator,
    SA10BGenerator,
    SA12Generator,
    SA20Generator,
    SA20BGenerator,
    SA23Generator,
)
from gen.to_remove.sam_sa11 import SA11Generator
from gen.to_remove.sam_sa13 import SA13Generator
from gen.to_remove.sam_sa15 import SA15Generator
from gen.to_remove.sam_sa17 import SA17Generator
from gen.to_remove.sam_sa19 import SA19Generator
from gen.to_remove.sam_sa2 import SA2Generator
from gen.to_remove.sam_sa3 import SA3Generator
from gen.to_remove.sam_sa5 import SA5Generator, SA5FlatFaceGenerator
from gen.to_remove.sam_sa6 import SA6Generator
from gen.to_remove.sam_sa8 import SA8Generator
from gen.to_remove.sam_sa9 import SA9Generator
from gen.to_remove.sam_vulcan import VulcanGenerator
from gen.to_remove.sam_zsu23 import ZSU23Generator
from gen.to_remove.sam_zu23 import ZU23Generator
from gen.to_remove.sam_zu23_ural import ZU23UralGenerator
from gen.to_remove.sam_zu23_ural_insurgent import ZU23UralInsurgentGenerator

SAM_MAP: Dict[str, Type[AirDefenseGroupGenerator]] = {
    "HawkGenerator": HawkGenerator,
    "ZU23Generator": ZU23Generator,
    "ZU23UralGenerator": ZU23UralGenerator,
    "ZU23UralInsurgentGenerator": ZU23UralInsurgentGenerator,
    "ZU23InsurgentGenerator": ZU23InsurgentGenerator,
    "ZSU23Generator": ZSU23Generator,
    "VulcanGenerator": VulcanGenerator,
    "LinebackerGenerator": LinebackerGenerator,
    "RapierGenerator": RapierGenerator,
    "AvengerGenerator": AvengerGenerator,
    "GepardGenerator": GepardGenerator,
    "RolandGenerator": RolandGenerator,
    "PatriotGenerator": PatriotGenerator,
    "ChaparralGenerator": ChaparralGenerator,
    "BoforsGenerator": BoforsGenerator,
    "FlakGenerator": FlakGenerator,
    "SA2Generator": SA2Generator,
    "SA3Generator": SA3Generator,
    "SA5Generator": SA5Generator,
    "SA5FlatFaceGenerator": SA5FlatFaceGenerator,
    "SA6Generator": SA6Generator,
    "SA8Generator": SA8Generator,
    "SA9Generator": SA9Generator,
    "SA10Generator": SA10Generator,
    "Tier2SA10Generator": Tier2SA10Generator,
    "Tier3SA10Generator": Tier3SA10Generator,
    "SA11Generator": SA11Generator,
    "SA13Generator": SA13Generator,
    "SA15Generator": SA15Generator,
    "SA19Generator": SA19Generator,
    "HQ7Generator": HQ7Generator,
    "Flak18Generator": Flak18Generator,
    "ColdWarFlakGenerator": ColdWarFlakGenerator,
    "EarlyColdWarFlakGenerator": EarlyColdWarFlakGenerator,
    "FreyaGenerator": FreyaGenerator,
    "AllyWW2FlakGenerator": AllyWW2FlakGenerator,
    "ZSU57Generator": ZSU57Generator,
    "KS19Generator": KS19Generator,
    "SA10BGenerator": SA10BGenerator,
    "SA12Generator": SA12Generator,
    "SA17Generator": SA17Generator,
    "SA20Generator": SA20Generator,
    "SA20BGenerator": SA20BGenerator,
    "SA23Generator": SA23Generator,
    "NasamBGenerator": NasamBGenerator,
    "NasamCGenerator": NasamCGenerator,
}


def get_faction_possible_sams_generator(
    faction: Faction,
) -> List[Type[AirDefenseGroupGenerator]]:
    """
    Return the list of possible SAM generator for the given faction
    :param faction: Faction name to search units for
    """
    return [SAM_MAP[s] for s in faction.air_defenses]


def _generate_anti_air_from(
    generators: Sequence[Type[AirDefenseGroupGenerator]],
    game: Game,
    ground_object: SamGroundObject,
) -> List[VehicleGroup]:
    if not generators:
        return []
    sam_generator_class = random.choice(generators)
    generator = sam_generator_class(game, ground_object)
    generator.generate()
    return list(generator.groups)


def generate_anti_air_group(
    game: Game,
    ground_object: SamGroundObject,
    faction: Faction,
    ranges: Optional[Iterable[Set[AirDefenseRange]]] = None,
) -> List[VehicleGroup]:
    """
    This generate a SAM group
    :param game: The Game.
    :param ground_object: The ground object which will own the sam group.
    :param faction: Owner faction.
    :param ranges: Optional list of preferred ranges of the air defense to
        create. If None, any generator may be used. Otherwise generators
        matching the given ranges will be used in order of preference. For
        example, when given `[{Long, Medium}, {Short}]`, long and medium range
        air defenses will be tried first with no bias, and short range air
        defenses will be used if no long or medium range generators are
        available to the faction. If instead `[{Long}, {Medium}, {Short}]` had
        been used, long range systems would take precedence over medium range
        systems. If instead `[{Long, Medium, Short}]` had been used, all types
        would be considered with equal preference.
    :return: The generated group, or None if one could not be generated.
    """
    generators = get_faction_possible_sams_generator(faction)
    if ranges is None:
        ranges = [
            {
                AirDefenseRange.Long,
                AirDefenseRange.Medium,
                AirDefenseRange.Short,
            }
        ]

    for range_options in ranges:
        generators_for_range = [g for g in generators if g.range() in range_options]
        groups = _generate_anti_air_from(generators_for_range, game, ground_object)
        if groups:
            return groups
    return []
