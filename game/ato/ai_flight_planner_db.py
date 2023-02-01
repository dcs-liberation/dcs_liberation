import logging
from collections.abc import Sequence
from typing import Type

from dcs.helicopters import (
    AH_1W,
    AH_64A,
    AH_64D,
    AH_64D_BLK_II,
    CH_47D,
    CH_53E,
    Ka_50,
    Ka_50_3,
    Mi_24P,
    Mi_24V,
    Mi_26,
    Mi_28N,
    Mi_8MT,
    OH_58D,
    SA342L,
    SA342M,
    SH_60B,
    UH_1H,
    UH_60A,
)
from dcs.planes import (
    AJS37,
    AV8BNA,
    A_10A,
    A_10C,
    A_10C_2,
    A_20G,
    A_50,
    An_26B,
    B_17G,
    B_1B,
    B_52H,
    Bf_109K_4,
    C_101CC,
    C_130,
    C_17A,
    E_2C,
    E_3A,
    FA_18C_hornet,
    FW_190A8,
    FW_190D9,
    F_117A,
    F_14A_135_GR,
    F_14B,
    F_15C,
    F_15E,
    F_16A,
    F_16C_50,
    F_4E,
    F_5E_3,
    F_86F_Sabre,
    H_6J,
    IL_76MD,
    IL_78M,
    I_16,
    JF_17,
    J_11A,
    Ju_88A4,
    KC130,
    KC135MPRS,
    KC_135,
    KJ_2000,
    L_39ZA,
    MB_339A,
    MQ_9_Reaper,
    M_2000C,
    MiG_15bis,
    MiG_19P,
    MiG_21Bis,
    MiG_23MLD,
    MiG_25PD,
    MiG_27K,
    MiG_29A,
    MiG_29G,
    MiG_29S,
    MiG_31,
    Mirage_2000_5,
    Mirage_F1B,
    Mirage_F1BE,
    Mirage_F1CE,
    Mirage_F1CT,
    Mirage_F1C_200,
    Mirage_F1EE,
    Mirage_F1EQ,
    Mirage_F1M_CE,
    Mirage_F1M_EE,
    MosquitoFBMkVI,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    P_51D,
    P_51D_30_NA,
    RQ_1A_Predator,
    S_3B,
    S_3B_Tanker,
    SpitfireLFMkIX,
    SpitfireLFMkIXCW,
    Su_17M4,
    Su_24M,
    Su_25,
    Su_25T,
    Su_25TM,
    Su_27,
    Su_30,
    Su_33,
    Su_34,
    Tornado_GR4,
    Tornado_IDS,
    Tu_142,
    Tu_160,
    Tu_22M3,
    Tu_95MS,
    WingLoong_I,
    Yak_40,
)
from dcs.unittype import FlyingType

from game.dcs.aircrafttype import AircraftType
from pydcs_extensions.a4ec.a4ec import A_4E_C
from pydcs_extensions.f104.f104 import VSN_F104G, VSN_F104S, VSN_F104S_AG
from pydcs_extensions.f22a.f22a import F_22A
from pydcs_extensions.hercules.hercules import Hercules
from pydcs_extensions.jas39.jas39 import JAS39Gripen, JAS39Gripen_AG
from pydcs_extensions.ov10a.ov10a import Bronco_OV_10A
from pydcs_extensions.su57.su57 import Su_57
from pydcs_extensions.uh60l.uh60l import KC130J, UH_60L
from .flighttype import FlightType

# All aircraft lists are in priority order. Aircraft higher in the list will be
# preferred over those lower in the list.
# TODO: These lists really ought to be era (faction) dependent.
# Factions which have F-5s, F-86s, and A-4s will should prefer F-5s for CAP, but
# factions that also have F-4s should not.

# Used for CAP, Escort, and intercept if there is not a specialised aircraft available
CAP_CAPABLE = [
    Su_57,
    F_22A,
    F_15C,
    F_14B,
    F_14A_135_GR,
    Su_33,
    J_11A,
    Su_30,
    Su_27,
    MiG_29S,
    F_16C_50,
    FA_18C_hornet,
    JF_17,
    JAS39Gripen,
    F_16A,
    F_4E,
    MiG_31,
    MiG_25PD,
    MiG_29G,
    MiG_29A,
    MiG_23MLD,
    MiG_21Bis,
    Mirage_2000_5,
    Mirage_F1B,
    Mirage_F1BE,
    Mirage_F1CE,
    Mirage_F1EE,
    Mirage_F1EQ,
    Mirage_F1M_CE,
    Mirage_F1M_EE,
    Mirage_F1C_200,
    Mirage_F1CT,
    F_15E,
    M_2000C,
    F_5E_3,
    VSN_F104S,
    VSN_F104G,
    MiG_19P,
    A_4E_C,
    F_86F_Sabre,
    MiG_15bis,
    C_101CC,
    L_39ZA,
    P_51D_30_NA,
    P_51D,
    SpitfireLFMkIXCW,
    SpitfireLFMkIX,
    MosquitoFBMkVI,
    Bf_109K_4,
    FW_190D9,
    FW_190A8,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    I_16,
]


# Used for CAS (Close air support) and BAI (Battlefield Interdiction)
CAS_CAPABLE = [
    A_10C_2,
    A_10C,
    Hercules,
    Su_34,
    Su_25TM,
    Su_25T,
    Su_25,
    F_15E,
    F_16C_50,
    FA_18C_hornet,
    Tornado_GR4,
    Tornado_IDS,
    JAS39Gripen_AG,
    JF_17,
    AV8BNA,
    A_10A,
    B_1B,
    A_4E_C,
    Bronco_OV_10A,
    F_14B,
    F_14A_135_GR,
    AJS37,
    Su_24M,
    Su_17M4,
    Su_33,
    F_4E,
    S_3B,
    Su_30,
    MiG_29S,
    MiG_27K,
    MiG_29A,
    MiG_21Bis,
    AH_64D_BLK_II,
    AH_64D,
    AH_64A,
    AH_1W,
    OH_58D,
    SA342M,
    SA342L,
    Ka_50_3,
    Ka_50,
    Mi_28N,
    Mi_24P,
    Mi_24V,
    Mi_8MT,
    H_6J,
    MiG_19P,
    MiG_15bis,
    M_2000C,
    Mirage_F1B,
    Mirage_F1BE,
    Mirage_F1CE,
    Mirage_F1EE,
    Mirage_F1EQ,
    Mirage_F1M_CE,
    Mirage_F1M_EE,
    Mirage_F1CT,
    F_5E_3,
    F_86F_Sabre,
    MB_339A,
    C_101CC,
    L_39ZA,
    UH_1H,
    VSN_F104S_AG,
    VSN_F104G,
    A_20G,
    Ju_88A4,
    P_47D_40,
    P_47D_30bl1,
    P_47D_30,
    P_51D_30_NA,
    P_51D,
    SpitfireLFMkIXCW,
    SpitfireLFMkIX,
    MosquitoFBMkVI,
    I_16,
    Bf_109K_4,
    FW_190D9,
    FW_190A8,
    WingLoong_I,
    MQ_9_Reaper,
    RQ_1A_Predator,
]


# Aircraft used for SEAD and SEAD Escort tasks. Must be capable of the CAS DCS task.
SEAD_CAPABLE = [
    JF_17,
    F_16C_50,
    FA_18C_hornet,
    Tornado_IDS,
    Su_25T,
    Su_25TM,
    F_4E,
    A_4E_C,
    F_14B,
    F_14A_135_GR,
    JAS39Gripen_AG,
    AV8BNA,
    Su_24M,
    Su_17M4,
    Su_34,
    Su_30,
    MiG_27K,
    Tornado_GR4,
]


# Aircraft used for DEAD tasks. Must be capable of the CAS DCS task.
DEAD_CAPABLE = SEAD_CAPABLE + [
    AJS37,
    F_15E,
    F_14B,
    F_14A_135_GR,
    JAS39Gripen_AG,
    B_1B,
    B_52H,
    Tu_160,
    Tu_95MS,
    H_6J,
    A_20G,
    Ju_88A4,
    VSN_F104S_AG,
    VSN_F104G,
    P_47D_40,
    P_47D_30bl1,
    P_47D_30,
    P_51D_30_NA,
    P_51D,
    Bronco_OV_10A,
    SpitfireLFMkIXCW,
    SpitfireLFMkIX,
    MosquitoFBMkVI,
    Bf_109K_4,
    FW_190D9,
    FW_190A8,
]


# Aircraft used for Strike mission
STRIKE_CAPABLE = [
    F_117A,
    B_1B,
    B_52H,
    Tu_160,
    Tu_95MS,
    Tu_22M3,
    H_6J,
    F_15E,
    AJS37,
    Tornado_GR4,
    F_16C_50,
    FA_18C_hornet,
    AV8BNA,
    JF_17,
    F_16A,
    F_14B,
    F_14A_135_GR,
    JAS39Gripen_AG,
    Tornado_IDS,
    Su_17M4,
    Su_24M,
    Su_25TM,
    Su_25T,
    Su_25,
    Su_34,
    Su_33,
    Su_30,
    Su_27,
    MiG_29S,
    MiG_29G,
    MiG_29A,
    F_4E,
    A_10C_2,
    A_10C,
    S_3B,
    A_4E_C,
    Bronco_OV_10A,
    M_2000C,
    Mirage_F1B,
    Mirage_F1BE,
    Mirage_F1CE,
    Mirage_F1EE,
    Mirage_F1EQ,
    Mirage_F1M_CE,
    Mirage_F1M_EE,
    Mirage_F1CT,
    MiG_27K,
    MiG_21Bis,
    MiG_15bis,
    F_5E_3,
    F_86F_Sabre,
    MB_339A,
    C_101CC,
    L_39ZA,
    B_17G,
    A_20G,
    Ju_88A4,
    VSN_F104S_AG,
    VSN_F104G,
    P_47D_40,
    P_47D_30bl1,
    P_47D_30,
    P_51D_30_NA,
    P_51D,
    SpitfireLFMkIXCW,
    SpitfireLFMkIX,
    MosquitoFBMkVI,
    Bf_109K_4,
    FW_190D9,
    FW_190A8,
]


ANTISHIP_CAPABLE = [
    AJS37,
    Tu_142,
    Tu_22M3,
    H_6J,
    FA_18C_hornet,
    JAS39Gripen_AG,
    Su_24M,
    Su_17M4,
    JF_17,
    Su_34,
    Su_30,
    Tornado_IDS,
    Tornado_GR4,
    AV8BNA,
    S_3B,
    A_20G,
    Ju_88A4,
    MosquitoFBMkVI,
    C_101CC,
    SH_60B,
]


# This list does not "inherit" from the strike list because some strike aircraft can
# only carry guided weapons, and the AI cannot do runway attack with dguided weapons.
# https://github.com/dcs-liberation/dcs_liberation/issues/1703
RUNWAY_ATTACK_CAPABLE = [
    JF_17,
    Su_34,
    Su_30,
    Tornado_IDS,
    M_2000C,
    H_6J,
    B_1B,
    B_52H,
    Tu_22M3,
    H_6J,
    F_15E,
    AJS37,
    F_16C_50,
    FA_18C_hornet,
    AV8BNA,
    JF_17,
    F_16A,
    F_14B,
    F_14A_135_GR,
    JAS39Gripen_AG,
    Tornado_IDS,
    Su_17M4,
    Su_24M,
    Su_25TM,
    Su_25T,
    Su_25,
    Su_34,
    Su_33,
    Su_30,
    Su_27,
    MiG_29S,
    MiG_29G,
    MiG_29A,
    F_4E,
    A_10C_2,
    A_10C,
    S_3B,
    A_4E_C,
    Bronco_OV_10A,
    M_2000C,
    Mirage_F1B,
    Mirage_F1BE,
    Mirage_F1CE,
    Mirage_F1EE,
    Mirage_F1EQ,
    Mirage_F1M_CE,
    Mirage_F1M_EE,
    Mirage_F1CT,
    MiG_27K,
    MiG_21Bis,
    MiG_15bis,
    MB_339A,
    F_5E_3,
    F_86F_Sabre,
    C_101CC,
    L_39ZA,
    B_17G,
    A_20G,
    Ju_88A4,
    VSN_F104S_AG,
    VSN_F104G,
    P_47D_40,
    P_47D_30bl1,
    P_47D_30,
    P_51D_30_NA,
    P_51D,
    SpitfireLFMkIXCW,
    SpitfireLFMkIX,
    MosquitoFBMkVI,
    Bf_109K_4,
    FW_190D9,
    FW_190A8,
]

# For any aircraft that isn't necessarily directly involved in strike
# missions in a direct combat sense, but can transport objects and infantry.
TRANSPORT_CAPABLE = [
    C_17A,
    Hercules,
    C_130,
    IL_76MD,
    An_26B,
    Yak_40,
    CH_53E,
    CH_47D,
    UH_60L,
    SH_60B,
    UH_60A,
    UH_1H,
    Mi_8MT,
    Mi_8MT,
    Mi_26,
]

AIR_ASSAULT_CAPABLE = [
    CH_53E,
    CH_47D,
    UH_60L,
    SH_60B,
    UH_60A,
    UH_1H,
    Mi_8MT,
    Mi_26,
    Mi_24P,
    Mi_24V,
    Hercules,
]

DRONES = [MQ_9_Reaper, RQ_1A_Predator, WingLoong_I]

AEWC_CAPABLE = [
    E_3A,
    E_2C,
    A_50,
    KJ_2000,
]

# Priority is given to the tankers that can carry the most fuel.
REFUELING_CAPABALE = [
    KC_135,
    KC135MPRS,
    IL_78M,
    KC130J,
    KC130,
    S_3B_Tanker,
]


def dcs_types_for_task(task: FlightType) -> Sequence[Type[FlyingType]]:
    cap_missions = (
        FlightType.BARCAP,
        FlightType.INTERCEPTION,
        FlightType.SWEEP,
        FlightType.TARCAP,
    )
    if task in cap_missions:
        return CAP_CAPABLE
    elif task == FlightType.ANTISHIP:
        return ANTISHIP_CAPABLE
    elif task == FlightType.BAI:
        return CAS_CAPABLE
    elif task == FlightType.CAS:
        return CAS_CAPABLE
    elif task == FlightType.SEAD:
        return SEAD_CAPABLE
    elif task == FlightType.SEAD_ESCORT:
        return SEAD_CAPABLE
    elif task == FlightType.DEAD:
        return DEAD_CAPABLE
    elif task == FlightType.OCA_AIRCRAFT:
        return CAS_CAPABLE
    elif task == FlightType.OCA_RUNWAY:
        return RUNWAY_ATTACK_CAPABLE
    elif task == FlightType.STRIKE:
        return STRIKE_CAPABLE
    elif task == FlightType.ESCORT:
        return CAP_CAPABLE
    elif task == FlightType.AEWC:
        return AEWC_CAPABLE
    elif task == FlightType.REFUELING:
        return REFUELING_CAPABALE
    elif task == FlightType.TRANSPORT:
        return TRANSPORT_CAPABLE
    elif task == FlightType.AIR_ASSAULT:
        return AIR_ASSAULT_CAPABLE
    else:
        logging.error(f"Unplannable flight type: {task}")
        return []


def aircraft_for_task(task: FlightType) -> list[AircraftType]:
    dcs_types = dcs_types_for_task(task)
    types: list[AircraftType] = []
    for dcs_type in dcs_types:
        types.extend(AircraftType.for_dcs_type(dcs_type))
    return types


def tasks_for_aircraft(aircraft: AircraftType) -> list[FlightType]:
    tasks: list[FlightType] = []
    for task in FlightType:
        if task is FlightType.FERRY:
            # Not a plannable task, so skip it.
            continue
        if aircraft in aircraft_for_task(task):
            tasks.append(task)
    return tasks
