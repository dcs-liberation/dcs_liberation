import typing
import enum
from datetime import datetime

from dcs.vehicles import *
from dcs.ships import *
from dcs.planes import *
from dcs.helicopters import *

from dcs.task import *
from dcs.unit import *
from dcs.unittype import *
from dcs.unitgroup import *

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
    MiG_23MLD: 13,
    Su_27: 18,
    Su_33: 22,
    MiG_29A: 18,
    MiG_29S: 20,
    MiG_29G: 18,
    MiG_31: 30,
    J_11A: 26,
    Su_30: 24,

    F_5E_3: 8,
    MiG_15bis: 4,
    MiG_19P: 6,
    F_86F_Sabre: 4,
    MiG_21Bis: 8,
    F_4E: 10,
    AJS37: 12,

    AV8BNA: 14,
    M_2000C: 16,
    Mirage_2000_5: 22,
    FA_18C_hornet: 24,
    F_15C: 26,
    F_16C_bl_52d: 20,
    F_14B: 22,
    Tornado_IDS: 24,
    # Tornado_GR4: 24,

    # bomber
    Su_17M4: 10,
    Su_25: 15,
    Su_25T: 18,
    L_39ZA: 10,
    Su_34: 24,
    Su_24M: 20,
    Su_24MR: 24,

    A_10A: 16,
    A_10C: 22,

    # heli
    Ka_50: 13,
    SA342M: 8,
    UH_1H: 4,
    Mi_8MT: 5,
    Mi_24V: 12,
    AH_1W: 10,
    AH_64A: 12,
    AH_64D: 15,
    OH_58D: 6,

    # Bombers
    B_52H: 25,
    B_1B: 50,

    # special
    IL_76MD: 13,
    An_26B: 13,
    An_30M: 13,
    Yak_40: 13,
    S_3B_Tanker: 13,
    IL_78M: 13,
    KC_135: 13,

    A_50: 8,
    E_3A: 8,
    C_130: 8,

    # WW2
    P_51D_30_NA: 3,
    P_51D: 3,

    # armor
    Armor.APC_MTLB: 4,
    Armor.ARV_MTLB_U_BOMAN: 5,
    Armor.ARV_BRDM_2: 6,
    Armor.ARV_BTR_RD: 8,
    Armor.APC_BTR_80: 8,
    Armor.MBT_T_55: 18,
    Armor.MBT_T_72B: 25,
    Armor.MBT_T_80U: 30,
    Armor.MBT_T_90: 35,
    Armor.IFV_BMD_1: 8,
    Armor.IFV_BMP_1: 14,
    Armor.IFV_BMP_2: 16,
    Armor.IFV_BMP_3: 20,

    Armor.APC_M113: 6,
    Armor.APC_M1043_HMMWV_Armament: 2,
    Armor.ATGM_M1045_HMMWV_TOW: 8,
    Armor.IFV_M2A2_Bradley: 12,
    Armor.APC_M1126_Stryker_ICV: 16,
    Armor.ATGM_M1134_Stryker: 18,
    Armor.MBT_M60A3_Patton: 18,
    Armor.MBT_M1A2_Abrams: 35,
    Armor.MBT_Leclerc: 35,
    Armor.MBT_Leopard_1A3: 24,
    Armor.MBT_Leopard_2: 35,
    Armor.TPz_Fuchs: 8,

    Unarmed.Transport_UAZ_469: 3,
    Unarmed.Transport_Ural_375: 3,
    Infantry.Infantry_M4: 1,
    Infantry.Soldier_AK: 1,

    Unarmed.Transport_M818: 3,

    AirDefence.AAA_Vulcan_M163: 5,
    AirDefence.SAM_Linebacker_M6: 10,

    AirDefence.AAA_ZU_23_Closed: 2,
    AirDefence.SPAAA_ZSU_23_4_Shilka: 4,
    AirDefence.SAM_SA_9_Strela_1_9P31: 8,
    AirDefence.SAM_SA_19_Tunguska_2S6: 15,
    AirDefence.SAM_SA_6_Kub_LN_2P25: 22,
    AirDefence.SAM_SA_8_Osa_9A33: 12,
    AirDefence.SAM_SA_3_S_125_LN_5P73: 20,
    AirDefence.SAM_SA_2_LN_SM_90: 15,
    AirDefence.SAM_SA_11_Buk_LN_9A310M1: 25,
    AirDefence.SAM_Hawk_PCP: 20,

    # ship
    CV_1143_5_Admiral_Kuznetsov: 100,
    CVN_74_John_C__Stennis: 100,
    LHA_1_Tarawa: 50,

    Bulk_cargo_ship_Yakushev: 10,
    Armed_speedboat: 10,
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
        F_5E_3,
        MiG_23MLD,
        Su_27,
        Su_33,
        MiG_19P,
        MiG_21Bis,
        MiG_29A,
        MiG_29S,
        FA_18C_hornet,
        F_15C,
        F_14B,
        F_16C_bl_52d,
        M_2000C,
        Mirage_2000_5,
        P_51D_30_NA,
        P_51D,
        MiG_29G,
        Su_30,
        J_11A
    ],
    CAS: [
        F_86F_Sabre,
        MiG_15bis,
        L_39ZA,
        AV8BNA,
        AJS37,
        A_10A,
        A_10C,
        Su_17M4,
        Su_25,
        Su_25T,
        Su_34,
        Ka_50,
        F_4E,
        SA342M,
        Su_24M,
        Su_24MR,
        AH_64A,
        AH_64D,
        OH_58D,
        B_52H,
        B_1B,
        Tornado_IDS,
        # Tornado_GR4,
    ],
    Transport: [
        IL_76MD,
        An_26B,
        An_30M,
        Yak_40,

        C_130,
    ],
    Refueling: [
        IL_78M,
        KC_135,
        S_3B_Tanker,
    ],
    AWACS: [E_3A, A_50, ],
    PinpointStrike: [
        Armor.APC_MTLB,
        Armor.APC_MTLB,
        Armor.APC_MTLB,
        Armor.APC_MTLB,
        Armor.APC_MTLB,
        Armor.ARV_MTLB_U_BOMAN,
        Armor.ARV_MTLB_U_BOMAN,
        Armor.ARV_MTLB_U_BOMAN,
        Armor.ARV_MTLB_U_BOMAN,
        Armor.ARV_MTLB_U_BOMAN,
        Armor.ARV_BRDM_2,
        Armor.ARV_BRDM_2,
        Armor.ARV_BRDM_2,
        Armor.ARV_BRDM_2,
        Armor.ARV_BRDM_2,
        Armor.ARV_BTR_RD,
        Armor.APC_BTR_80,
        Armor.APC_BTR_80,
        Armor.APC_BTR_80,
        Armor.MBT_T_55,
        Armor.MBT_T_55,
        Armor.MBT_T_55,
        Armor.MBT_T_72B,
        Armor.MBT_T_72B,
        Armor.MBT_T_80U,
        Armor.MBT_T_80U,
        Armor.MBT_T_90,

        Armor.APC_M113,
        Armor.APC_M113,
        Armor.APC_M113,
        Armor.APC_M113,
        Armor.TPz_Fuchs,
        Armor.TPz_Fuchs,
        Armor.TPz_Fuchs,
        Armor.TPz_Fuchs,
        Armor.ATGM_M1045_HMMWV_TOW,
        Armor.ATGM_M1045_HMMWV_TOW,
        Armor.APC_M1043_HMMWV_Armament,
        Armor.APC_M1043_HMMWV_Armament,
        Armor.IFV_M2A2_Bradley,
        Armor.IFV_M2A2_Bradley,
        Armor.ATGM_M1134_Stryker,
        Armor.ATGM_M1134_Stryker,
        Armor.MBT_M60A3_Patton,
        Armor.MBT_M60A3_Patton,
        Armor.MBT_M60A3_Patton,
        Armor.MBT_Leopard_1A3,
        Armor.MBT_Leopard_1A3,
        Armor.MBT_M1A2_Abrams,
        Armor.MBT_Leclerc,
        Armor.MBT_Leopard_2,
    ],
    AirDefence: [

        # those are listed multiple times here to balance prioritization more into lower tier AAs
        AirDefence.AAA_Vulcan_M163,
        AirDefence.AAA_Vulcan_M163,
        AirDefence.AAA_Vulcan_M163,
        AirDefence.SAM_Linebacker_M6,

        AirDefence.SPAAA_ZSU_23_4_Shilka,
        AirDefence.AAA_ZU_23_Closed,
        AirDefence.SAM_SA_9_Strela_1_9P31,
        AirDefence.SAM_SA_8_Osa_9A33,
        AirDefence.SAM_SA_19_Tunguska_2S6,
        AirDefence.SAM_SA_6_Kub_LN_2P25,
        AirDefence.SAM_SA_3_S_125_LN_5P73,
        AirDefence.SAM_Hawk_PCP,
        AirDefence.SAM_SA_2_LN_SM_90,
        AirDefence.SAM_SA_11_Buk_LN_9A310M1,
    ],
    Reconnaissance: [Unarmed.Transport_M818, Unarmed.Transport_Ural_375, Unarmed.Transport_UAZ_469],
    Nothing: [Infantry.Infantry_M4, Infantry.Soldier_AK, ],
    Embarking: [UH_1H, Mi_8MT, ],
    Carriage: [CVN_74_John_C__Stennis, LHA_1_Tarawa, CV_1143_5_Admiral_Kuznetsov, ],
    CargoTransportation: [Dry_cargo_ship_Ivanov, Bulk_cargo_ship_Yakushev, Tanker_Elnya_160, Armed_speedboat, ],
}

"""
Units from AirDefense category of UNIT_BY_TASK that will be removed from use if "No SAM" option is checked at the start of the game
"""
SAM_BAN = [
    AirDefence.SAM_Linebacker_M6,

    AirDefence.SAM_SA_9_Strela_1_9P31,
    AirDefence.SAM_SA_8_Osa_9A33,
    AirDefence.SAM_SA_19_Tunguska_2S6,
    AirDefence.SAM_SA_6_Kub_LN_2P25,
    AirDefence.SAM_SA_8_Osa_9A33,
    AirDefence.SAM_SA_3_S_125_LN_5P73,
    AirDefence.SAM_Hawk_PCP,
    AirDefence.SAM_SA_2_LN_SM_90,
    AirDefence.SAM_SA_11_Buk_LN_9A310M1,
]

"""
Used to convert SAM site parts to the corresponding site
"""
SAM_CONVERT = {
    AirDefence.SAM_SR_P_19: AirDefence.SAM_SA_3_S_125_LN_5P73,
    AirDefence.SAM_SA_3_S_125_TR_SNR: AirDefence.SAM_SA_3_S_125_LN_5P73,
    AirDefence.SAM_SA_3_S_125_LN_5P73: AirDefence.SAM_SA_3_S_125_LN_5P73,
    AirDefence.SAM_SA_6_Kub_LN_2P25: AirDefence.SAM_SA_6_Kub_LN_2P25,
    AirDefence.SAM_SA_6_Kub_STR_9S91: AirDefence.SAM_SA_6_Kub_LN_2P25,
    AirDefence.SAM_SA_10_S_300PS_LN_5P85C: AirDefence.SAM_SA_10_S_300PS_LN_5P85C,
    AirDefence.SAM_SA_10_S_300PS_SR_5N66M: AirDefence.SAM_SA_10_S_300PS_LN_5P85C,
    AirDefence.SAM_SA_10_S_300PS_TR_30N6: AirDefence.SAM_SA_10_S_300PS_LN_5P85C,
    AirDefence.SAM_SA_10_S_300PS_CP_54K6: AirDefence.SAM_SA_10_S_300PS_LN_5P85C,
    AirDefence.SAM_SA_10_S_300PS_SR_64H6E: AirDefence.SAM_SA_10_S_300PS_CP_54K6,
    AirDefence.SAM_Hawk_TR_AN_MPQ_46: AirDefence.SAM_Hawk_PCP,
    AirDefence.SAM_Hawk_SR_AN_MPQ_50: AirDefence.SAM_Hawk_PCP,
    AirDefence.SAM_Hawk_LN_M192: AirDefence.SAM_Hawk_PCP,
    'except': {
        # this radar is shared between the two S300's. if we attempt to find a SAM site at a base and can't find one
        #  model, we can safely assume the other was deployed
        # well, perhaps not safely, but we'll make the assumption anyway :p
        AirDefence.SAM_SA_10_S_300PS_TR_30N6: AirDefence.SAM_SA_10_S_300PS_CP_54K6,
        AirDefence.SAM_SR_P_19: AirDefence.SAM_SA_2_LN_SM_90
    }
}

"""
Units that will always be spawned in the air
"""
TAKEOFF_BAN = [
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
    "USA": AirDefence.SAM_Linebacker_M6,
    "France": AirDefence.SPAAA_Gepard,
    "Germany": AirDefence.SPAAA_Gepard,
    "China": AirDefence.SPAAA_ZSU_23_4_Shilka,
    "UK": AirDefence.AAA_Vulcan_M163,
    "Russia 1955": AirDefence.AAA_ZU_23_Closed,
    "USA 1955": AirDefence.AAA_Vulcan_M163,
    "Russia 1965": AirDefence.AAA_ZU_23_Closed,
    "Russia 1975": AirDefence.AAA_ZU_23_Closed,
    "USA 1965": AirDefence.AAA_Vulcan_M163,
    "Russia 1988": AirDefence.AAA_ZU_23_Closed,
    "USA 1990": AirDefence.AAA_Vulcan_M163,
    "France 1990": AirDefence.AAA_Vulcan_M163,
    "Germany 1990": AirDefence.AAA_Vulcan_M163,
    "Iran 2015": AirDefence.SPAAA_ZSU_23_4_Shilka,
    "China 2015": AirDefence.SPAAA_ZSU_23_4_Shilka
}

"""
Units separated by country. Currently only Russia and USA are supported. 

Be advised that putting unit to the country that have not access to the unit in the game itself will result in incorrect missions generated!
So it's better to just use 'Russia' or 'USA', 'Ukraine' and 'USAF Aggresor' faction which have most units.

country : DCS Country name

"""
FACTIONS = {

    "Russia 1955": {
        "country": "Russia",
        "side": "red",
        "units": [
            MiG_15bis,

            IL_76MD,
            IL_78M,
            An_26B,
            An_30M,
            Yak_40,

            AirDefence.AAA_ZU_23_Closed,
            AirDefence.SAM_SA_6_Kub_LN_2P25,
            AirDefence.SAM_SA_3_S_125_LN_5P73,

            Armor.ARV_BRDM_2,
            Armor.ARV_MTLB_U_BOMAN,
            Armor.APC_MTLB,
            Armor.MBT_T_55,

            Unarmed.Transport_Ural_375,
            Unarmed.Transport_UAZ_469,
            Infantry.Soldier_AK,

            CV_1143_5_Admiral_Kuznetsov,
            Bulk_cargo_ship_Yakushev,
            Dry_cargo_ship_Ivanov,
            Tanker_Elnya_160
        ]
    },

    "Russia 1965": {
        "country": "Russia",
        "side": "red",
        "units": [
            MiG_15bis,
            MiG_19P,
            MiG_21Bis,

            IL_76MD,
            IL_78M,
            An_26B,
            An_30M,
            Yak_40,

            A_50,

            Mi_8MT,

            AirDefence.AAA_ZU_23_Closed,
            AirDefence.SAM_SA_6_Kub_LN_2P25,
            AirDefence.SAM_SA_3_S_125_LN_5P73,

            Armor.ARV_BRDM_2,
            Armor.APC_BTR_80,
            Armor.ARV_BTR_RD,
            Armor.IFV_BMD_1,
            Armor.IFV_BMP_1,
            Armor.MBT_T_55,

            Unarmed.Transport_Ural_375,
            Unarmed.Transport_UAZ_469,
            Infantry.Soldier_AK,

            CV_1143_5_Admiral_Kuznetsov,
            Bulk_cargo_ship_Yakushev,
            Dry_cargo_ship_Ivanov,
            Tanker_Elnya_160
        ]
    },

    "Russia 1975": {
        "country": "Russia",
        "side": "red",
        "units": [

            MiG_21Bis,
            MiG_23MLD,
            MiG_25PD,
            MiG_29A,

            Su_17M4,
            Su_24M,
            Su_25,

            IL_76MD,
            IL_78M,
            An_26B,
            An_30M,
            Yak_40,

            A_50,

            Mi_8MT,
            Mi_24V,

            AirDefence.AAA_ZU_23_Closed,
            AirDefence.SAM_SA_6_Kub_LN_2P25,
            AirDefence.SAM_SA_3_S_125_LN_5P73,

            Armor.ARV_BRDM_2,
            Armor.APC_BTR_80,
            Armor.IFV_BMD_1,
            Armor.IFV_BMP_1,
            Armor.MBT_T_55,

            Unarmed.Transport_Ural_375,
            Unarmed.Transport_UAZ_469,
            Infantry.Soldier_AK,

            CV_1143_5_Admiral_Kuznetsov,
            Bulk_cargo_ship_Yakushev,
            Dry_cargo_ship_Ivanov,
            Tanker_Elnya_160
        ]
    },

    "Russia 1988": {
        "country": "Russia",
        "side": "red",
        "units": [

            MiG_23MLD,
            MiG_25PD,
            MiG_29A,
            MiG_29S,
            MiG_31,
            Su_27,

            Su_24M,
            Su_24MR,
            Su_25,

            IL_76MD,
            IL_78M,
            An_26B,
            An_30M,
            Yak_40,

            A_50,

            Mi_8MT,
            Mi_24V,

            AirDefence.AAA_ZU_23_Closed,
            AirDefence.SAM_SA_6_Kub_LN_2P25,
            AirDefence.SAM_SA_3_S_125_LN_5P73,

            Armor.ARV_BRDM_2,
            Armor.APC_BTR_80,
            Armor.IFV_BMD_1,
            Armor.IFV_BMP_1,
            Armor.MBT_T_55,

            Unarmed.Transport_Ural_375,
            Unarmed.Transport_UAZ_469,
            Infantry.Soldier_AK,

            CV_1143_5_Admiral_Kuznetsov,
            Bulk_cargo_ship_Yakushev,
            Dry_cargo_ship_Ivanov,
            Tanker_Elnya_160
        ]
    },

    "Russia 2010": {
        "country": "Russia",
        "side":"red",
        "units": [
            AJS37,
            MiG_23MLD,
            Su_25,
            Su_27,
            Su_33,
            MiG_29S,

            Su_25T,
            Su_34,
            Su_24MR,
            L_39ZA,

            IL_76MD,
            IL_78M,
            An_26B,
            An_30M,
            Yak_40,
            A_50,

            Ka_50,
            Mi_8MT,

            AirDefence.SPAAA_ZSU_23_4_Shilka,
            AirDefence.SAM_SA_19_Tunguska_2S6,
            AirDefence.SAM_SA_11_Buk_LN_9A310M1,
            AirDefence.SAM_SA_10_S_300PS_LN_5P85C,

            Armor.APC_BTR_80,
            Armor.MBT_T_90,
            Armor.MBT_T_80U,
            Armor.MBT_T_72B,

            Unarmed.Transport_Ural_375,
            Unarmed.Transport_UAZ_469,
            Infantry.Soldier_AK,
            CV_1143_5_Admiral_Kuznetsov,
            Bulk_cargo_ship_Yakushev,
            Dry_cargo_ship_Ivanov,
            Tanker_Elnya_160,
        ]
    },

    "Iran 2015": {
        "country": "Iran",
        "side": "red",
        "units": [

            MiG_29A,
            F_4E,
            F_14B,
            F_5E_3,

            MiG_21Bis,
            Su_24M,
            Su_25,
            Su_17M4,

            IL_76MD,
            IL_78M,
            An_26B,
            An_30M,
            Yak_40,

            A_50,

            Mi_28N,
            Mi_24V,

            AirDefence.AAA_ZU_23_Closed,
            AirDefence.AAA_ZU_23_Insurgent_on_Ural_375,
            AirDefence.SPAAA_ZSU_23_4_Shilka,
            AirDefence.SAM_Hawk_PCP,
            AirDefence.SAM_SA_2_LN_SM_90,

            Armor.APC_M113,
            Armor.APC_BTR_80,
            Armor.MBT_M60A3_Patton,
            Armor.MBT_T_72B,

            Unarmed.Transport_Ural_375,
            Unarmed.Transport_UAZ_469,
            Infantry.Soldier_AK,

            CV_1143_5_Admiral_Kuznetsov,
            Bulk_cargo_ship_Yakushev,
            Dry_cargo_ship_Ivanov,
            Tanker_Elnya_160
        ]
    },

    "China 2000": {
        "country": "China",
        "side": "red",
        "units": [

            MiG_21Bis, # Standing as J-7
            Su_30,
            J_11A,

            IL_76MD,
            IL_78M,
            An_26B,
            An_30M,
            Yak_40,

            A_50,

            Mi_8MT,

            AirDefence.AAA_ZU_23_Closed,
            AirDefence.Rapier_FSA_Launcher, # Standing as PL-9C Shorad
            AirDefence.SAM_SA_10_S_300PS_LN_5P85C, # Standing as HQ-9+
            AirDefence.SAM_SA_6_Kub_LN_2P25,
            # TODO : ADD HQ-7 (need pydcs support)

            Armor.MBT_T_55,
            Armor.ZBD_04A,
            Armor.IFV_BMP_1,

            Unarmed.Transport_Ural_375,
            Unarmed.Transport_UAZ_469,
            Infantry.Soldier_AK,

            CV_1143_5_Admiral_Kuznetsov,
            Bulk_cargo_ship_Yakushev,
            Dry_cargo_ship_Ivanov,
            Tanker_Elnya_160
        ]
    },

    "USA 1955": {
        "country": "USA",
        "side": "blue",
        "units": [
            F_86F_Sabre,
            P_51D,
            P_51D_30_NA,

            KC_135,
            S_3B_Tanker,
            C_130,
            E_3A,

            UH_1H,

            Unarmed.Transport_M818,
            Infantry.Infantry_M4,

            AirDefence.AAA_Vulcan_M163,

            CVN_74_John_C__Stennis,
            LHA_1_Tarawa,
            Armed_speedboat,
        ]
    },

    "USA 1965": {
        "country": "USA",
        "side": "blue",
        "units": [

            F_5E_3,
            F_4E,

            KC_135,
            S_3B_Tanker,
            C_130,
            E_3A,

            B_52H,

            UH_1H,

            Armor.MBT_M60A3_Patton,
            Armor.APC_M113,
            Unarmed.Transport_M818,
            Infantry.Infantry_M4,

            AirDefence.AAA_Vulcan_M163,
            AirDefence.SAM_Linebacker_M6,

            CVN_74_John_C__Stennis,
            LHA_1_Tarawa,
            Armed_speedboat,
        ]
    },

    "USA 1990": {
        "country":"USA",
        "side":"blue",
        "units":[
            F_15C,
            F_14B,
            FA_18C_hornet,

            A_10A,
            AV8BNA,

            B_1B,

            KC_135,
            S_3B_Tanker,
            C_130,
            E_3A,

            UH_1H,
            AH_64A,
            OH_58D,

            Armor.MBT_M1A2_Abrams,
            Armor.IFV_LAV_25,
            Armor.APC_M1043_HMMWV_Armament,
            Armor.ATGM_M1045_HMMWV_TOW,
            Armor.ATGM_M1134_Stryker,
            Unarmed.Transport_M818,
            Infantry.Infantry_M4,

            AirDefence.AAA_Vulcan_M163,
            AirDefence.SAM_Linebacker_M6,

            CVN_74_John_C__Stennis,
            LHA_1_Tarawa,
            Armed_speedboat,
        ]
    },

    "USA 2005": {
        "country": "USA",
        "side": "blue",
        "units": [
            F_15C,
            F_14B,
            FA_18C_hornet,
            F_16C_bl_52d,

            A_10C,
            AV8BNA,

            B_1B,

            KC_135,
            S_3B_Tanker,
            C_130,
            E_3A,

            UH_1H,
            AH_64D,
            OH_58D,

            Armor.MBT_M1A2_Abrams,
            Armor.ATGM_M1134_Stryker,
            Armor.IFV_M2A2_Bradley,

            Unarmed.Transport_M818,
            Infantry.Infantry_M4,

            AirDefence.AAA_Vulcan_M163,
            AirDefence.SAM_Linebacker_M6,

            CVN_74_John_C__Stennis,
            LHA_1_Tarawa,
            Armed_speedboat,
        ]
    },

    "France 1990": {
        "country": "France",
        "side": "blue",
        "units":[
            M_2000C,
            Mirage_2000_5,

            KC_135,
            S_3B_Tanker,
            C_130,
            E_3A,

            SA342M,

            Armor.MBT_Leclerc,
            Unarmed.Transport_M818,
            Infantry.Infantry_M4,

            AirDefence.SAM_Roland_ADS,

            CVN_74_John_C__Stennis,
            LHA_1_Tarawa,
            Armed_speedboat,
        ]
    },

    "Germany 1990": {
        "country": "Germany",
        "side": "blue",
        "units":[
            MiG_29G,
            Tornado_IDS,
            F_4E,

            KC_135,
            S_3B_Tanker,
            C_130,
            E_3A,

            UH_1H,
            SA342M,

            Armor.TPz_Fuchs,
            Armor.MBT_Leopard_1A3,
            Armor.MBT_Leopard_2,
            Unarmed.Transport_M818,
            Infantry.Infantry_M4,

            AirDefence.SPAAA_Gepard,
            AirDefence.SAM_Roland_ADS,

            CVN_74_John_C__Stennis,
            LHA_1_Tarawa,
            Armed_speedboat,
        ]
    },
}

CARRIER_TYPE_BY_PLANE = {
    FA_18C_hornet: CVN_74_John_C__Stennis,
    F_14B: CVN_74_John_C__Stennis,
    Ka_50: LHA_1_Tarawa,
    SA342M: LHA_1_Tarawa,
    UH_1H: LHA_1_Tarawa,
    Mi_8MT: LHA_1_Tarawa,
    AV8BNA: LHA_1_Tarawa,
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
        CAP: "AIM-120*4,AIM-9*2,AIM-7*2,Fuel",
        Escort: "AIM-120*4,AIM-9*2,AIM-7*2,Fuel",
        PinpointStrike: "MK-82*8,AIM-9*2,AIM-7,FLIR Pod,Fuel",
        AntishipStrike: "MK-82*8,AIM-9*2,AIM-7,FLIR Pod,Fuel",
    },

    F_14B: {
        CAP: "AIM-54A-MK47*4, AIM-7M*2, AIM-9M*2, XT*2",
        Escort: "AIM-54A-MK47*4, AIM-7M*2, AIM-9M*2, XT*2",
        CAS: "AIM-54A-MK60*1, AIM-7M*1, AIM-9M*2, XT*2, Mk-82*2, LANTIRN",
        GroundAttack: "AIM54, AIM-9M*2, XT*2, GBU-12*4, LANTIRN",
    },

    Su_25T: {
        CAS: "APU-8 Vikhr-M*2,Kh-25ML,R-73*2,SPPU-22*2,Mercury LLTV Pod,MPS-410",
    },

    Su_33: {
        CAP: "R-73*4,R-27R*2,R-27ER*6",
        Escort: "R-73*4,R-27R*2,R-27ER*6",
    },

    AJS37: {
        CAS: "CAS (75 GUN): RB-75*2, AKAN",
    },

    AV8BNA: {
        CAS: "AS 2",
    },

    A_10C: {
        CAS: "AGM-65D*2,AGM-65H*2,GBU-12*2,GBU-38*2,AIM-9*2,TGP,ECM,MK151*7",
        GroundAttack: "AGM-65K*2,GBU-12*8,AIM-9M*2.ECM,TGP",
    },

    Ka_50: {
        CAS: "12x9A4172, 40xS-8",
        GroundAttack: "12x9A4172, 40xS-8",
    },

    M_2000C: {
        CAP: "Combat Air Patrol",
        Escort: "Combat Air Patrol",
        GroundAttack: "MK-82S Heavy Strike",
    },

    MiG_21Bis: {
        CAP: "Patrol, medium range",
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
    "Gulf War - Fall [1990]": datetime(1990, 10, 1),
    "Modern - Winter [2010]": datetime(2010, 1, 1),
    "Modern - Spring [2010]": datetime(2010, 4, 1),
    "Modern - Summer [2010]": datetime(2010, 6, 1),
    "Modern - Fall [2010]": datetime(2010, 10, 1),
    "Georgian War [2008]": datetime(2008, 8, 7),
    "Syrian War [2011]": datetime(2011, 8, 7),
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

AssignedUnitsDict = typing.Dict[typing.Type[UnitType], typing.Tuple[int, int]]
TaskForceDict = typing.Dict[typing.Type[Task], AssignedUnitsDict]

StartingPosition = typing.Optional[typing.Union[ShipGroup, StaticGroup, Airport, Point]]


def unit_task(unit: UnitType) -> Task:
    for task, units in UNIT_BY_TASK.items():
        if unit in units:
            return task

    if unit in SAM_CONVERT:
        return unit_task(SAM_CONVERT[unit])

    print(unit.name + " cause issue")
    return None

def find_unittype(for_task: Task, country_name: str) -> typing.List[UnitType]:
    return [x for x in UNIT_BY_TASK[for_task] if x in FACTIONS[country_name]["units"]]


def unit_type_name(unit_type) -> str:
    return unit_type.id and unit_type.id or unit_type.name


def unit_type_from_name(name: str) -> UnitType:
    if name in vehicle_map:
        return vehicle_map[name]
    elif name in plane_map:
        return plane_map[name]
    elif name in ship_map:
        return ship_map[name]
    else:
        return None


def unit_type_of(unit: Unit) -> UnitType:
    if isinstance(unit, Vehicle):
        return vehicle_map[unit.type]
    elif isinstance(unit, Ship):
        return ship_map[unit.type]
    else:
        return unit.unit_type


def task_name(task) -> str:
    if task == AirDefence:
        return "AirDefence"
    elif task == Embarking:
        return "Transportation"
    else:
        return task.name


def choose_units(for_task: Task, factor: float, count: int, country: str) -> typing.Collection[UnitType]:
    suitable_unittypes = find_unittype(for_task, country)
    suitable_unittypes = [x for x in suitable_unittypes if x not in helicopter_map.values()]
    suitable_unittypes.sort(key=lambda x: PRICES[x])

    idx = int(len(suitable_unittypes) * factor)
    variety = int(count + count * factor / 2)

    index_start = min(idx, len(suitable_unittypes) - variety)
    index_end = min(idx + variety, len(suitable_unittypes))
    return list(set(suitable_unittypes[index_start:index_end]))


def unitdict_append(unit_dict: UnitsDict, unit_type: UnitType, count: int):
    unit_dict[unit_type] = unit_dict.get(unit_type, 0) + 1


def unitdict_merge(a: UnitsDict, b: UnitsDict) -> UnitsDict:
    b = b.copy()
    for k, v in a.items():
        b[k] = b.get(k, 0) + v

    return b


def unitdict_split(unit_dict: UnitsDict, count: int):
    buffer_dict = {}
    for unit_type, unit_count in unit_dict.items():
        for _ in range(unit_count):
            unitdict_append(buffer_dict, unit_type, 1)
            if sum(buffer_dict.values()) >= count:
                yield buffer_dict
                buffer_dict = {}

    if len(buffer_dict):
        yield buffer_dict


def unitdict_restrict_count(unit_dict: UnitsDict, total_count: int) -> UnitsDict:
    if total_count == 0:
        return {}

    groups = list(unitdict_split(unit_dict, total_count))
    if len(groups) > 0:
        return groups[0]
    else:
        return {}


def assigned_units_split(fd: AssignedUnitsDict) -> typing.Tuple[PlaneDict, PlaneDict]:
    return {k: v1 for k, (v1, v2) in fd.items()}, {k: v2 for k, (v1, v2) in fd.items()},


def assigned_units_from(d: PlaneDict) -> AssignedUnitsDict:
    return {k: (v, 0) for k, v in d.items()}


def assignedunits_split_to_count(dict: AssignedUnitsDict, count: int):
    buffer_dict = {}
    for unit_type, (unit_count, client_count) in dict.items():
        for _ in range(unit_count):
            new_count, new_client_count = buffer_dict.get(unit_type, (0, 0))

            new_count += 1

            if client_count > 0:
                new_client_count += 1
                client_count -= 1

            buffer_dict[unit_type] = new_count, new_client_count
            if new_count >= count:
                yield buffer_dict
                buffer_dict = {}

    if len(buffer_dict):
        yield buffer_dict


def unitdict_from(fd: AssignedUnitsDict) -> Dict:
    return {k: v1 for k, (v1, v2) in fd.items()}


def _validate_db():
    # check unit by task uniquity
    total_set = set()
    for t, unit_collection in UNIT_BY_TASK.items():
        for unit_type in set(unit_collection):
            assert unit_type not in total_set, "{} is duplicate for task {}".format(unit_type, t)
            total_set.add(unit_type)

    # check country allegiance
    for unit_type in total_set:
        did_find = False
        for country_units_list in FACTIONS.values():
            if unit_type in country_units_list["units"]:
                did_find = True
        print("WARN : {} not in country list".format(unit_type))

    # check prices
    for unit_type in total_set:
        assert unit_type in PRICES, "{} not in prices".format(unit_type)


_validate_db()
