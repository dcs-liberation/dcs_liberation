from datetime import datetime
from enum import Enum
from typing import Optional, Type, Union

from dcs.countries import country_dict
from dcs.helicopters import (
    OH_58D,
    helicopter_map,
)
from dcs.mapping import Point

# mypy can't resolve these if they're wildcard imports for some reason.
from dcs.planes import (
    B_17G,
    FA_18C_hornet,
    F_16C_50,
    F_14A,
    Ju_88A4,
    P_51D_30_NA,
    plane_map,
)
from dcs.ships import (
    ship_map,
    Stennis,
    KUZNECOW,
    CVN_71,
    CVN_75,
    CVN_73,
    CVN_72,
    CV_1143_5,
)
from dcs.terrain.terrain import Airport
from dcs.unit import Ship
from dcs.unitgroup import ShipGroup, StaticGroup
from dcs.unittype import UnitType, FlyingType, ShipType, VehicleType
from dcs.vehicles import (
    vehicle_map,
)

import pydcs_extensions.frenchpack.frenchpack as frenchpack
import pydcs_extensions.highdigitsams.highdigitsams as highdigitsams

# PATCH pydcs data with MODS
from game.factions.faction_loader import FactionLoader
from pydcs_extensions.a4ec.a4ec import A_4E_C
from pydcs_extensions.ea6b.ea6b import EA_6B
from pydcs_extensions.eurofighter.eurofighter import Eurofighter
from pydcs_extensions.f104.f104 import VSN_F104G, VSN_F104S, VSN_F104S_AG
from pydcs_extensions.f18f.f18f import VSN_FA18F, VSN_FA18F_AG
from pydcs_extensions.f22a.f22a import F_22A
from pydcs_extensions.hercules.hercules import Hercules
from pydcs_extensions.jas39.jas39 import JAS39Gripen, JAS39Gripen_AG
from pydcs_extensions.rafale.rafale import Rafale_B, Rafale_C
from pydcs_extensions.su57.su57 import Su_57

plane_map["A-4E-C"] = A_4E_C
plane_map["EA-6B"] = EA_6B
plane_map["Eurofighter"] = Eurofighter
plane_map["FA18F_hornet"] = VSN_FA18F
plane_map["FA18F_hornetAG"] = VSN_FA18F_AG
plane_map["F-22A"] = F_22A
plane_map["Su-57"] = Su_57
plane_map["Hercules"] = Hercules
plane_map["JAS39Gripen"] = JAS39Gripen
plane_map["JAS39Gripen_AG"] = JAS39Gripen_AG
plane_map["Rafale_B"] = Rafale_B
plane_map["Rafale_C"] = Rafale_C
plane_map["VSN_F104G"] = VSN_F104G
plane_map["VSN_F104S"] = VSN_F104S
plane_map["VSN_F104S_AG"] = VSN_F104S_AG

vehicle_map["FieldHL"] = frenchpack._FIELD_HIDE
vehicle_map["HARRIERH"] = frenchpack._FIELD_HIDE_SMALL
vehicle_map["SMOKESAM"] = frenchpack.SMOKE_SAM_IR
vehicle_map["SmokeD1"] = frenchpack.SmokeD1
vehicle_map["SmokeD3"] = frenchpack.SmokeD3
vehicle_map["AMX10RCR"] = frenchpack.AMX_10RCR
vehicle_map["SEPAR"] = frenchpack.AMX_10RCR_SEPAR
vehicle_map["ERC"] = frenchpack.ERC_90
vehicle_map["M120"] = frenchpack.MO_120_RT
vehicle_map["AA20"] = frenchpack._53T2
vehicle_map["TRM2000"] = frenchpack.TRM_2000
vehicle_map["TRM2000_Citerne"] = frenchpack.TRM_2000_Fuel
vehicle_map["TRM2000_AA20"] = frenchpack.TRM_2000_53T2
vehicle_map["TRMMISTRAL"] = frenchpack.TRM_2000_PAMELA
vehicle_map["VABH"] = frenchpack.VAB_MEDICAL
vehicle_map["VAB_RADIO"] = frenchpack.VAB
vehicle_map["VAB_50"] = frenchpack.VAB__50
vehicle_map["VIB_VBR"] = frenchpack.VAB_T20_13
vehicle_map["VAB_HOT"] = frenchpack.VAB_MEPHISTO
vehicle_map["VAB_MORTIER"] = frenchpack.VAB_MORTIER
vehicle_map["VBL50"] = frenchpack.VBL__50
vehicle_map["VBLANF1"] = frenchpack.VBL_AANF1
vehicle_map["VBL-radio"] = frenchpack.VBL
vehicle_map["VBAE"] = frenchpack.VBAE_CRAB
vehicle_map["VBAE_MMP"] = frenchpack.VBAE_CRAB_MMP
vehicle_map["AMX-30B2"] = frenchpack.AMX_30B2
vehicle_map["Tracma"] = frenchpack.Tracma_TD_1500
vehicle_map["JTACFP"] = frenchpack.Infantry_Soldier_JTAC
vehicle_map["SHERIDAN"] = frenchpack.Char_M551_Sheridan
vehicle_map["Leclerc_XXI"] = frenchpack.Leclerc_Serie_XXI
vehicle_map["Toyota_bleu"] = frenchpack.DIM__TOYOTA_BLUE
vehicle_map["Toyota_vert"] = frenchpack.DIM__TOYOTA_GREEN
vehicle_map["Toyota_desert"] = frenchpack.DIM__TOYOTA_DESERT
vehicle_map["Kamikaze"] = frenchpack.DIM__KAMIKAZE
vehicle_map["AMX1375"] = frenchpack.AMX_13_75mm
vehicle_map["AMX1390"] = frenchpack.AMX_13_90mm
vehicle_map["VBCI"] = frenchpack.VBCI
vehicle_map["T62"] = frenchpack.Char_T_62
vehicle_map["T64BV"] = frenchpack.Char_T_64BV
vehicle_map["T72M"] = frenchpack.Char_T_72A
vehicle_map["KORNET"] = frenchpack.KORNET_ATGM


vehicle_map[highdigitsams.AAA_SON_9_Fire_Can.id] = highdigitsams.AAA_SON_9_Fire_Can
vehicle_map[highdigitsams.AAA_100mm_KS_19.id] = highdigitsams.AAA_100mm_KS_19
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_54K6_CP.id
] = highdigitsams.SAM_SA_10B_S_300PS_54K6_CP
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_5P85SE_LN.id
] = highdigitsams.SAM_SA_10B_S_300PS_5P85SE_LN
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_5P85SU_LN.id
] = highdigitsams.SAM_SA_10B_S_300PS_5P85SU_LN
vehicle_map[
    highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85CE.id
] = highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85CE
vehicle_map[
    highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85DE.id
] = highdigitsams.SAM_SA_10__5V55RUD__S_300PS_LN_5P85DE
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_30N6_TR.id
] = highdigitsams.SAM_SA_10B_S_300PS_30N6_TR
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_40B6M_TR.id
] = highdigitsams.SAM_SA_10B_S_300PS_40B6M_TR
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_40B6MD_SR.id
] = highdigitsams.SAM_SA_10B_S_300PS_40B6MD_SR
vehicle_map[
    highdigitsams.SAM_SA_10B_S_300PS_64H6E_SR.id
] = highdigitsams.SAM_SA_10B_S_300PS_64H6E_SR
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_CP_54K6.id
] = highdigitsams.SAM_SA_20_S_300PMU1_CP_54K6
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E.id
] = highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E_truck.id
] = highdigitsams.SAM_SA_20_S_300PMU1_TR_30N6E_truck
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_SR_5N66E.id
] = highdigitsams.SAM_SA_20_S_300PMU1_SR_5N66E
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_SR_64N6E.id
] = highdigitsams.SAM_SA_20_S_300PMU1_SR_64N6E
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85CE.id
] = highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85CE
vehicle_map[
    highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85DE.id
] = highdigitsams.SAM_SA_20_S_300PMU1_LN_5P85DE
vehicle_map[
    highdigitsams.SAM_SA_20B_S_300PMU2_CP_54K6E2.id
] = highdigitsams.SAM_SA_20B_S_300PMU2_CP_54K6E2
vehicle_map[
    highdigitsams.SAM_SA_20B_S_300PMU2_TR_92H6E_truck.id
] = highdigitsams.SAM_SA_20B_S_300PMU2_TR_92H6E_truck
vehicle_map[
    highdigitsams.SAM_SA_20B_S_300PMU2_SR_64N6E2.id
] = highdigitsams.SAM_SA_20B_S_300PMU2_SR_64N6E2
vehicle_map[
    highdigitsams.SAM_SA_20B_S_300PMU2_LN_5P85SE2.id
] = highdigitsams.SAM_SA_20B_S_300PMU2_LN_5P85SE2
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9S457_CP.id
] = highdigitsams.SAM_SA_12_S_300V_9S457_CP
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9A82_LN.id
] = highdigitsams.SAM_SA_12_S_300V_9A82_LN
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9A83_LN.id
] = highdigitsams.SAM_SA_12_S_300V_9A83_LN
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9S15_SR.id
] = highdigitsams.SAM_SA_12_S_300V_9S15_SR
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9S19_SR.id
] = highdigitsams.SAM_SA_12_S_300V_9S19_SR
vehicle_map[
    highdigitsams.SAM_SA_12_S_300V_9S32_TR.id
] = highdigitsams.SAM_SA_12_S_300V_9S32_TR
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9S457ME_CP.id
] = highdigitsams.SAM_SA_23_S_300VM_9S457ME_CP
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9S15M2_SR.id
] = highdigitsams.SAM_SA_23_S_300VM_9S15M2_SR
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9S19M2_SR.id
] = highdigitsams.SAM_SA_23_S_300VM_9S19M2_SR
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9S32ME_TR.id
] = highdigitsams.SAM_SA_23_S_300VM_9S32ME_TR
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9A83ME_LN.id
] = highdigitsams.SAM_SA_23_S_300VM_9A83ME_LN
vehicle_map[
    highdigitsams.SAM_SA_23_S_300VM_9A82ME_LN.id
] = highdigitsams.SAM_SA_23_S_300VM_9A82ME_LN
vehicle_map[
    highdigitsams.SAM_SA_17_Buk_M1_2_LN_9A310M1_2.id
] = highdigitsams.SAM_SA_17_Buk_M1_2_LN_9A310M1_2
vehicle_map[
    highdigitsams.SAM_SA_2__V759__LN_SM_90.id
] = highdigitsams.SAM_SA_2__V759__LN_SM_90
vehicle_map[highdigitsams.SAM_HQ_2_LN_SM_90.id] = highdigitsams.SAM_HQ_2_LN_SM_90
vehicle_map[
    highdigitsams.SAM_SA_3__V_601P__LN_5P73.id
] = highdigitsams.SAM_SA_3__V_601P__LN_5P73
vehicle_map[
    highdigitsams.SAM_SA_24_Igla_S_manpad.id
] = highdigitsams.SAM_SA_24_Igla_S_manpad
vehicle_map[
    highdigitsams.SAM_SA_14_Strela_3_manpad.id
] = highdigitsams.SAM_SA_14_Strela_3_manpad
vehicle_map[highdigitsams.Polyana_D4M1_C2_node.id] = highdigitsams.Polyana_D4M1_C2_node
vehicle_map[
    highdigitsams._34Ya6E_Gazetchik_E_decoy.id
] = highdigitsams._34Ya6E_Gazetchik_E_decoy

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
For example, player accessible Hornet is called `FA_18C_hornet`, and MANPAD Igla is called `AirDefence.MANPADS_SA_18_Igla_S_Grouse`
"""

# This should probably be much higher, but the AI doesn't rollover their budget
# and isn't smart enough to save to repair a critical runway anyway, so it has
# to be cheap enough to repair with a single turn's income.
RUNWAY_REPAIR_COST = 100

"""
Units separated by country. 
country : DCS Country name
"""
FACTIONS = FactionLoader()

"""
Aircraft livery overrides. Syntax as follows:

    `Identifier`: "LiveryName",

`Identifier` is aircraft identifier (as used troughout the file) and "LiveryName" (with double quotes) 
is livery name as found in mission editor.
"""
PLANE_LIVERY_OVERRIDES: dict[Type[FlyingType], str] = {
    FA_18C_hornet: "VFA-34",  # default livery for the hornet is blue angels one
    F_14A: "vf-142 `ghost riders`",  # default livery for the AI F-14A is the black demo scheme
}

"""
Possible time periods for new games

    `Name`: daytime(day, month, year),

`Identifier` is the name that will appear in the menu
The object is a python datetime object
"""
TIME_PERIODS = {
    "WW2 - Winter [1944]": datetime(1944, 1, 1),
    "WW2 - Spring [1944]": datetime(1944, 4, 1),
    "WW2 - Summer [1944]": datetime(1944, 6, 1),
    "WW2 - Fall [1944]": datetime(1944, 10, 1),
    "Early Cold War - Winter [1952]": datetime(1952, 1, 1),
    "Early Cold War - Spring [1952]": datetime(1952, 4, 1),
    "Early Cold War - Summer [1952]": datetime(1952, 6, 1),
    "Early Cold War - Fall [1952]": datetime(1952, 10, 1),
    "Cold War - Winter [1970]": datetime(1970, 1, 1),
    "Cold War - Spring [1970]": datetime(1970, 4, 1),
    "Cold War - Summer [1970]": datetime(1970, 6, 1),
    "Cold War - Fall [1970]": datetime(1970, 10, 1),
    "Late Cold War - Winter [1985]": datetime(1985, 1, 1),
    "Late Cold War - Spring [1985]": datetime(1985, 4, 1),
    "Late Cold War - Summer [1985]": datetime(1985, 6, 1),
    "Late Cold War - Fall [1985]": datetime(1985, 10, 1),
    "Gulf War - Winter [1990]": datetime(1990, 1, 1),
    "Gulf War - Spring [1990]": datetime(1990, 4, 1),
    "Gulf War - Summer [1990]": datetime(1990, 6, 1),
    "Mid-90s - Winter [1995]": datetime(1995, 1, 1),
    "Mid-90s - Spring [1995]": datetime(1995, 4, 1),
    "Mid-90s - Summer [1995]": datetime(1995, 6, 1),
    "Mid-90s - Fall [1995]": datetime(1995, 10, 1),
    "Gulf War - Fall [1990]": datetime(1990, 10, 1),
    "Modern - Winter [2010]": datetime(2010, 1, 1),
    "Modern - Spring [2010]": datetime(2010, 4, 1),
    "Modern - Summer [2010]": datetime(2010, 6, 1),
    "Modern - Fall [2010]": datetime(2010, 10, 1),
    "Georgian War [2008]": datetime(2008, 8, 7),
    "Syrian War [2011]": datetime(2011, 3, 15),
    "6 days war [1967]": datetime(1967, 6, 5),
    "Yom Kippour War [1973]": datetime(1973, 10, 6),
    "First Lebanon War [1982]": datetime(1982, 6, 6),
    "Arab-Israeli War [1948]": datetime(1948, 5, 15),
}

REWARDS = {
    "power": 4,
    "warehouse": 2,
    "ware": 2,
    "fuel": 2,
    "ammo": 2,
    "farp": 1,
    # TODO: Should generate no cash once they generate units.
    # https://github.com/dcs-liberation/dcs_liberation/issues/1036
    "factory": 10,
    "comms": 10,
    "oil": 10,
    "derrick": 8,
    "village": 0.25,
    "allycamp": 0.5,
}

"""
---------- END OF CONFIGURATION SECTION
"""

StartingPosition = Union[ShipGroup, StaticGroup, Airport, Point]


def upgrade_to_supercarrier(unit: Type[ShipType], name: str) -> Type[ShipType]:
    if unit == Stennis:
        if name == "CVN-71 Theodore Roosevelt":
            return CVN_71
        elif name == "CVN-72 Abraham Lincoln":
            return CVN_72
        elif name == "CVN-73 George Washington":
            return CVN_73
        elif name == "CVN-75 Harry S. Truman":
            return CVN_75
        elif name == "Carrier Strike Group 8":
            return CVN_75
        else:
            return CVN_71
    elif unit == KUZNECOW:
        return CV_1143_5
    else:
        return unit


def unit_type_from_name(name: str) -> Optional[Type[UnitType]]:
    if name in vehicle_map:
        return vehicle_map[name]
    elif name in plane_map:
        return plane_map[name]
    elif name in ship_map:
        return ship_map[name]
    if name in helicopter_map:
        return helicopter_map[name]
    else:
        return None


def vehicle_type_from_name(name: str) -> Type[VehicleType]:
    return vehicle_map[name]


def ship_type_from_name(name: str) -> Type[ShipType]:
    return ship_map[name]


def country_id_from_name(name: str) -> int:
    for k, v in country_dict.items():
        if v.name == name:
            return k
    return -1


class DefaultLiveries:
    class Default(Enum):
        af_standard = ""


OH_58D.Liveries = DefaultLiveries
F_16C_50.Liveries = DefaultLiveries  # type: ignore
P_51D_30_NA.Liveries = DefaultLiveries
Ju_88A4.Liveries = DefaultLiveries
B_17G.Liveries = DefaultLiveries
