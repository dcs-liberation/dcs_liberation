import os
import random
from dataclasses import dataclass
from typing import List, Dict, TYPE_CHECKING
from jinja2 import Environment, FileSystemLoader, select_autoescape

from dcs.mission import Mission

from .aircraft import FlightData
from .airsupportgen import AwacsInfo, TankerInfo
from .armor import JtacInfo
from .conflictgen import Conflict
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


@dataclass
class BriefingInfo:
    description: str


@dataclass
class FrontLineInfo(BriefingInfo):
    enemy_base: str
    player_base: str


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

    def __init__(self, mission: Mission, conflict: Conflict, game: 'Game'):
        super().__init__(mission)
        self.conflict = conflict
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
        self.generate_ongoing_war_text()
        self.generate_allied_flights_by_departure()
        self.mission.set_description_text(self.template.render(vars(self)))
        ## TODO: Remove debug code
        with open(r'C:\Users\walte\Documents\briefing.txt', 'w') as file:
            file.write(self.template.render(vars(self)))
        self.mission.add_picture_blue(os.path.abspath(
            "./resources/ui/splash_screen.png"))

    def __random_frontline_sentence(self, player_base_name, enemy_base_name):
        templates = [
            "There are combats between {} and {}. ",
            "The war on the ground is still going on between {} and {}. ",
            "Our ground forces in {} are opposed to enemy forces based in {}. ",
            "Our forces from {} are fighting enemies based in {}. ",
            "There is an active frontline between {} and {}. ",
        ]
        return random.choice(templates).format(player_base_name, enemy_base_name)

    # TODO: refactor this, perhaps move to FrontLineInfo factory object? 
    def generate_ongoing_war_text(self):
        for front_line in self.game.theater.conflicts(from_player=True):
            player_base = front_line.control_point_a
            enemy_base = front_line.control_point_b
            has_numerical_superiority = player_base.base.total_armor > enemy_base.base.total_armor
            description = self.__random_frontline_sentence(player_base.name, enemy_base.name)
            stance = player_base.stances[enemy_base.id]  ## Sometimes this contains enum value, sometimes it contains int.
            if player_base.base.total_armor == 0:
                player_zero = True
                description += "We do not have a single vehicle available to hold our position, the situation is critical, and we will lose ground inevitably.\n"
            elif enemy_base.base.total_armor == 0:
                player_zero = False
                description += "The enemy forces have been crushed, we will be able to make significant progress toward " + enemy_base.name + ". \n"
            else: player_zero = False
            if not player_zero:
                if stance == CombatStance.AGGRESSIVE:
                    if has_numerical_superiority:
                        description += "On this location, our ground forces will try to make progress against the enemy"
                        description += ". As the enemy is outnumbered, our forces should have no issue making progress.\n"
                    else:
                        description += "On this location, our ground forces will try an audacious assault against enemies in superior numbers. The operation is risky, and the enemy might counter attack.\n"
                elif stance == CombatStance.ELIMINATION:
                    if has_numerical_superiority:
                        description += "On this location, our ground forces will focus on the destruction of enemy assets, before attempting to make progress toward " + enemy_base.name + ". "
                        description += "The enemy is already outnumbered, and this maneuver might draw a final blow to their forces.\n"
                    else:
                        description += "On this location, our ground forces will try an audacious assault against enemies in superior numbers. The operation is risky, and the enemy might counter attack.\n"
                elif stance == CombatStance.BREAKTHROUGH:
                    if has_numerical_superiority:
                        description += "On this location, our ground forces will focus on progression toward " + enemy_base.name + ".\n"
                    else:
                        description += "On this location, our ground forces have been ordered to rush toward " + enemy_base.name + ". Wish them luck... We are also expecting a counter attack.\n"
                elif stance in [CombatStance.DEFENSIVE, CombatStance.AMBUSH]:
                    if has_numerical_superiority:
                        description += "On this location, our ground forces will hold position. We are not expecting an enemy assault.\n"
                    else:
                        description += "On this location, our ground forces have been ordered to hold still, and defend against enemy attacks. An enemy assault might be iminent.\n"
            self.add_frontline(FrontLineInfo(description, enemy_base, player_base))
    
    # TODO: This should determine if runway is friendly through a method more robust than the existing string match
    def generate_allied_flights_by_departure(self) -> None:
        for flight in self.flights:
            if not flight.client_units and flight.friendly: ## where else can we get this?
                name = flight.departure.airfield_name
                if name in self.allied_flights_by_departure.keys():  
                    self.allied_flights_by_departure[name].append(flight) 
                else:
                    self.allied_flights_by_departure[name] = [flight]


