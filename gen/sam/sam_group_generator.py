import random
from typing import List

from dcs.unittype import UnitType
from dcs.vehicles import AirDefence

from game import db
from gen.sam.aaa_bofors import BoforsGenerator
from gen.sam.aaa_flak import FlakGenerator
from gen.sam.aaa_zu23_insurgent import ZU23InsurgentGenerator
from gen.sam.sam_avenger import AvengerGenerator
from gen.sam.sam_chaparral import ChaparralGenerator
from gen.sam.sam_gepard import GepardGenerator
from gen.sam.sam_hawk import HawkGenerator
from gen.sam.sam_hq7 import HQ7Generator
from gen.sam.sam_linebacker import LinebackerGenerator
from gen.sam.sam_patriot import PatriotGenerator
from gen.sam.sam_rapier import RapierGenerator
from gen.sam.sam_roland import RolandGenerator
from gen.sam.sam_sa10 import SA10Generator
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

SAM_MAP = {
    AirDefence.SAM_Hawk_PCP: HawkGenerator,
    AirDefence.AAA_ZU_23_Emplacement: ZU23Generator,
    AirDefence.AAA_ZU_23_Closed: ZU23Generator,
    AirDefence.AAA_ZU_23_on_Ural_375: ZU23UralGenerator,
    AirDefence.AAA_ZU_23_Insurgent_on_Ural_375: ZU23UralInsurgentGenerator,
    AirDefence.AAA_ZU_23_Insurgent_Closed: ZU23InsurgentGenerator,
    AirDefence.AAA_ZU_23_Insurgent: ZU23InsurgentGenerator,
    AirDefence.SPAAA_ZSU_23_4_Shilka: ZSU23Generator,
    AirDefence.AAA_Vulcan_M163: VulcanGenerator,
    AirDefence.SAM_Linebacker_M6: LinebackerGenerator,
    AirDefence.Rapier_FSA_Launcher: RapierGenerator,
    AirDefence.SAM_Avenger_M1097: AvengerGenerator,
    AirDefence.SPAAA_Gepard: GepardGenerator,
    AirDefence.SAM_Roland_ADS: RolandGenerator,
    AirDefence.SAM_Patriot_LN_M901: PatriotGenerator,
    AirDefence.SAM_Patriot_EPP_III: PatriotGenerator,
    AirDefence.SAM_Chaparral_M48: ChaparralGenerator,
    AirDefence.AAA_Bofors_40mm: BoforsGenerator,
    AirDefence.AAA_8_8cm_Flak_36: FlakGenerator,
    AirDefence.SAM_SA_2_LN_SM_90: SA2Generator,
    AirDefence.SAM_SA_3_S_125_LN_5P73: SA3Generator,
    AirDefence.SAM_SA_6_Kub_LN_2P25: SA6Generator,
    AirDefence.SAM_SA_8_Osa_9A33: SA8Generator,
    AirDefence.SAM_SA_9_Strela_1_9P31: SA9Generator,
    AirDefence.SAM_SA_10_S_300PS_LN_5P85C: SA10Generator,
    AirDefence.SAM_SA_10_S_300PS_CP_54K6: SA10Generator,
    AirDefence.SAM_SA_11_Buk_LN_9A310M1: SA11Generator,
    AirDefence.SAM_SA_13_Strela_10M3_9A35M3: SA13Generator,
    AirDefence.SAM_SA_15_Tor_9A331: SA15Generator,
    AirDefence.SAM_SA_19_Tunguska_2S6: SA19Generator,
    AirDefence.HQ_7_Self_Propelled_LN: HQ7Generator
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


def get_faction_possible_sams_units(faction: str) -> List[UnitType]:
    """
    Return the list
    :param faction: Faction to search units for
    """
    return [u for u in db.FACTIONS[faction]["units"] if u in AirDefence.__dict__.values()]


def get_faction_possible_sams_generator(faction: str) -> List[UnitType]:
    """
    Return the list of possible SAM generator for the given faction
    :param faction: Faction to search units for
    """
    return [SAM_MAP[u] for u in get_faction_possible_sams_units(faction)]


def generate_anti_air_group(game, parent_cp, ground_object, faction:str):
    """
    This generate a SAM group
    :param parentCp: The parent control point
    :param ground_object: The ground object which will own the sam group
    :param country: Owner country
    :return: Nothing, but put the group reference inside the ground object
    """
    possible_sams = get_faction_possible_sams_units(faction)
    if len(possible_sams) > 0:
        sam = random.choice(possible_sams)
        generator = SAM_MAP[sam](game, ground_object)
        generator.generate()
        return generator.get_generated_group()
    return None


def generate_shorad_group(game, parent_cp, ground_object, faction:str):
    if("shorad") in db.FACTIONS[faction].keys():
        shorad = db.FACTIONS[faction]["shorad"]
        sam = random.choice(shorad)
        generator = SAM_MAP[sam](game, ground_object)
        generator.generate()
        return generator.get_generated_group()
    else:
        return generate_anti_air_group(game, parent_cp, ground_object, faction)







