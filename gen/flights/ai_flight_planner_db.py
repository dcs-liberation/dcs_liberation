import logging
from typing import List, Type

from dcs.helicopters import (
    AH_1W,
    AH_64A,
    AH_64D,
    Ka_50,
    Mi_24V,
    Mi_28N,
    Mi_8MT,
    OH_58D,
    SA342L,
    SA342M,
    UH_1H,
)
from dcs.planes import (
    AJS37,
    AV8BNA,
    A_10A,
    A_10C,
    A_10C_2,
    A_20G,
    B_17G,
    B_1B,
    B_52H,
    Bf_109K_4,
    C_101CC,
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
    JF_17,
    J_11A,
    Ju_88A4,
    L_39ZA,
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
    MiG_29K,
    MiG_29S,
    MiG_31,
    Mirage_2000_5,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    P_51D,
    P_51D_30_NA,
    RQ_1A_Predator,
    SpitfireLFMkIX,
    SpitfireLFMkIXCW,
    Su_17M4,
    Su_24M,
    Su_24MR,
    Su_25,
    Su_25T,
    Su_25TM,
    Su_27,
    Su_30,
    Su_33,
    Su_34,
    Tornado_GR4,
    Tornado_IDS,
    Tu_160,
    Tu_22M3,
    Tu_95MS,
    WingLoong_I,
    I_16
)
from dcs.unittype import FlyingType

from gen.flights.flight import FlightType

from pydcs_extensions.a4ec.a4ec import A_4E_C
from pydcs_extensions.f22a.f22a import F_22A
from pydcs_extensions.mb339.mb339 import MB_339PAN
from pydcs_extensions.rafale.rafale import Rafale_A_S, Rafale_M, Rafale_B
from pydcs_extensions.su57.su57 import Su_57

# All aircraft lists are in priority order. Aircraft higher in the list will be
# preferred over those lower in the list.

# TODO: These lists really ought to be era (faction) dependent.
# Factions which have F-5s, F-86s, and A-4s will should prefer F-5s for CAP, but
# factions that also have F-4s should not.

# Used for CAP, Escort, and intercept if there is not a specialised aircraft available
CAP_CAPABLE = [
    Su_57,
    F_22A,
    MiG_31,
    F_14B,
    F_14A_135_GR,
    MiG_25PD,
    Rafale_M,
    Su_33,
    Su_30,
    Su_27,
    J_11A,
    F_15C,
    MiG_29S,
    MiG_29K,
    MiG_29G,
    MiG_29A,
    F_16C_50,
    FA_18C_hornet,
    F_15E,
    F_16A,
    F_4E,
    JF_17,
    MiG_23MLD,
    MiG_21Bis,
    Mirage_2000_5,
    M_2000C,
    F_5E_3,
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
    Su_25TM,
    Su_25T,
    Su_25,
    F_15E,
    F_16C_50,
    FA_18C_hornet,
    Rafale_A_S,
    Rafale_B,
    Tornado_GR4,
    Tornado_IDS,
    JF_17,
    A_10A,
    A_4E_C,
    AJS37,
    Su_24MR,
    Su_24M,
    Su_17M4,
    AV8BNA,
    Su_34,
    Su_30,
    MiG_29S,
    MiG_27K,
    MiG_29A,
    AH_64D,
    AH_64A,
    AH_1W,
    OH_58D,
    SA342M,
    SA342L,
    Ka_50,
    Mi_28N,
    Mi_24V,
    Mi_8MT,
    UH_1H,
    MiG_15bis,
    M_2000C,
    F_5E_3,
    F_86F_Sabre,
    C_101CC,
    MB_339PAN,
    L_39ZA,
    A_20G,
    P_47D_40,
    P_47D_30bl1,
    P_47D_30,
    P_51D_30_NA,
    P_51D,
    SpitfireLFMkIXCW,
    SpitfireLFMkIX,
    I_16,
    Bf_109K_4,
    FW_190D9,
    FW_190A8,
    WingLoong_I,
    MQ_9_Reaper,
    RQ_1A_Predator,
]


# Aircraft used for SEAD / DEAD tasks
SEAD_CAPABLE = [
    JF_17,
    F_16C_50,
    FA_18C_hornet,
    Tornado_IDS,
    Su_25T,
    Su_25TM,
    Rafale_A_S,
    Rafale_B,
    F_4E,
    A_4E_C,
    AV8BNA,
    Su_24M,
    Su_17M4,
    Su_34,
    Su_30,
    MiG_27K,
    Tornado_GR4,
]


# Aircraft used for Strike mission
STRIKE_CAPABLE = [
    F_117A,
    B_1B,
    B_52H,
    Tu_160,
    Tu_95MS,
    Tu_22M3,
    F_15E,
    AJS37,
    Rafale_A_S,
    Rafale_B,
    Tornado_GR4,
    F_16C_50,
    FA_18C_hornet,
    F_16A,
    F_14B,
    F_14A_135_GR,
    Tornado_IDS,
    Su_17M4,
    Su_24MR,
    Su_24M,
    Su_25TM,
    Su_25T,
    Su_25,
    Su_34,
    Su_33,
    Su_30,
    Su_27,
    MiG_29S,
    MiG_29K,
    MiG_29G,
    MiG_29A,
    JF_17,
    A_10C_2,
    A_10C,
    AV8BNA,
    A_4E_C,
    M_2000C,
    MiG_27K,
    MiG_21Bis,
    MiG_15bis,
    F_5E_3,
    F_86F_Sabre,
    MB_339PAN,
    C_101CC,
    L_39ZA,
    B_17G,
    A_20G,
    P_47D_40,
    P_47D_30bl1,
    P_47D_30,
    P_51D_30_NA,
    P_51D,
    SpitfireLFMkIXCW,
    SpitfireLFMkIX,
    Bf_109K_4,
    FW_190D9,
    FW_190A8,
]


ANTISHIP_CAPABLE = [
    AJS37,
    Tu_22M3,
    FA_18C_hornet,
    Rafale_A_S,
    Rafale_B,
    Su_24M,
    Su_17M4,
    JF_17,
    Su_34,
    Su_30,
    Tornado_IDS,
    Tornado_GR4,
    AV8BNA,
    Ju_88A4,
    C_101CC,
]


# Duplicates some list entries but that's fine.
RUNWAY_ATTACK_CAPABLE = [
    JF_17,
    Su_34,
    Su_30,
    Tornado_IDS,
] + STRIKE_CAPABLE


DRONES = [
    MQ_9_Reaper,
    RQ_1A_Predator,
    WingLoong_I
]


def aircraft_for_task(task: FlightType) -> List[Type[FlyingType]]:
    cap_missions = (FlightType.BARCAP, FlightType.TARCAP)
    if task in cap_missions:
        return CAP_CAPABLE
    elif task == FlightType.ANTISHIP:
        return ANTISHIP_CAPABLE
    elif task == FlightType.BAI:
        return CAS_CAPABLE
    elif task == FlightType.CAS:
        return CAS_CAPABLE
    elif task in (FlightType.DEAD, FlightType.SEAD):
        return SEAD_CAPABLE
    elif task == FlightType.OCA_AIRCRAFT:
        return CAS_CAPABLE
    elif task == FlightType.OCA_RUNWAY:
        return RUNWAY_ATTACK_CAPABLE
    elif task == FlightType.STRIKE:
        return STRIKE_CAPABLE
    elif task == FlightType.ESCORT:
        return CAP_CAPABLE
    else:
        logging.error(f"Unplannable flight type: {task}")
        return []
