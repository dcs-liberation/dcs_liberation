from pydcs_extensions.a4ec.a4ec import A_4E_C
from pydcs_extensions.ah64d.ah64d import AH_64D_BLK_II
from pydcs_extensions.f104.f104 import VSN_F104G, VSN_F104S, VSN_F104S_AG
from pydcs_extensions.f22a.f22a import F_22A
from pydcs_extensions.hercules.hercules import Hercules
from pydcs_extensions.highdigitsams import highdigitsams
from pydcs_extensions.jas39.jas39 import JAS39Gripen, JAS39Gripen_AG
from pydcs_extensions.su57.su57 import Su_57
import pydcs_extensions.frenchpack.frenchpack as frenchpack
from pydcs_extensions.uh60l.uh60l import UH_60L, KC130J

MODDED_AIRPLANES = [
    A_4E_C,
    Su_57,
    F_22A,
    VSN_F104G,
    VSN_F104S,
    VSN_F104S_AG,
    Hercules,
    KC130J,
    JAS39Gripen,
    JAS39Gripen_AG,
]
MODDED_HELICOPTERS = [
    UH_60L,
    AH_64D_BLK_II,
]
MODDED_VEHICLES = [
    frenchpack._FIELD_HIDE,
    frenchpack._FIELD_HIDE_SMALL,
    frenchpack.SMOKE_SAM_IR,
    frenchpack.SmokeD1,
    frenchpack.SmokeD3,
    frenchpack.AMX_10RCR,
    frenchpack.AMX_10RCR_SEPAR,
    frenchpack.ERC_90,
    frenchpack.MO_120_RT,
    frenchpack._53T2,
    frenchpack.TRM_2000,
    frenchpack.TRM_2000_Fuel,
    frenchpack.TRM_2000_53T2,
    frenchpack.TRM_2000_PAMELA,
    frenchpack.VAB_MEDICAL,
    frenchpack.VAB,
    frenchpack.VAB__50,
    frenchpack.VAB_T20_13,
    frenchpack.VAB_MEPHISTO,
    frenchpack.VAB_MORTIER,
    frenchpack.VBL__50,
    frenchpack.VBL_AANF1,
    frenchpack.VBL,
    frenchpack.VBAE_CRAB,
    frenchpack.VBAE_CRAB_MMP,
    frenchpack.AMX_30B2,
    frenchpack.Tracma_TD_1500,
    frenchpack.Infantry_Soldier_JTAC,
    frenchpack.Char_M551_Sheridan,
    frenchpack.Leclerc_Serie_XXI,
    frenchpack.DIM__TOYOTA_BLUE,
    frenchpack.DIM__TOYOTA_GREEN,
    frenchpack.DIM__TOYOTA_DESERT,
    frenchpack.DIM__KAMIKAZE,
    frenchpack.VBCI,
    frenchpack.AMX_13_75mm,
    frenchpack.AMX_13_90mm,
    frenchpack.Char_T_62,
    frenchpack.Char_T_64BV,
    frenchpack.Char_T_72A,
    frenchpack.KORNET_ATGM,
    highdigitsams.AAA_SON_9_Fire_Can,
    highdigitsams.AAA_100mm_KS_19,
    highdigitsams.SAM_SA_10B_S_300PS_54K6_CP,
    highdigitsams.SAM_SA_10B_S_300PS_5P85SE_LN,
    highdigitsams.SAM_SA_10B_S_300PS_5P85SU_LN,
    highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85CE,
    highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85DE,
    highdigitsams.SAM_SA_10B_S_300PS_30N6_TR,
    highdigitsams.SAM_SA_10B_S_300PS_40B6M_TR,
    highdigitsams.SAM_SA_10B_S_300PS_40B6MD_SR,
    highdigitsams.SAM_SA_10B_S_300PS_64H6E_SR,
    highdigitsams.SAM_SA_20_S_300PMU1_CP_54K6,
    highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E,
    highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E_truck,
    highdigitsams.SAM_SA_20_S_300PMU1_SR_5N66E,
    highdigitsams.SAM_SA_20_S_300PMU1_SR_64N6E,
    highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85CE,
    highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85DE,
    highdigitsams.SAM_SA_20B_S_300PMU2_CP_54K6E2,
    highdigitsams.SAM_SA_20B_S_300PMU2_TR_92H6E_truck,
    highdigitsams.SAM_SA_20B_S_300PMU2_SR_64N6E2,
    highdigitsams.SAM_SA_20B_S_300PMU2_LN_5P85SE2,
    highdigitsams.SAM_SA_12_S_300V_9S457_CP,
    highdigitsams.SAM_SA_12_S_300V_9A82_LN,
    highdigitsams.SAM_SA_12_S_300V_9A83_LN,
    highdigitsams.SAM_SA_12_S_300V_9S15_SR,
    highdigitsams.SAM_SA_12_S_300V_9S19_SR,
    highdigitsams.SAM_SA_12_S_300V_9S32_TR,
    highdigitsams.SAM_SA_23_S_300VM_9S457ME_CP,
    highdigitsams.SAM_SA_23_S_300VM_9S15M2_SR,
    highdigitsams.SAM_SA_23_S_300VM_9S19M2_SR,
    highdigitsams.SAM_SA_23_S_300VM_9S32ME_TR,
    highdigitsams.SAM_SA_23_S_300VM_9A83ME_LN,
    highdigitsams.SAM_SA_23_S_300VM_9A82ME_LN,
    highdigitsams.SAM_SA_17_Buk_M1_2_LN_9A310M1_2,
    highdigitsams.SAM_SA_2__V759__LN_SM_90,
    highdigitsams.SAM_HQ_2_LN_SM_90,
    highdigitsams.SAM_SA_3__V_601P__LN_5P73,
    highdigitsams.SAM_SA_24_Igla_S_manpad,
    highdigitsams.SAM_SA_14_Strela_3_manpad,
    highdigitsams.Polyana_D4M1_C2_node,
    highdigitsams._34Ya6E_Gazetchik_E_decoy,
]
