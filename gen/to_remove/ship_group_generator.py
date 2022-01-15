from __future__ import annotations

import logging
import random
from typing import TYPE_CHECKING, Optional

from dcs.unitgroup import ShipGroup

from game import db
from game.theater.theatergroundobject import (
    LhaGroundObject,
    CarrierGroundObject,
    ShipGroundObject,
)
from gen.to_remove.carrier_group import CarrierGroupGenerator
from gen.to_remove.cn_dd_group import ChineseNavyGroupGenerator, Type54GroupGenerator
from gen.to_remove.dd_group import (
    ArleighBurkeGroupGenerator,
    OliverHazardPerryGroupGenerator,
)
from gen.to_remove.lacombattanteII import LaCombattanteIIGroupGenerator
from gen.to_remove.lha_group import LHAGroupGenerator
from gen.to_remove.ru_dd_group import (
    RussianNavyGroupGenerator,
    GrishaGroupGenerator,
    MolniyaGroupGenerator,
    KiloSubGroupGenerator,
    TangoSubGroupGenerator,
)
from gen.to_remove.schnellboot import SchnellbootGroupGenerator
from gen.to_remove.uboat import UBoatGroupGenerator
from gen.to_remove.ww2lst import WW2LSTGroupGenerator

if TYPE_CHECKING:
    from game import Game


SHIP_MAP = {
    "SchnellbootGroupGenerator": SchnellbootGroupGenerator,
    "WW2LSTGroupGenerator": WW2LSTGroupGenerator,
    "UBoatGroupGenerator": UBoatGroupGenerator,
    "OliverHazardPerryGroupGenerator": OliverHazardPerryGroupGenerator,
    "ArleighBurkeGroupGenerator": ArleighBurkeGroupGenerator,
    "RussianNavyGroupGenerator": RussianNavyGroupGenerator,
    "ChineseNavyGroupGenerator": ChineseNavyGroupGenerator,
    "GrishaGroupGenerator": GrishaGroupGenerator,
    "MolniyaGroupGenerator": MolniyaGroupGenerator,
    "KiloSubGroupGenerator": KiloSubGroupGenerator,
    "TangoSubGroupGenerator": TangoSubGroupGenerator,
    "Type54GroupGenerator": Type54GroupGenerator,
    "LaCombattanteIIGroupGenerator": LaCombattanteIIGroupGenerator,
}
