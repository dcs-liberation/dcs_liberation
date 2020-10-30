'''
Briefing generation logic
'''
import os
import random
import logging
from dataclasses import dataclass
from theater.frontline import FrontLine
from typing import List, Dict, TYPE_CHECKING
from jinja2 import Environment, FileSystemLoader, select_autoescape

from dcs.mission import Mission

from .aircraft import FlightData
from .airsupportgen import AwacsInfo, TankerInfo
from .armor import JtacInfo
# from .conflictgen import Conflict
from theater import ControlPoint
from .ground_forces.combat_stance import CombatStance
from .radios import RadioFrequency
from .runways import RunwayData

if TYPE_CHECKING:
    from game import Game


@dataclass
class CommInfo:
    """Communications information for the kneeboard."""
    name: str
    freq: RadioFrequency

class FrontLineInfo:
    def __init__(self, front_line: FrontLine):
        self.front_line: FrontLine = front_line
        self.player_base: ControlPoint = front_line.control_point_a
        self.enemy_base: ControlPoint = front_line.control_point_b
        self.player_zero: bool = self.player_base.base.total_armor == 0
        self.enemy_zero: bool = self.enemy_base.base.total_armor == 0
        self.advantage: bool = self.player_base.base.total_armor > self.enemy_base.base.total_armor
        self.stance: CombatStance = self.player_base.stances[self.enemy_base.id]
    

    @property
    def _random_frontline_sentence(self) -> str:
        '''Random sentences for start of situation briefing'''
        templates = [
            f"There are combats between {self.player_base.name} and {self.enemy_base.name}. ",
            f"The war on the ground is still going on between {self.player_base.name} and {self.enemy_base.name}. ",
            f"Our ground forces in {self.player_base.name} are opposed to enemy forces based in {self.enemy_base.name}. ",
            f"Our forces from {self.player_base.name} are fighting enemies based in {self.enemy_base.name}. ",
            f"There is an active frontline between {self.player_base.name} and {self.enemy_base.name}. ",
        ]
        return random.choice(templates)
    
    @property
    def _zero_units_sentence(self) -> str:
        '''Situation description if either side has zero units on a frontline'''
        if self.player_zero:
            return ("We do not have a single vehicle available to hold our position, the situation is"
                    "critical, and we will lose ground inevitably.")
        elif self.enemy_zero:
            return ("The enemy forces have been crushed, we will be able to make significant progress"
                    f" toward {self.enemy_base.name}.")
        return None

    @property
    def _advantage_description(self) -> str:
        '''Situation description for when player has numerical advantage on the frontline'''
        if self.stance == CombatStance.AGGRESSIVE:
            return (
                "On this location, our ground forces will try to make "
                "progress against the enemy. As the enemy is outnumbered, "
                "our forces should have no issue making progress."
                )
        elif self.stance == CombatStance.ELIMINATION:
            return (
                "On this location, our ground forces will focus on the destruction of enemy"
                f"assets, before attempting to make progress toward {self.enemy_base.name}. "
                "The enemy is already outnumbered, and this maneuver might draw a final "
                "blow to their forces."
            )
        elif self.stance == CombatStance.BREAKTHROUGH:
            return (
                "On this location, our ground forces will focus on progression toward "
                f"{self.enemy_base.name}."
            )
        elif self.stance in [CombatStance.DEFENSIVE, CombatStance.AMBUSH]:
            return (
                "On this location, our ground forces will hold position. We are not expecting an enemy assault."
            )
        # TODO: Write a situation description for player RETREAT stance
        elif self.stance == CombatStance.RETREAT:
            return ''
        else:
            logging.warning('Briefing did not receive a known CombatStance')
    
    @property
    def _disadvantage_description(self):
        if self.stance == CombatStance.AGGRESSIVE:
            return (
                "On this location, our ground forces will try an audacious "
                "assault against enemies in superior numbers. The operation"
                " is risky, and the enemy might counter attack."
                )
        elif self.stance == CombatStance.ELIMINATION:
            return (
                "On this location, our ground forces will try an audacious assault against "
                "enemies in superior numbers. The operation is risky, and the enemy might "
                "counter attack.\n"
            )
        elif self.stance == CombatStance.BREAKTHROUGH:
            return (
                "On this location, our ground forces have been ordered to rush toward "
                f"{self.enemy_base.name}. Wish them luck... We are also expecting a counter attack."
            )
        elif self.stance in [CombatStance.DEFENSIVE, CombatStance.AMBUSH]:
            return (
                "On this location, our ground forces have been ordered to hold still, "
                "and defend against enemy attacks. An enemy assault might be iminent."
            )
        # TODO: Write a situation description for player RETREAT stance
        elif self.stance == CombatStance.RETREAT:
            return ''
        else:
            logging.warning('Briefing did not receive a known CombatStance')
    
    @property
    def brief(self):
        if self._zero_units_sentence:
            return self._zero_units_sentence
        situation = self._random_frontline_sentence
        if self.advantage:
            situation += self._advantage_description
        else:
            situation += self._disadvantage_description
        return situation
        
class MissionInfoGenerator:
    """Base type for generators of mission information for the player.

    Examples of subtypes include briefing generators, kneeboard generators, etc.
    """

    def __init__(self, mission: Mission) -> None:
        self.mission = mission
        self.awacs: List[AwacsInfo] = []
        self.comms: List[CommInfo] = []
        self.flights: List[FlightData] = []
        self.jtacs: List[JtacInfo] = []
        self.tankers: List[TankerInfo] = []
        self.frontlines: List[FrontLineInfo] = []

    def add_awacs(self, awacs: AwacsInfo) -> None:
        """Adds an AWACS/GCI to the mission.

        Args:
            awacs: AWACS information.
        """
        self.awacs.append(awacs)

    def add_comm(self, name: str, freq: RadioFrequency) -> None:
        """Adds communications info to the mission.

        Args:
            name: Name of the radio channel.
            freq: Frequency of the radio channel.
        """
        self.comms.append(CommInfo(name, freq))

    def add_flight(self, flight: FlightData) -> None:
        """Adds flight info to the mission.

        Args:
            flight: Flight information.
        """
        self.flights.append(flight)

    def add_jtac(self, jtac: JtacInfo) -> None:
        """Adds a JTAC to the mission.

        Args:
            jtac: JTAC information.
        """
        self.jtacs.append(jtac)

    def add_tanker(self, tanker: TankerInfo) -> None:
        """Adds a tanker to the mission.

        Args:
            tanker: Tanker information.
        """
        self.tankers.append(tanker)

    def add_frontline(self, frontline: FrontLineInfo) -> None:
        self.frontlines.append(frontline)

    def generate(self) -> None:
        """Generates the mission information."""
        raise NotImplementedError


class BriefingGenerator(MissionInfoGenerator):

    def __init__(self, mission: Mission, game: 'Game'):
        super().__init__(mission)
        # self.conflict = conflict
        self.game = game
        self.title = ""
        self.description = ""
        self.dynamic_runways: List[RunwayData] = []
        self.allied_flights_by_departure: Dict[str, List[FlightData]] = {}
        env = Environment(
            loader=FileSystemLoader('resources/briefing/templates'),
            autoescape=select_autoescape(
                disabled_extensions=('txt'),
                default_for_string=True,
                default=True,
                )
            )
        self.template = env.get_template('briefingtemplate_EN.j2')

    def add_dynamic_runway(self, runway: RunwayData) -> None:
        """Adds a dynamically generated runway to the briefing.

        Dynamic runways are any valid landing point that is a unit rather than a
        map feature. These include carriers, ships with a helipad, and FARPs.
        """
        self.dynamic_runways.append(runway)

    def generate(self):
        self._generate_frontline_info()
        self.generate_allied_flights_by_departure()
        with open('testgen.txt', 'w') as file:
            file.write(self.template.render(vars(self)))
        self.mission.set_description_text(self.template.render(vars(self)))
        self.mission.add_picture_blue(os.path.abspath(
            "./resources/ui/splash_screen.png"))

    def _generate_frontline_info(self):
        for front_line in self.game.theater.conflicts(from_player=True):
            print(front_line.name)
            self.add_frontline(FrontLineInfo(front_line))

    # TODO: This should determine if runway is friendly through a method more robust than the existing string match
    def generate_allied_flights_by_departure(self) -> None:
        for flight in self.flights:
            if not flight.client_units and flight.friendly:  # where else can we get this?
                name = flight.departure.airfield_name
                if name in self.allied_flights_by_departure.keys():
                    self.allied_flights_by_departure[name].append(flight)
                else:
                    self.allied_flights_by_departure[name] = [flight]
