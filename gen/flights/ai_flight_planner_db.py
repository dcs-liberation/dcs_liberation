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

# Interceptor are the aircraft prioritized for interception tasks
# If none is available, the AI will use regular CAP-capable aircraft instead
from pydcs_extensions.a4ec.a4ec import A_4E_C
from pydcs_extensions.mb339.mb339 import MB_339PAN
from pydcs_extensions.rafale.rafale import Rafale_A_S, Rafale_M

# TODO: These lists really ought to be era (faction) dependent.
# Factions which have F-5s, F-86s, and A-4s will should prefer F-5s for CAP, but
# factions that also have F-4s should not.
from pydcs_extensions.su57.su57 import Su_57

INTERCEPT_CAPABLE = [
    MiG_21Bis,
    MiG_25PD,
    MiG_31,
    MiG_29S,
    MiG_29A,
    MiG_29G,
    MiG_29K,
    JF_17,
    J_11A,
    Su_27,
    Su_30,
    Su_33,
    M_2000C,
    Mirage_2000_5,
    Rafale_M,

    F_14A_135_GR,
    F_14B,
    F_15C,
    F_16A,
    F_16C_50,
    FA_18C_hornet,

]

# Used for CAP, Escort, and intercept if there is not a specialised aircraft available
CAP_CAPABLE = [

    MiG_15bis,
    MiG_19P,
    MiG_21Bis,
    MiG_23MLD,
    MiG_25PD,
    MiG_29A,
    MiG_29G,
    MiG_29S,
    MiG_31,

    Su_27,
    J_11A,
    JF_17,
    Su_30,
    Su_33,
    Su_57,

    M_2000C,
    Mirage_2000_5,

    F_86F_Sabre,
    F_4E,
    F_5E_3,
    F_14A_135_GR,
    F_14B,
    F_15C,
    F_15E,
    F_16A,
    F_16C_50,
    FA_18C_hornet,

    C_101CC,
    L_39ZA,

    P_51D_30_NA,
    P_51D,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,

    I_16,

    SpitfireLFMkIXCW,
    SpitfireLFMkIX,

    Bf_109K_4,
    FW_190D9,
    FW_190A8,

    A_4E_C,
    Rafale_M,
]

CAP_PREFERRED = [
    MiG_15bis,
    MiG_19P,
    MiG_21Bis,
    MiG_23MLD,
    MiG_29A,
    MiG_29G,
    MiG_29S,

    Su_27,
    J_11A,
    JF_17,
    Su_30,
    Su_33,
    Su_57,

    M_2000C,
    Mirage_2000_5,

    F_86F_Sabre,
    F_14A_135_GR,
    F_14B,
    F_15C,
    F_16C_50,

    P_51D_30_NA,
    P_51D,

    SpitfireLFMkIXCW,
    SpitfireLFMkIX,

    I_16,

    Bf_109K_4,
    FW_190D9,
    FW_190A8,

    Rafale_M,
]

# Used for CAS (Close air support) and BAI (Battlefield Interdiction)
CAS_CAPABLE = [

    MiG_15bis,
    MiG_29A,
    MiG_27K,
    MiG_29S,

    Su_17M4,
    Su_24M,
    Su_24MR,
    Su_25,
    Su_25T,
    Su_25TM,
    Su_30,
    Su_34,

    JF_17,

    M_2000C,

    A_10A,
    A_10C,
    A_10C_2,
    AV8BNA,

    F_86F_Sabre,
    F_5E_3,

    F_16C_50,
    FA_18C_hornet,
    F_15E,

    Tornado_IDS,
    Tornado_GR4,

    C_101CC,
    MB_339PAN,
    L_39ZA,
    AJS37,

    SA342M,
    SA342L,
    OH_58D,

    AH_64A,
    AH_64D,
    AH_1W,

    UH_1H,

    Mi_8MT,
    Mi_28N,
    Mi_24V,
    Ka_50,

    P_51D_30_NA,
    P_51D,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    A_20G,

    SpitfireLFMkIXCW,
    SpitfireLFMkIX,

    I_16,

    Bf_109K_4,
    FW_190D9,
    FW_190A8,

    A_4E_C,
    Rafale_A_S,

    WingLoong_I,
    MQ_9_Reaper,
    RQ_1A_Predator
]

CAS_PREFERRED = [
    Su_17M4,
    Su_24M,
    Su_24MR,
    Su_25,
    Su_25T,
    Su_25TM,
    Su_30,
    Su_34,

    A_10A,
    A_10C,
    A_10C_2,
    AV8BNA,

    Tornado_GR4,

    C_101CC,
    MB_339PAN,
    L_39ZA,
    AJS37,

    SA342M,
    SA342L,
    OH_58D,

    AH_64A,
    AH_64D,
    AH_1W,

    Mi_28N,
    Mi_24V,
    Ka_50,

    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    A_20G,
    I_16,

    A_4E_C,
    Rafale_A_S,

    WingLoong_I,
    MQ_9_Reaper,
    RQ_1A_Predator
]

# Aircraft used for SEAD / DEAD tasks
SEAD_CAPABLE = [
    F_4E,
    FA_18C_hornet,

    F_16C_50,
    AV8BNA,
    JF_17,

    Su_24M,
    Su_25T,
    Su_25TM,
    Su_17M4,
    Su_30,
    Su_34,
    MiG_27K,

    Tornado_IDS,
    Tornado_GR4,

    A_4E_C,
    Rafale_A_S
]

SEAD_PREFERRED = [
    F_4E,
    Su_25T,
    Su_25TM,
    Tornado_IDS,
    F_16C_50,
    FA_18C_hornet,
    Su_30,
    Su_34,
    Su_24M,
]

# Aircraft used for Strike mission
STRIKE_CAPABLE = [
    MiG_15bis,
    MiG_27K,
    MB_339PAN,

    Su_17M4,
    Su_24M,
    Su_24MR,
    Su_25,
    Su_25T,
    Su_25TM,
    Su_27,
    Su_33,
    Su_30,
    Su_34,
    MiG_29A,
    MiG_29G,
    MiG_29K,
    MiG_29S,

    Tu_160,
    Tu_22M3,
    Tu_95MS,

    JF_17,

    M_2000C,

    A_10C,
    A_10C_2,
    AV8BNA,

    F_86F_Sabre,
    F_5E_3,

    F_14A_135_GR,
    F_14B,
    F_15E,
    F_16A,
    F_16C_50,
    FA_18C_hornet,

    B_1B,
    B_52H,
    F_117A,

    Tornado_IDS,
    Tornado_GR4,

    C_101CC,
    L_39ZA,
    AJS37,

    P_51D_30_NA,
    P_51D,
    P_47D_30,
    P_47D_30bl1,
    P_47D_40,
    A_20G,
    B_17G,

    SpitfireLFMkIXCW,
    SpitfireLFMkIX,

    Bf_109K_4,
    FW_190D9,
    FW_190A8,

    A_4E_C,
    Rafale_A_S

]

STRIKE_PREFERRED = [
    AJS37,
    A_20G,
    B_17G,
    B_1B,
    B_52H,
    F_117A,
    F_15E,
    Su_24M,
    Su_30,
    Su_34,
    Tornado_IDS,
    Tornado_GR4,
    Tu_160,
    Tu_22M3,
    Tu_95MS,
]

ANTISHIP_CAPABLE = [
    AJS37,

    Su_24M,
    Su_17M4,
    FA_18C_hornet,

    AV8BNA,
    JF_17,

    Su_30,
    Su_34,
    Tu_22M3,

    Tornado_IDS,
    Tornado_GR4,

    Ju_88A4,
    Rafale_A_S,
]

ANTISHIP_PREFERRED = [
    AJS37,
    FA_18C_hornet,
    JF_17,
    Rafale_A_S,
    Su_24M,
    Su_30,
    Su_34,
    Tu_22M3,
    Ju_88A4
]

RUNWAY_ATTACK_PREFERRED = [
    JF_17,
    M_2000C,
    Su_30,
    Su_34,
    Tornado_IDS,
]

RUNWAY_ATTACK_CAPABLE = STRIKE_CAPABLE

DRONES = [
    MQ_9_Reaper,
    RQ_1A_Predator,
    WingLoong_I
]