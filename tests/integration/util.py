from dcs.mission import Mission

from game import *
from game.event import *
from game.db import *

from theater.persiangulf import *
from theater import start_generator

PLAYER_COUNTRY = None
ENEMY_COUNTRY = None


def init(player_country: str, enemy_country: str, theater_klass: typing.Type[ConflictTheater]) -> typing.Tuple[Game, ConflictTheater]:
    global PLAYER_COUNTRY
    global ENEMY_COUNTRY

    PLAYER_COUNTRY = player_country
    ENEMY_COUNTRY = enemy_country

    # prerequisites
    persistency.setup("./tests/userfolder/")
    theater = theater_klass()
    start_generator.generate_inital_units(theater, ENEMY_COUNTRY, True, 1)
    start_generator.generate_groundobjects(theater)
    return Game(PLAYER_COUNTRY, ENEMY_COUNTRY, theater), theater


def autoflights_for(event: Event, country: str) -> TaskForceDict:
    result = {}
    for task in event.tasks:
        result[task] = {find_unittype(task, country)[0]: (1, 1)}
    return result


class AutodebriefType(Enum):
    EVERYONE_DEAD = 0
    PLAYER_DEAD = 1
    ENEMY_DEAD = 2


def autodebrief_for(event: Event, type: AutodebriefType) -> Debriefing:
    mission = event.operation.current_mission  # type: Mission

    countries = []
    if type == AutodebriefType.PLAYER_DEAD or type == AutodebriefType.EVERYONE_DEAD:
        countries.append(mission.country(PLAYER_COUNTRY))

    if type == AutodebriefType.ENEMY_DEAD or type == AutodebriefType.EVERYONE_DEAD:
        countries.append(mission.country(ENEMY_COUNTRY))

    dead_units = []
    for country in countries:
        for group in country.plane_group + country.vehicle_group + country.helicopter_group:
            for unit in group.units:
                dead_units.append(str(unit.name))

    return Debriefing(dead_units, [])


def event_state_save(e: Event) -> typing.Tuple[Base, Base]:
    return (copy.deepcopy(e.from_cp.base), copy.deepcopy(e.to_cp.base))


def event_state_restore(e: Event, state: typing.Tuple[Base, Base]):
    e.from_cp.base, e.to_cp.base = state[0], state[1]


def execute_autocommit(e: Event):
    state = event_state_save(e)
    e.commit(autodebrief_for(e, AutodebriefType.EVERYONE_DEAD))
    event_state_restore(e, state)

    state = event_state_save(e)
    e.commit(autodebrief_for(e, AutodebriefType.PLAYER_DEAD))
    event_state_restore(e, state)

    state = event_state_save(e)
    e.commit(autodebrief_for(e, AutodebriefType.ENEMY_DEAD))
    event_state_restore(e, state)
