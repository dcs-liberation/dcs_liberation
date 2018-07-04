import typing

from dcs.vehicles import *
from dcs.unitgroup import *
from dcs.ships import *
from dcs.planes import *
from dcs.helicopters import *
from dcs.task import *
from dcs.unittype import *

"""
---------- BEGINNING OF CONFIGURATION SECTION
"""

"""
All aircraft names in this file should correspond with naming provided in following files:

* https://github.com/pydcs/dcs/blob/master/dcs/planes.py - for planes
* https://github.com/pydcs/dcs/blob/master/dcs/helicopters.py - for helicopters
* https://github.com/pydcs/dcs/blob/master/dcs/vehicles.py - for vehicles (this include all of the ground vehicles)

You can find names at the bottom of the file in following format:

x_map = {
    "Name of the unit in game": Identifier,
}

from this example `Identifier` should be used (which may or may not include category of the unit and dot + underscore characters).
For example, player accessible Hornet is called `FA_18C_hornet`, and MANPAD Igla is called `AirDefence.SAM_SA_18_Igla_S_MANPADS`
"""

"""
Prices for the aircraft. 
This defines both price for the player (although only aircraft listed in CAP/CAS/Transport/Armor/AirDefense roles will be purchasable) 
and prioritization for the enemy (i.e. less important bases will receive units with lower price)
"""
PRICES = {
    # fighter
    C_101CC: 8,
    MiG_23MLD: 20,
    Su_27: 24,
    Su_33: 25,
    MiG_29A: 22,
    MiG_29S: 26,

    F_5E_3: 6,
    MiG_15bis: 5,
    MiG_21Bis: 6,
    AJS37: 8,

    AV8BNA: 13,
    M_2000C: 13,
    FA_18C_hornet: 18,
    F_15C: 24,

    # bomber
    Su_25: 15,
    Su_25T: 13,
    L_39ZA: 10,
    Su_34: 18,

    A_10A: 18,
    A_10C: 20,

    # heli
    Ka_50: 13,
    UH_1H: 5,
    Mi_8MT: 5,

    # special
    IL_76MD: 13,
    An_26B: 13,
    An_30M: 13,
    Yak_40: 13,
    S_3B_Tanker: 13,

    A_50: 8,
    E_3A: 8,
    C_130: 8,

    # armor
    Armor.MBT_T_55: 4,
    Armor.MBT_T_80U: 8,
    Armor.MBT_T_90: 10,

    Armor.MBT_M60A3_Patton: 6,
    Armor.MBT_M1A2_Abrams: 9,

    Armor.ATGM_M1134_Stryker: 6,
    Armor.APC_BTR_80: 6,

    Unarmed.Transport_UAZ_469: 3,
    Unarmed.Transport_Ural_375: 3,
    Infantry.Infantry_M4: 1,
    Infantry.Soldier_AK: 1,

    Unarmed.Transport_M818: 3,

    AirDefence.AAA_Vulcan_M163: 5,
    AirDefence.SAM_Avenger_M1097: 10,
    AirDefence.SAM_Patriot_ICC: 15,

    AirDefence.AAA_ZU_23_on_Ural_375: 5,
    AirDefence.SAM_SA_18_Igla_S_MANPADS: 8,
    AirDefence.SAM_SA_19_Tunguska_2S6: 15,
    AirDefence.SAM_SA_8_Osa_9A33: 13,

    # ship
    CV_1143_5_Admiral_Kuznetsov: 100,
    CVN_74_John_C__Stennis: 100,

    LHA_1_Tarawa: 30,
    Bulk_cargo_ship_Yakushev: 10,
    Dry_cargo_ship_Ivanov: 10,
    Tanker_Elnya_160: 10,
}

"""
Units separated by tasks. This will include units for both countries. Be advised that unit could only belong to single task!

Following tasks are present:
* CAP - figther aircraft for CAP/Escort/Intercept
* CAS - CAS aircraft
* Transport - transport aircraft (used as targets in intercept operations)
* AWACS - awacs
* PinpointStrike - armor that will engage in ground war
* AirDefense - AA units
* Reconnaissance - units that will be used as targets in destroy insurgents operations
* Nothing - troops that will be used for helicopter transport operations
* Embarking - helicopters that will be used for helicopter transport operations
* Carriage - aircraft carriers
* CargoTransportation - ships that will be used as targets for ship intercept operations
"""
UNIT_BY_TASK = {
    CAP: [
        C_101CC,
        AJS37,
        F_5E_3,
        Su_27,
        Su_33,
        MiG_21Bis,
        MiG_29A,
        MiG_29S,
        FA_18C_hornet,
        F_15C,
        M_2000C,
    ],
    CAS: [
        MiG_15bis,
        L_39ZA,
        AV8BNA,
        A_10A,
        A_10C,
        Su_25,
        Su_25T,
        Su_34,
        Ka_50,
    ],

    Transport: [
        IL_76MD,
        An_26B,
        An_30M,
        Yak_40,

        S_3B_Tanker,
        C_130,
    ],

    AWACS: [E_3A, A_50, ],

    PinpointStrike: [Armor.MBT_T_90, Armor.MBT_T_80U, Armor.MBT_T_55, Armor.MBT_M1A2_Abrams, Armor.MBT_M60A3_Patton, Armor.ATGM_M1134_Stryker, Armor.APC_BTR_80, ],
    AirDefence: [
        # those are listed multiple times here to balance prioritization more into lower tier AAs
        AirDefence.AAA_Vulcan_M163,
        AirDefence.AAA_Vulcan_M163,
        AirDefence.SAM_Avenger_M1097,
        AirDefence.SAM_Avenger_M1097,
        AirDefence.SAM_Avenger_M1097,
        AirDefence.SAM_Patriot_ICC,

        AirDefence.AAA_ZU_23_on_Ural_375,
        AirDefence.AAA_ZU_23_on_Ural_375,
        AirDefence.AAA_ZU_23_on_Ural_375,
        AirDefence.SAM_SA_8_Osa_9A33,
        AirDefence.SAM_SA_8_Osa_9A33,
        AirDefence.SAM_SA_19_Tunguska_2S6,
    ],

    Reconnaissance: [Unarmed.Transport_M818, Unarmed.Transport_Ural_375, Unarmed.Transport_UAZ_469],
    Nothing: [Infantry.Infantry_M4, Infantry.Soldier_AK, ],
    Embarking: [UH_1H, Mi_8MT, ],

    Carriage: [CVN_74_John_C__Stennis, CV_1143_5_Admiral_Kuznetsov, ],
    CargoTransportation: [Dry_cargo_ship_Ivanov, Bulk_cargo_ship_Yakushev, Tanker_Elnya_160, LHA_1_Tarawa],
}

"""
Units from AirDefense category of UNIT_BY_TASK that will be removed from use if "No SAM" option is checked at the start of the game
"""
SAM_BAN = [
    AirDefence.SAM_Avenger_M1097,
    AirDefence.SAM_Patriot_ICC,

    AirDefence.SAM_SA_19_Tunguska_2S6,
    AirDefence.SAM_SA_8_Osa_9A33,
]

"""
Units that will always be spawned in the air
"""
TAKEOFF_BAN = [
    AV8BNA,  # AI takeoff currently bugged attempting VTOL with no regards for the total weight
]

"""
Units that will be always spawned in the air if launched from the carrier
"""
CARRIER_TAKEOFF_BAN = [
   Su_33,  # Kuznecow is bugged in a way that only 2 aircraft could be spawned
]

"""
AirDefense units that will be spawned at control points not related to the current operation
"""
EXTRA_AA = {
    "Russia": AirDefence.SAM_SA_9_Strela_1_9P31,
    "USA": AirDefence.SAM_Patriot_EPP_III,
}

"""
Units separated by country. Currently only Russia and USA are supported. 
Be advised that putting unit to the country that have not access to the unit in the game itself will result in incorrect missions generated!
"""
UNIT_BY_COUNTRY = {
    "Russia": [
        C_101CC,
        AJS37,
        F_5E_3,
        Su_25,
        Su_27,
        Su_33,
        MiG_15bis,
        MiG_21Bis,
        MiG_29A,
        MiG_29S,
        M_2000C,

        Su_25T,
        Su_34,
        L_39ZA,

        IL_76MD,
        An_26B,
        An_30M,
        Yak_40,
        A_50,

        Ka_50,
        UH_1H,
        Mi_8MT,

        AirDefence.AAA_ZU_23_on_Ural_375,
        AirDefence.SAM_SA_18_Igla_S_MANPADS,
        AirDefence.SAM_SA_8_Osa_9A33,
        AirDefence.SAM_SA_19_Tunguska_2S6,

        Armor.APC_BTR_80,
        Armor.MBT_T_90,
        Armor.MBT_T_80U,
        Armor.MBT_T_55,
        Unarmed.Transport_Ural_375,
        Unarmed.Transport_UAZ_469,
        Infantry.Soldier_AK,
        CV_1143_5_Admiral_Kuznetsov,
        Bulk_cargo_ship_Yakushev,
        Dry_cargo_ship_Ivanov,
        Tanker_Elnya_160,
    ],

    "USA": [
        F_15C,
        FA_18C_hornet,
        AJS37,
        M_2000C,
        MiG_21Bis,
        MiG_15bis,

        A_10A,
        A_10C,
        AV8BNA,

        S_3B_Tanker,
        C_130,
        E_3A,

        Ka_50,
        UH_1H,
        Mi_8MT,

        Armor.MBT_M1A2_Abrams,
        Armor.MBT_M60A3_Patton,
        Armor.ATGM_M1134_Stryker,
        Unarmed.Transport_M818,
        Infantry.Infantry_M4,

        AirDefence.AAA_Vulcan_M163,
        AirDefence.SAM_Avenger_M1097,
        AirDefence.SAM_Patriot_ICC,

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
    ],
}

"""
Aircraft payload overrides. Usually default loadout for the task is loaded during the mission generation.
Syntax goes as follows:

    `AircraftIdentifier`: {
        "Category": "PayloadName",
    },

where:
    * `AircraftIdentifier`: identifier of aircraft (the same that is used troughout the file)
    * "Category": (in double quotes) is one of the tasks: CAS, CAP, Intercept, Escort or "*"
    * "PayloadName": payload as found in resources/payloads/UNIT_TYPE.lua file. Sometimes this will match payload names 
                     in the mission editor, sometimes it doesn't
                     
Payload will be used for operation of following type, "*" category will be used always, no matter the operation.
"""
PLANE_PAYLOAD_OVERRIDES = {
    FA_18C_hornet: {
        "*": "AIM-9M*6, AIM-7M*2, FUEL*3",
    },

    Su_33: {
        "*": "R-73*4,R-27R*2,R-27ER*6",
    },

    AV8BNA: {
        CAS: "AS 2",
    },

    A_10C: {
        CAS: "AGM-65D*2,AGM-65H*2,GBU-12*2,GBU-38*2,AIM-9*2,TGP,ECM,MK151*7",
    },

    Ka_50: {
      "*": "12x9A4172, 40xS-8",
    },

    M_2000C: {
        "*": "Combat Air Patrol",
    },

    MiG_21Bis: {
        "*": "Patrol, medium range",
    }
}

"""
Aircraft livery overrides. Syntax as follows:

    `Identifier`: "LiveryName",

`Identifier` is aircraft identifier (as used troughout the file) and "LiveryName" (with double quotes) 
is livery name as found in mission editor.
"""
PLANE_LIVERY_OVERRIDES = {
    FA_18C_hornet: "VFA-34",  # default livery for the hornet is blue angels one
}

"""
---------- END OF CONFIGURATION SECTION
"""

UnitsDict = typing.Dict[UnitType, int]
PlaneDict = typing.Dict[FlyingType, int]
HeliDict = typing.Dict[HelicopterType, int]
ArmorDict = typing.Dict[VehicleType, int]
ShipDict = typing.Dict[ShipType, int]
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
    elif task == Embarking:
        return "Transportation"
    else:
        return task.name


def choose_units(for_task: Task, factor: float, count: int, country: str) -> typing.Collection[UnitType]:
    suitable_unittypes = find_unittype(for_task, country)
    suitable_unittypes.sort(key=lambda x: PRICES[x])

    idx = int(len(suitable_unittypes) * factor)
    variety = int(count + count * factor / 2)

    index_start = min(idx, len(suitable_unittypes) - variety)
    index_end = min(idx + variety, len(suitable_unittypes))
    return list(set(suitable_unittypes[index_start:index_end]))


def _validate_db():
    # check unit by task uniquity
    total_set = set()
    for t, unit_collection in UNIT_BY_TASK.items():
        for unit_type in set(unit_collection):
            assert unit_type not in total_set, "{} is duplicate".format(unit_type)
            total_set.add(unit_type)

    # check country allegiance
    for unit_type in total_set:
        did_find = False
        for country_units_list in UNIT_BY_COUNTRY.values():
            if unit_type in country_units_list:
                did_find = True
        assert did_find, "{} not in country list".format(unit_type)

    # check prices
    for unit_type in total_set:
        assert unit_type in PRICES, "{} not in prices".format(unit_type)


_validate_db()
