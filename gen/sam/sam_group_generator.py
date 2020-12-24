import random
from typing import Dict, Iterable, List, Optional, Sequence, Set, Type

from dcs.unitgroup import VehicleGroup
from dcs.vehicles import AirDefence

from game import Game
from game.factions.faction import Faction
from game.theater import TheaterGroundObject
from game.theater.theatergroundobject import SamGroundObject
from gen.sam.aaa_bofors import BoforsGenerator
from gen.sam.aaa_flak import FlakGenerator
from gen.sam.aaa_flak18 import Flak18Generator
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
from gen.sam.ewrs import (
    BigBirdGenerator,
    BoxSpringGenerator,
    DogEarGenerator,
    FlatFaceGenerator,
    HawkEwrGenerator,
    PatriotEwrGenerator,
    RolandEwrGenerator,
    SnowDriftGenerator,
    StraightFlushGenerator,
    TallRackGenerator,
)
from gen.sam.freya_ewr import FreyaGenerator
from gen.sam.group_generator import GroupGenerator
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
)
from gen.sam.sam_sa11 import SA11Generator
from gen.sam.sam_sa13 import SA13Generator
from gen.sam.sam_sa15 import SA15Generator
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
    "ZSU57Generator": ZSU57Generator
}


SAM_PRICES = {
    AirDefence.SAM_Hawk_PCP: 35,
    AirDefence.AAA_ZU_23_Emplacement: 10,
    AirDefence.AAA_ZU_23_Closed: 10,
    AirDefence.AAA_ZU_23_on_Ural_375: 10,
    AirDefence.AAA_ZU_23_Insurgent_on_Ural_375: 10,
    AirDefence.AAA_ZU_23_Insurgent_Closed: 10,
    AirDefence.AAA_ZU_23_Insurgent: 10,
    AirDefence.SPAAA_ZSU_23_4_Shilka: 10,
    AirDefence.AAA_Vulcan_M163: 15,
    AirDefence.SAM_Linebacker_M6: 20,
    AirDefence.Rapier_FSA_Launcher: 20,
    AirDefence.SAM_Avenger_M1097: 22,
    AirDefence.SPAAA_Gepard: 24,
    AirDefence.SAM_Roland_ADS: 40,
    AirDefence.SAM_Patriot_LN_M901: 85,
    AirDefence.SAM_Patriot_EPP_III: 85,
    AirDefence.SAM_Chaparral_M48: 25,
    AirDefence.AAA_Bofors_40mm: 15,
    AirDefence.AAA_8_8cm_Flak_36: 15,
    AirDefence.SAM_SA_2_LN_SM_90: 30,
    AirDefence.SAM_SA_3_S_125_LN_5P73: 35,
    AirDefence.SAM_SA_6_Kub_LN_2P25: 45,
    AirDefence.SAM_SA_8_Osa_9A33: 30,
    AirDefence.SAM_SA_9_Strela_1_9P31: 25,
    AirDefence.SAM_SA_10_S_300PS_LN_5P85C: 80,
    AirDefence.SAM_SA_10_S_300PS_CP_54K6: 80,
    AirDefence.SAM_SA_11_Buk_LN_9A310M1: 60,
    AirDefence.SAM_SA_13_Strela_10M3_9A35M3: 30,
    AirDefence.SAM_SA_15_Tor_9A331: 40,
    AirDefence.SAM_SA_19_Tunguska_2S6: 35,
    AirDefence.HQ_7_Self_Propelled_LN: 35
}

EWR_MAP = {
    "BoxSpringGenerator": BoxSpringGenerator,
    "TallRackGenerator": TallRackGenerator,
    "DogEarGenerator": DogEarGenerator,
    "RolandEwrGenerator": RolandEwrGenerator,
    "FlatFaceGenerator": FlatFaceGenerator,
    "PatriotEwrGenerator": PatriotEwrGenerator,
    "BigBirdGenerator": BigBirdGenerator,
    "SnowDriftGenerator": SnowDriftGenerator,
    "StraightFlushGenerator": StraightFlushGenerator,
    "HawkEwrGenerator": HawkEwrGenerator,
}


def get_faction_possible_sams_generator(
        faction: Faction) -> List[Type[AirDefenseGroupGenerator]]:
    """
    Return the list of possible SAM generator for the given faction
    :param faction: Faction name to search units for
    """
    return [SAM_MAP[s] for s in faction.air_defenses]


def get_faction_possible_ewrs_generator(faction: Faction) -> List[Type[GroupGenerator]]:
    """
    Return the list of possible SAM generator for the given faction
    :param faction: Faction name to search units for
    """
    return [EWR_MAP[s] for s in faction.ewrs]


def _generate_anti_air_from(
        generators: Sequence[Type[AirDefenseGroupGenerator]], game: Game,
        ground_object: SamGroundObject) -> List[VehicleGroup]:
    if not generators:
        return []
    sam_generator_class = random.choice(generators)
    generator = sam_generator_class(game, ground_object)
    generator.generate()
    return list(generator.groups)


def generate_anti_air_group(
        game: Game, ground_object: SamGroundObject, faction: Faction,
        ranges: Optional[Iterable[Set[AirDefenseRange]]] = None
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
        ranges = [{
            AirDefenseRange.Long,
            AirDefenseRange.Medium,
            AirDefenseRange.Short,
        }]

    for range_options in ranges:
        generators_for_range = [g for g in generators if
                                g.range() in range_options]
        groups = _generate_anti_air_from(generators_for_range, game,
                                         ground_object)
        if groups:
            return groups
    return []


def generate_ewr_group(game: Game, ground_object: TheaterGroundObject,
                       faction: Faction) -> Optional[VehicleGroup]:
    """Generates an early warning radar group.

    :param game: The Game.
    :param ground_object: The ground object which will own the EWR group.
    :param faction: Owner faction.
    :return: The generated group, or None if one could not be generated.
    """
    generators = get_faction_possible_ewrs_generator(faction)
    if len(generators) > 0:
        generator_class = random.choice(generators)
        generator = generator_class(game, ground_object)
        generator.generate()
        return generator.get_generated_group()
    return None
