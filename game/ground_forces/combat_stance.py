from enum import Enum


class CombatStance(Enum):
    DEFENSIVE = 0  # Unit will adopt defensive stance with medium group of units
    AGGRESSIVE = (
        1  # Unit will attempt to make progress with medium sized group of units
    )
    RETREAT = 2  # Unit will retreat
    BREAKTHROUGH = 3  # Unit will attempt a breakthrough, rushing forward very aggresively with big group of armored units, and even less armored units will move aggresively
    ELIMINATION = 4  # Unit will progress aggresively toward anemy units, attempting to eliminate the ennemy force
    AMBUSH = 5  # Units will adopt a defensive stance a bit different from 'DEFENSIVE', ATGM & INFANTRY with RPG will be located on frontline with the armored units. (The groups of units will be smaller)
