import random
from typing import Dict, Iterable, List, Optional, Sequence, Set, Type

from dcs.unitgroup import VehicleGroup
from dcs.mapping import Point

from game import Game
from game.factions.faction import Faction
from game.theater import ControlPoint
from game.theater.theatergroundobject import SamGroundObject
from gen.sam.aaa_bofors import BoforsGenerator
from gen.sam.aaa_flak import FlakGenerator
from gen.sam.aaa_flak18 import Flak18Generator
from gen.sam.aaa_ks19 import KS19Generator
from gen.sam.aaa_ww2_ally_flak import AllyWW2FlakGenerator
from gen.sam.aaa_zsu57 import ZSU57Generator
from gen.sam.aaa_zu23_insurgent import ZU23InsurgentGenerator
from gen.sam.airdefensegroupgenerator import (
    AirDefenseGroupGenerator,
    AirDefenseRange,
)
from gen.sam.cold_war_flak import (
    ColdWarFlakGenerator,
    EarlyColdWarFlakGenerator,
)
from gen.sam.freya_ewr import FreyaGenerator
from gen.sam.sam_avenger import AvengerGenerator
from gen.sam.sam_chaparral import ChaparralGenerator
from gen.sam.sam_gepard import GepardGenerator
from gen.sam.sam_hawk import HawkGenerator
from gen.sam.sam_hq7 import HQ7Generator
from gen.sam.sam_linebacker import LinebackerGenerator
from gen.sam.sam_patriot import PatriotGenerator
from gen.sam.sam_rapier import RapierGenerator
from gen.sam.sam_roland import RolandGenerator
from gen.sam.sam_sa10 import (
    SA10Generator,
    Tier2SA10Generator,
    Tier3SA10Generator,
    SA10BGenerator,
    SA12Generator,
    SA20Generator,
    SA20BGenerator,
    SA23Generator,
)
from gen.sam.sam_sa11 import SA11Generator
from gen.sam.sam_sa13 import SA13Generator
from gen.sam.sam_sa15 import SA15Generator
from gen.sam.sam_sa17 import SA17Generator
from gen.sam.sam_sa19 import SA19Generator
from gen.sam.sam_sa2 import SA2Generator
from gen.sam.sam_sa3 import SA3Generator
from gen.sam.sam_sa6 import SA6Generator
from gen.sam.sam_sa8 import SA8Generator
from gen.sam.sam_sa9 import SA9Generator
from gen.sam.sam_vulcan import VulcanGenerator
from gen.sam.sam_zsu23 import ZSU23Generator
from gen.sam.sam_zu23 import ZU23Generator
from gen.sam.sam_zu23_ural import ZU23UralGenerator
from gen.sam.sam_zu23_ural_insurgent import ZU23UralInsurgentGenerator

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
    name: str,
    group_id: int,
    position: Point,
    control_point: ControlPoint,
) -> Optional[SamGroundObject]:
    if not generators:
        return None
    sam_generator_class = random.choice(generators)
    ground_object = SamGroundObject(
        name, group_id, position, control_point, sam_generator_class.range()
    )
    generator = sam_generator_class(game, ground_object)
    generator.generate()
    ground_object.set_groups(list(generator.groups), list(generator.ranges))
    return ground_object


def generate_anti_air_ground_object(
    game: Game,
    name: str,
    group_id: int,
    position: Point,
    control_point: ControlPoint,
    faction: Faction,
    ranges: Optional[Iterable[Set[AirDefenseRange]]] = None,
) -> Optional[SamGroundObject]:
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
        ground_object = _generate_anti_air_from(
            generators_for_range, game, name, group_id, position, control_point
        )
        if ground_object:
            return ground_object
    return None
