import typing
import dcs

from .controlpoint import *

from dcs.planes import *
from dcs.vehicles import *

class Base:
    aircraft = [] # type: typing.Dict[PlaneType, int]
    armor = [] # type: typing.Dict[Armor, int]
