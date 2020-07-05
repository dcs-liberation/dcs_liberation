from dcs.planes import *
from dcs.helicopters import *

# Interceptor are the aircraft prioritized for interception tasks
# If none is available, the AI will use regular CAP-capable aircraft instead
from pydcs_extensions.a4ec.a4ec import A_4E_C
from pydcs_extensions.mb339.mb339 import MB_339PAN

INTERCEPT_CAPABLE = [
    MiG_21Bis,
    MiG_25PD,
    MiG_31,
    MiG_29S,
    MiG_29A,
    MiG_29G,
    MiG_29K,

    M_2000C,
    Mirage_2000_5,

    F_14B,
    F_15C,

]

# Used for CAP, Escort, and intercept if there is not a specialised aircraft available
CAP_CAPABLE = [
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

    M_2000C,
    Mirage_2000_5,

    F_86F_Sabre,
    F_4E,
    F_5E_3,
    F_14B,
    F_15C,
    F_16C_50,
    FA_18C_hornet,

    C_101CC,
    L_39ZA,

    P_51D_30_NA,
    P_51D,
    P_47D_30,

    SpitfireLFMkIXCW,
    SpitfireLFMkIX,

    Bf_109K_4,
    FW_190D9,
    FW_190A8,

    A_4E_C
]

# USed for CAS (Close air support) and BAI (Battlefield Interdiction)
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
    Su_34,

    JF_17,

    M_2000C,

    A_10A,
    A_10C,
    AV8BNA,

    F_86F_Sabre,
    F_5E_3,
    F_14B,
    F_16C_50,
    FA_18C_hornet,

    C_101CC,
    MB_339PAN,
    L_39ZA,
    AJS37,

    SA342M,
    SA342L,

    AH_64A,
    AH_64D,

    UH_1H,

    Mi_8MT,
    Mi_28N,
    Mi_24V,
    Ka_50,

    P_51D_30_NA,
    P_51D,
    P_47D_30,
    A_20G,

    SpitfireLFMkIXCW,
    SpitfireLFMkIX,

    Bf_109K_4,
    FW_190D9,
    FW_190A8,

    A_4E_C
]

# Aircraft used for SEAD / DEAD tasks
SEAD_CAPABLE = [
    F_4E,
    FA_18C_hornet,
    # F_16C_50, Not yet
    AV8BNA,
    JF_17,

    Su_24M,
    Su_25T,
    Su_25TM,
    Su_17M4,
    Su_30,
    Su_34,
    MiG_27K,

    A_4E_C
]

# Aircraft used for Strike mission
STRIKE_CAPABLE = [
    MiG_15bis,
    MiG_29A,
    MiG_27K,
    MiG_29S,
    MB_339PAN,

    Su_17M4,
    Su_24M,
    Su_24MR,
    Su_25,
    Su_25T,
    Su_34,

    JF_17,

    M_2000C,

    A_10A,
    A_10C,
    AV8BNA,

    F_86F_Sabre,
    F_5E_3,
    F_14B,
    F_16C_50,
    FA_18C_hornet,

    C_101CC,
    L_39ZA,
    AJS37,

    P_51D_30_NA,
    P_51D,
    P_47D_30,
    A_20G,
    B_17G,

    SpitfireLFMkIXCW,
    SpitfireLFMkIX,

    Bf_109K_4,
    FW_190D9,
    FW_190A8,

    A_4E_C

]

ANTISHIP_CAPABLE = [
    Su_24M,
    Su_17M4,
    F_A_18C,
    AV8BNA,
    JF_17,
    F_16C_50,
    A_10C,
    A_10A,

    Ju_88A4,
]