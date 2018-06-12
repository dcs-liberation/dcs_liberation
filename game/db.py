import typing

from dcs.vehicles import *
from dcs.unitgroup import *
from dcs.planes import *
from dcs.task import *
from dcs.unittype import *

PRICES = {
    # planes

    Su_25T: 11,
    Su_25: 11,
    A_10A: 18,
    A_10C: 20,

    F_A_18C: 18,
    AV8BNA: 15,

    Su_27: 30,
    Su_33: 33,
    F_15C: 30,
    M_2000C: 11,

    MiG_15bis: 6,
    MiG_21Bis: 13,
    MiG_29A: 23,

    IL_76MD: 13,
    S_3B_Tanker: 13,

    # armor

    Armor.MBT_T_55: 4,
    Armor.MBT_T_80U: 8,
    Armor.MBT_T_90: 10,

    Armor.MBT_M60A3_Patton: 6,
    Armor.MBT_M1A2_Abrams: 9,

    Armor.ATGM_M1134_Stryker: 6,
    Armor.APC_BTR_80: 6,

    AirDefence.AAA_ZU_23_on_Ural_375: 4,
}

UNIT_BY_TASK = {
    FighterSweep: [Su_27, Su_33, Su_25, F_15C, MiG_15bis, MiG_21Bis, MiG_29A, F_A_18C, AV8BNA],
    CAS: [Su_25T, A_10A, A_10C, ],
    CAP: [Armor.MBT_T_90, Armor.MBT_T_80U, Armor.MBT_T_55, Armor.MBT_M1A2_Abrams, Armor.MBT_M60A3_Patton, Armor.ATGM_M1134_Stryker, Armor.APC_BTR_80, ],
    AirDefence: [AirDefence.AAA_ZU_23_on_Ural_375,  ],
    Transport: [IL_76MD, S_3B_Tanker, ],
}

UNIT_BY_COUNTRY = {
    "Russia": [Su_25T, Su_27, Su_33, Su_25, MiG_15bis, MiG_21Bis, MiG_29A, AirDefence.AAA_ZU_23_on_Ural_375, Armor.APC_BTR_80, Armor.MBT_T_90, Armor.MBT_T_80U, Armor.MBT_T_55, IL_76MD, ],
    "USA": [F_15C, A_10C, F_A_18C, AV8BNA, Armor.MBT_M1A2_Abrams, Armor.MBT_M60A3_Patton, Armor.ATGM_M1134_Stryker, S_3B_Tanker],
}

UnitsDict = typing.Dict[UnitType, int]
PlaneDict = typing.Dict[PlaneType, int]
ArmorDict = typing.Dict[VehicleType, int]
AirDefenseDict = typing.Dict[AirDefence, int]
StartingPosition = typing.Optional[typing.Union[ShipGroup, Airport, Point]]


def unit_task(unit: UnitType) -> Task:
    for task, units in UNIT_BY_TASK.items():
        if unit in units:
            return task

    assert False


def find_unittype(for_task: Task, country_name: str) -> typing.List[UnitType]:
    return [x for x in UNIT_BY_TASK[for_task] if x in UNIT_BY_COUNTRY[country_name]]


def unit_type_name(unit_type) -> str:
    return unit_type.id and unit_type.id or unit_type.name


def task_name(task) -> str:
    if task == AirDefence:
        return "AirDefence"
    else:
        return task.name
