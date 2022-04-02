# Requires French Pack mod :
# https://www.reddit.com/r/DCSExposed/comments/m5uje8/insurgent_pack_work_in_progress_impressions/
#
from dcs import unittype

from game.modsupport import vehiclemod


@vehiclemod
class HPG_Ural_Isis_Troops(unittype.VehicleType):
    id = "HPG_Ural_Isis_Troops"
    name = "*LLH Ural ISIS Troops"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class HPG_Ural_Isis_Covered(unittype.VehicleType):
    id = "HPG_Ural_Isis_Covered"
    name = "*LLH Ural ISIS Covered"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class HPGUralIsisFlak(unittype.VehicleType):
    id = "HPGUralIsisFlak"
    name = "*LLH Ural ISIS Flak 88"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class HPGUralIsisZU23(unittype.VehicleType):
    id = "HPGUralIsisZU23"
    name = "*LLH Ural ISIS ZU23"
    detection_range = 7500
    threat_range = 2500
    air_weapon_dist = 2500


@vehiclemod
class HPG_Toyota_ISIS(unittype.VehicleType):
    id = "HPG_Toyota_ISIS"
    name = "*LLH Toyota ISIS"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
    eplrs = True


@vehiclemod
class HPGToyotaISISDShK(unittype.VehicleType):
    id = "HPGToyotaISISDShK"
    name = "*LLH Toyota ISIS DShk"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


## FORTIFICATIONS


@vehiclemod
class LLH_IED_Site_Barrel(unittype.VehicleType):
    id = "LLH_IED_Site_Barrel"
    name = "*LLH IED Site Barrel"
    detection_range = 0
    threat_range = 20000
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class LLH_Shovel_Flat(unittype.VehicleType):
    id = "LLH_Shovel_Flat"
    name = "*LLH_Shovel Flat"
    detection_range = 0
    threat_range = 1100
    air_weapon_dist = 1100
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class LLH_Shovel_Planted(unittype.VehicleType):
    id = "LLH Shovel_Planted"
    name = "*LLH Shovel Planted"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class LLH_Cache_Site(unittype.VehicleType):
    id = "LLH_Cache_Site"
    name = "*LLH Cache Site"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class LLH_IED_Can(unittype.VehicleType):
    id = "LLH_IED_Can"
    name = "*LLH IED Can"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class LLH_Fertilizer(unittype.VehicleType):
    id = "LLH_Fertilizer"
    name = "*LLH Fertilizer Bag"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class LLH_Fertilizer_Stack(unittype.VehicleType):
    id = "LLH_Fertilizer_Stack"
    name = "*LLH Fertilizer Stack"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0


@vehiclemod
class LLH_Diesel_Drum(unittype.VehicleType):
    id = "LLH_Diesel_Drum"
    name = "*LLH Diesel Drum"
    detection_range = 0
    threat_range = 0
    air_weapon_dist = 0
