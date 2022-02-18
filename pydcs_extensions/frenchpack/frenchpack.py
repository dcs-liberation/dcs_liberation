# Requires French Pack mod :
# https://forums.eagle.ru/showthread.php?t=279974
#
from dcs import unittype

from game.modsupport import vehiclemod


@vehiclemod
class AMX_10RCR(unittype.VehicleType):
    id = "AMX10RCR"
    name = "AMX-10RCR"
    detection_range = 0
    threat_range = 4000
    air_weapon_dist = 4000


@vehiclemod
class AMX_10RCR_SEPAR(unittype.VehicleType):
    id = "SEPAR"
    name = "AMX-10RCR SEPAR"
    detection_range = 0
    threat_range = 4000
    air_weapon_dist = 4000


@vehiclemod
class ERC_90(unittype.VehicleType):
    id = "ERC"
    name = "ERC-90"
    detection_range = 0
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class VAB__50(unittype.VehicleType):
    id = "VAB_50"
    name = "VAB .50"
    detection_range = 0
    threat_range = 1200
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class VAB_T20_13(unittype.VehicleType):
    id = "VIB_VBR"
    name = "VAB T20/13"
    detection_range = 0
    threat_range = 2000
    air_weapon_dist = 2000
    eplrs = True


@vehiclemod
class VAB_MEPHISTO(unittype.VehicleType):
    id = "VAB_HOT"
    name = "VAB MEPHISTO"
    detection_range = 0
    threat_range = 4000
    air_weapon_dist = 4000
    eplrs = True


@vehiclemod
class VBL__50(unittype.VehicleType):
    id = "VBL50"
    name = "VBL .50"
    detection_range = 0
    threat_range = 1200
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class VBL_AANF1(unittype.VehicleType):
    id = "VBLANF1"
    name = "VBL AANF1"
    detection_range = 0
    threat_range = 1000
    air_weapon_dist = 1000
    eplrs = True


@vehiclemod
class VBAE_CRAB(unittype.VehicleType):
    id = "VBAE"
    name = "VBAE CRAB"
    detection_range = 0
    threat_range = 3500
    air_weapon_dist = 3500
    eplrs = True


@vehiclemod
class VBAE_CRAB_MMP(unittype.VehicleType):
    id = "VBAE_MMP"
    name = "VBAE CRAB MMP"
    detection_range = 0
    threat_range = 3500
    air_weapon_dist = 3500
    eplrs = True


@vehiclemod
class AMX_30B2(unittype.VehicleType):
    id = "AMX-30B2"
    name = "AMX-30B2"
    detection_range = 0
    threat_range = 3500
    air_weapon_dist = 2500


@vehiclemod
class Char_M551_Sheridan(unittype.VehicleType):
    id = "SHERIDAN"
    name = "Char M551 Sheridan"
    detection_range = 0
    threat_range = 5000
    air_weapon_dist = 5000


@vehiclemod
class Leclerc_Serie_XXI(unittype.VehicleType):
    id = "Leclerc_XXI"
    name = "Leclerc Série XXI"
    detection_range = 0
    threat_range = 5000
    air_weapon_dist = 5000


@vehiclemod
class DIM__TOYOTA_BLUE(unittype.VehicleType):
    id = "Toyota_bleu"
    name = "DIM' TOYOTA BLUE"
    detection_range = 0
    threat_range = 1200
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class DIM__TOYOTA_GREEN(unittype.VehicleType):
    id = "Toyota_vert"
    name = "DIM' TOYOTA GREEN"
    detection_range = 0
    threat_range = 1200
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class DIM__TOYOTA_DESERT(unittype.VehicleType):
    id = "Toyota_desert"
    name = "DIM' TOYOTA DESERT"
    detection_range = 0
    threat_range = 1200
    air_weapon_dist = 1200
    eplrs = True


@vehiclemod
class DIM__KAMIKAZE(unittype.VehicleType):
    id = "Kamikaze"
    name = "DIM' KAMIKAZE"
    detection_range = 0
    threat_range = 50
    air_weapon_dist = 50
    eplrs = True


## FORTIFICATION


@vehiclemod
class _FIELD_HIDE(unittype.VehicleType):
    id = "FieldHL"
    name = "*FIELD HIDE"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class _FIELD_HIDE_SMALL(unittype.VehicleType):
    id = "HARRIERH"
    name = "*FIELD HIDE SMALL"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SmokeD1(unittype.VehicleType):
    id = "SmokeD1"
    name = "SmokeD1"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class SmokeD3(unittype.VehicleType):
    id = "SmokeD3"
    name = "SmokeD3"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class TRM_2000(unittype.VehicleType):
    id = "TRM2000"
    name = "TRM-2000"
    detection_range = 3500
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class TRM_2000_Fuel(unittype.VehicleType):
    id = "TRM2000_Citerne"
    name = "TRM-2000 Fuel"
    detection_range = 3500
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class VAB_MEDICAL(unittype.VehicleType):
    id = "VABH"
    name = "VAB MEDICAL"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class VAB(unittype.VehicleType):
    id = "VAB_RADIO"
    name = "VAB"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class VBL(unittype.VehicleType):
    id = "VBL-Radio"
    name = "VBL"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class Tracma_TD_1500(unittype.VehicleType):
    id = "Tracma"
    name = "Tracma TD 1500"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


## AIRDEFENCE


@vehiclemod
class SMOKE_SAM_IR(unittype.VehicleType):
    id = "SMOKESAM"
    name = "SMOKE SAM IR"
    detection_range = 20000
    threat_range = 20000
    air_weapon_dist = 20000
    eplrs = True


@vehiclemod
class _53T2(unittype.VehicleType):
    id = "AA20"
    name = "53T2"
    detection_range = 5000
    threat_range = 4000
    air_weapon_dist = 4000


@vehiclemod
class TRM_2000_53T2(unittype.VehicleType):
    id = "TRM2000_AA20"
    name = "TRM-2000 53T2"
    detection_range = 6000
    threat_range = 2000
    air_weapon_dist = 2000
    eplrs = True


@vehiclemod
class TRM_2000_PAMELA(unittype.VehicleType):
    id = "TRMMISTRAL"
    name = "TRM-2000 PAMELA"
    detection_range = 8000
    threat_range = 10000
    air_weapon_dist = 10000
    eplrs = True


@vehiclemod
class Leclerc_Serie_XXI_Desert(unittype.VehicleType):
    id = "Leclerc_XXI_Desert"
    name = "Leclerc Série XXI Désert"
    detection_range = 0
    threat_range = 4000
    air_weapon_dist = 4000


@vehiclemod
class AMX_13_75mm(unittype.VehicleType):
    id = "AMX1375"
    name = "AMX-13 75mm"
    detection_range = 0
    threat_range = 3500
    air_weapon_dist = 3500


@vehiclemod
class AMX_13_90mm(unittype.VehicleType):
    id = "AMX1390"
    name = "AMX-13 90mm"
    detection_range = 0
    threat_range = 3500
    air_weapon_dist = 3500


@vehiclemod
class VBCI(unittype.VehicleType):
    id = "VBCI"
    name = "VBCI"
    detection_range = 0
    threat_range = 3500
    air_weapon_dist = 3500
    eplrs = True


@vehiclemod
class Char_T_62(unittype.VehicleType):
    id = "T62"
    name = "Char T-62"
    detection_range = 0
    threat_range = 4000
    air_weapon_dist = 4000


@vehiclemod
class Char_T_64BV(unittype.VehicleType):
    id = "T64BV"
    name = "Char T-64BV"
    detection_range = 0
    threat_range = 4000
    air_weapon_dist = 4000


@vehiclemod
class Char_T_72A(unittype.VehicleType):
    id = "T72M"
    name = "Char T-72A"
    detection_range = 0
    threat_range = 4000
    air_weapon_dist = 4000


@vehiclemod
class KORNET_ATGM(unittype.VehicleType):
    id = "KORNET"
    name = "KORNET ATGM"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


## INFANTRY


@vehiclemod
class Infantry_Soldier_JTAC(unittype.VehicleType):
    id = "JTACFP"
    name = "Infantry Soldier JTAC"
    detection_range = 0
    threat_range = 500
    air_weapon_dist = 500


## ARTILERY


@vehiclemod
class MO_120_RT(unittype.VehicleType):
    id = "M120"
    name = "MO 120 RT"
    detection_range = 0
    threat_range = 15000
    air_weapon_dist = 15000


@vehiclemod
class VAB_MORTIER(unittype.VehicleType):
    id = "VAB_MORTIER"
    name = "VAB MORTIER"
    detection_range = 0
    threat_range = 15000
    air_weapon_dist = 15000
    eplrs = True
