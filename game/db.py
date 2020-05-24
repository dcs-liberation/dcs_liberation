import typing
import enum
from datetime import datetime

from dcs.countries import get_by_id, country_dict
from dcs.vehicles import *
from dcs.ships import *
from dcs.planes import *
from dcs.helicopters import *

from dcs.task import *
from dcs.unit import *
from dcs.unittype import *
from dcs.unitgroup import *

from game.factions.china_2000 import China_2000
from game.factions.france_1995 import France_1995
from game.factions.germany_1990 import Germany_1990
from game.factions.insurgent import Insurgent
from game.factions.iran_2015 import Iran_2015
from game.factions.israel_2000 import Israel_2000
from game.factions.italy_1990 import Italy_1990
from game.factions.netherlands_1990 import Netherlands_1990
from game.factions.north_korea_2000 import NorthKorea_2000
from game.factions.pakistan_2015 import Pakistan_2015
from game.factions.russia_1975 import Russia_1975
from game.factions.germany_1944 import Germany_1944
from game.factions.india_2010 import India_2010
from game.factions.russia_1955 import Russia_1955
from game.factions.russia_1965 import Russia_1965
from game.factions.russia_1990 import Russia_1990
from game.factions.russia_2010 import Russia_2010
from game.factions.spain_1990 import Spain_1990
from game.factions.sweden_1990 import Sweden_1990
from game.factions.turkey_2005 import Turkey_2005
from game.factions.uae_2005 import UAE_2005
from game.factions.uk_1990 import UnitedKingdom_1990
from game.factions.ukraine_2010 import Ukraine_2010
from game.factions.usa_1944 import USA_1944
from game.factions.usa_1955 import USA_1955
from game.factions.usa_1960 import USA_1960
from game.factions.usa_1965 import USA_1965
from game.factions.usa_1990 import USA_1990
from game.factions.usa_2005 import USA_2005

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
    JF_17: 20,
    Su_30: 24,
    SpitfireLFMkIX:3,
    SpitfireLFMkIXCW:3,
    Bf_109K_4:3,
    FW_190D9:3,
    FW_190A8:3,

    F_5E_3: 8,
    MiG_15bis: 4,
    MiG_19P: 6,
    F_86F_Sabre: 4,
    MiG_21Bis: 8,
    F_4E: 10,
    AJS37: 12,
    C_101CC: 6,

    AV8BNA: 14,
    M_2000C: 16,
    Mirage_2000_5: 22,
    FA_18C_hornet: 24,
    F_15C: 26,
    F_16C_50: 20,
    F_14B: 22,
    Tornado_IDS: 24,
    Tornado_GR4: 24,

    # bomber
    Su_17M4: 10,
    Su_25: 15,
    Su_25T: 18,
    L_39ZA: 10,
    Su_34: 24,
    Su_24M: 20,
    Su_24MR: 24,
    MiG_27K: 20,

    A_10A: 16,
    A_10C: 22,

    # heli
    Ka_50: 13,
    SA342M: 8,
    SA342L: 5,
    UH_1H: 4,
    Mi_8MT: 5,
    Mi_24V: 12,
    Mi_28N: 16,
    AH_1W: 10,
    AH_64A: 12,
    AH_64D: 16,
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
    Armor.IFV_BMP_3: 18,
    Armor.ZBD_04A: 12,
    Armor.ZTZ_96B: 35,

    Armor.APC_Cobra: 4,
    Armor.APC_M113: 6,
    Armor.APC_M1043_HMMWV_Armament: 2,
    Armor.ATGM_M1045_HMMWV_TOW: 8,
    Armor.IFV_M2A2_Bradley: 12,
    Armor.APC_M1126_Stryker_ICV: 10,
    Armor.ATGM_M1134_Stryker: 12,
    Armor.MBT_M60A3_Patton: 18,
    Armor.MBT_M1A2_Abrams: 35,
    Armor.MBT_Leclerc: 35,
    Armor.MBT_Leopard_1A3: 24,
    Armor.MBT_Leopard_2: 35,
    Armor.MBT_Merkava_Mk__4: 35,
    Armor.TPz_Fuchs: 5,
    Armor.MBT_Challenger_II: 30,
    Armor.IFV_Marder: 10,
    Armor.IFV_MCV_80: 10,

    Artillery.MLRS_M270: 55,
    Artillery.SPH_M109_Paladin: 25,

    Artillery.SPH_2S9_Nona: 12,
    Artillery.SPH_2S1_Gvozdika: 18,
    Artillery.SPH_2S3_Akatsia: 24,
    Artillery.SPH_2S19_Msta: 30,
    Artillery.MLRS_BM_21_Grad: 15,
    Artillery.MLRS_9K57_Uragan_BM_27: 40,
    Artillery.MLRS_9A52_Smerch: 40,

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
    AirDefence.SAM_Patriot_LN_M901: 60,
    AirDefence.SAM_SA_10_S_300PS_LN_5P85C: 60,
    AirDefence.SAM_Chaparral_M48: 10,

    # WW2
    Armor.MT_Pz_Kpfw_V_Panther_Ausf_G:7,
    Armor.MT_Pz_Kpfw_IV_Ausf_H:4,
    Armor.HT_Pz_Kpfw_VI_Tiger_I:10,
    Armor.HT_Pz_Kpfw_VI_Ausf__B__Tiger_II:12,
    Armor.APC_Sd_Kfz_251:3,
    Armor.IFV_Sd_Kfz_234_2_Puma:4,
    Armor.MT_M4_Sherman:4,
    Armor.MT_M4A4_Sherman_Firefly:6,
    Armor.CT_Cromwell_IV:8,
    Armor.M30_Cargo_Carrier:2,
    Armor.APC_M2A1:2,
    AirDefence.AAA_Bofors_40mm:4,
    AirDefence.AAA_Flak_36:6,
    AirDefence.AAA_Flak_18:4,
    Artillery.M12_GMC:2,
    Artillery.Sturmpanzer_IV_Brummbär:2,

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
        F_16C_50,
        M_2000C,
        Mirage_2000_5,
        P_51D_30_NA,
        P_51D,
        MiG_29G,
        Su_30,
        J_11A,
        JF_17,
        F_4E,
        C_101CC,
        Bf_109K_4,
        FW_190D9,
        FW_190A8,
        SpitfireLFMkIXCW,
        SpitfireLFMkIX
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
        SA342M,
        SA342L,
        Su_24M,
        Su_24MR,
        AH_64A,
        AH_64D,
        OH_58D,
        B_52H,
        B_1B,
        Tornado_IDS,
        Tornado_GR4,
        UH_1H,
        Mi_8MT,
        Mi_28N,
        Mi_24V,
        MiG_27K,
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
        Armor.ARV_BTR_RD,
        Armor.ARV_BTR_RD,
        Armor.ARV_BTR_RD,
        Armor.ARV_BTR_RD,
        Armor.APC_BTR_80,
        Armor.APC_BTR_80,
        Armor.APC_BTR_80,
        Armor.APC_BTR_80,
        Armor.APC_BTR_80,
        Armor.IFV_BMP_1,
        Armor.IFV_BMP_1,
        Armor.IFV_BMP_1,
        Armor.IFV_BMP_2,
        Armor.IFV_BMP_2,
        Armor.IFV_BMP_3,
        Armor.IFV_BMP_3,
        Armor.ZBD_04A,
        Armor.ZBD_04A,
        Armor.ZBD_04A,
        Armor.MBT_T_55,
        Armor.MBT_T_55,
        Armor.MBT_T_55,
        Armor.MBT_T_72B,
        Armor.MBT_T_72B,
        Armor.MBT_T_80U,
        Armor.MBT_T_80U,
        Armor.MBT_T_90,
        Armor.ZTZ_96B,

        Armor.APC_Cobra,
        Armor.APC_Cobra,
        Armor.APC_Cobra,
        Armor.APC_Cobra,
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
        Armor.APC_M1126_Stryker_ICV,
        Armor.APC_M1126_Stryker_ICV,
        Armor.APC_M1126_Stryker_ICV,
        Armor.IFV_MCV_80,
        Armor.IFV_MCV_80,
        Armor.IFV_MCV_80,
        Armor.IFV_Marder,
        Armor.IFV_Marder,
        Armor.IFV_Marder,
        Armor.IFV_Marder,
        Armor.MBT_M60A3_Patton,
        Armor.MBT_M60A3_Patton,
        Armor.MBT_M60A3_Patton,
        Armor.MBT_Leopard_1A3,
        Armor.MBT_Leopard_1A3,
        Armor.MBT_M1A2_Abrams,
        Armor.MBT_Leclerc,
        Armor.MBT_Leopard_2,
        Armor.MBT_Challenger_II,
        Armor.MBT_Merkava_Mk__4,

        Armor.MT_Pz_Kpfw_V_Panther_Ausf_G,
        Armor.MT_Pz_Kpfw_IV_Ausf_H,
        Armor.HT_Pz_Kpfw_VI_Tiger_I,
        Armor.HT_Pz_Kpfw_VI_Ausf__B__Tiger_II,
        Armor.APC_Sd_Kfz_251,
        Armor.APC_Sd_Kfz_251,
        Armor.APC_Sd_Kfz_251,
        Armor.APC_Sd_Kfz_251,
        Armor.IFV_Sd_Kfz_234_2_Puma,
        Armor.IFV_Sd_Kfz_234_2_Puma,
        Armor.MT_M4_Sherman,
        Armor.MT_M4A4_Sherman_Firefly,
        Armor.CT_Cromwell_IV,
        Armor.M30_Cargo_Carrier,
        Armor.M30_Cargo_Carrier,
        Armor.APC_M2A1,
        Armor.APC_M2A1,
        Armor.APC_M2A1,
        Armor.APC_M2A1,

        Artillery.MLRS_M270,
        Artillery.SPH_M109_Paladin,
        Artillery.SPH_2S9_Nona,
        Artillery.SPH_2S1_Gvozdika,
        Artillery.SPH_2S3_Akatsia,
        Artillery.SPH_2S19_Msta,
        Artillery.MLRS_BM_21_Grad,
        Artillery.MLRS_BM_21_Grad,
        Artillery.MLRS_9K57_Uragan_BM_27,
        Artillery.MLRS_9A52_Smerch,
        Artillery.M12_GMC,
        Artillery.Sturmpanzer_IV_Brummbär,

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
    Embarking: [],
    Carriage: [CVN_74_John_C__Stennis, LHA_1_Tarawa, CV_1143_5_Admiral_Kuznetsov, ],
    CargoTransportation: [Dry_cargo_ship_Ivanov, Bulk_cargo_ship_Yakushev, Tanker_Elnya_160, Armed_speedboat, ]
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
    "Iran": AirDefence.SPAAA_ZSU_23_4_Shilka,
    "North Korea": AirDefence.AAA_ZU_23_Closed,
    "Italy": AirDefence.AAA_Vulcan_M163,
    "Spain": AirDefence.AAA_Vulcan_M163,
    "The Netherlands": AirDefence.AAA_Vulcan_M163,
    "Turkey": AirDefence.AAA_Vulcan_M163,
    "Israel": AirDefence.AAA_Vulcan_M163,
    "India": AirDefence.SPAAA_ZSU_23_4_Shilka,
    "United Arab Emirates": AirDefence.Stinger_MANPADS,
    "Insurgents": AirDefence.AAA_ZU_23_Insurgent_on_Ural_375,
    "Third Reich": AirDefence.AAA_Flak_Vierling_38,
}

"""
Units separated by country. Currently only Russia and USA are supported. 
country : DCS Country name
"""
FACTIONS = {
    "Russia 1955": Russia_1955,
    "Russia 1965": Russia_1965,
    "Russia 1975": Russia_1975,
    "Russia 1990": Russia_1990,
    "Russia 2010": Russia_2010,
    "Iran 2015": Iran_2015,
    "China 2000": China_2000,
    "North Korea 2000": NorthKorea_2000,
    "Insurgent": Insurgent,

    "USA 2005": USA_2005,
    "USA 1990": USA_1990,
    "USA 1965": USA_1965,
    "USA 1960": USA_1960,
    "USA 1955 (Require WW2 Pack)": USA_1955,
    "USA 1944 (Require WW2 Pack)": USA_1944,
    "France 1995": France_1995,
    "Germany 1990": Germany_1990,
    "Netherlands 1990": Netherlands_1990,
    "United Kingdown 1990": UnitedKingdom_1990,
    "Spain 1990": Spain_1990,
    "Italy 1990": Italy_1990,
    "Sweden 1990": Sweden_1990,
    "Ukraine 2010": Ukraine_2010,
    "India 2010": India_2010,
    "Pakistan 2015": Pakistan_2015,
    "Israel 2000": Israel_2000,
    "Turkey 2005": Turkey_2005,
    "United Arab Emirates 2005": UAE_2005,
    "Germany 1944 (Require WW2 Pack)": Germany_1944
}
BLUEFOR_FACTIONS = [FACTIONS[f]["country"] for f in FACTIONS if FACTIONS[f]["side"] == "blue"]
print(BLUEFOR_FACTIONS)


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
        CAS: "AIM-9M*2,AGM-65D*2,Mk-82*4,FLIR Pod,Fuel",
        CAP: "AIM-120*4,AIM-9*2,AIM-7*2,Fuel",
        Escort: "AIM-120*4,AIM-9*2,AIM-7*2,Fuel",
        PinpointStrike: "MK-82*8,AIM-9*2,AIM-7,FLIR Pod,Fuel",
        AntishipStrike: "MK-82*8,AIM-9*2,AIM-7,FLIR Pod,Fuel",
        SEAD: "AGM-88*2,AIM-9*2,AIM-7,FLIR Pod,Fuel*3"
    },

    JF_17: {
        CAS: "PL-5Ex2, 2*SD-10x2, 800L Tank",
        CAP: "PL-5Ex2, 2*GBU-12x2, BRM1x2, WMD7",
        SEAD: "PL-5Ex2, LD-10x2, 1100L Tankx2, WMD7"
    },

    F_14B: {
        CAP: "AIM-54A-MK47*4, AIM-7M*2, AIM-9M*2, XT*2",
        Escort: "AIM-54A-MK47*4, AIM-7M*2, AIM-9M*2, XT*2",
        CAS: "AIM-54A-MK60*1, AIM-7M*1, AIM-9M*2, XT*2, Mk-82*2, LANTIRN",
        GroundAttack: "AIM54, AIM-9M*2, XT*2, GBU-12*4, LANTIRN",
    },

    Su_25T: {
        CAS: "APU-8 Vikhr-M*2,Kh-25ML,R-73*2,SPPU-22*2,Mercury LLTV Pod,MPS-410",
        SEAD: "Kh58*2_Kh25MPU*2_Kh25ML*2_R73*2_L-081_MPS-410"
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
        SEAD: "Stand Off 2"
    },

    AH_64D:{
        CAS: "AGM-114K*16"
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

    Mirage_2000_5: {
        CAP: "R 550*2,MICA IR*2,MICA AR*2,Fuel*3",
    },

    MiG_21Bis: {
        CAP: "Patrol, medium range",
    },

    Su_24M: {
        CAS: "S-24*6",
        SEAD: "Kh25MPU*2_Kh25ML*2_L-081"
    },

    Su_25TM: {
        SEAD: "Kh-31P*2_Kh-25ML*4_R-73*2_L-081_MPS410",
    },

    Su_17M4: {
        CAS: "Kh-25MR*4,R-60M*2,Fuel*2",
        SEAD: "Kh25MPU*2_Kh25ML*2_,R60M*2_Fuel*2"
    },

    Su_30: {
        SEAD: "Kh-31P*4,R-73*2,R-77*2,ECM",
    },

    Su_34: {
        SEAD: "Kh-25MPU*6,R-73*2,R-77*2,ECM",
    },

    MiG_27K: {
        SEAD: "Kh-25MPU*2,R-60M*2,Fuel"
    },

    F_4E: {
        SEAD: "AGM-45*4,AIM-7*2,ECM"
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

CARRIER_CAPABLE = [
    FA_18C_hornet,
    F_14B,
    AV8BNA,

    UH_1H,
    Mi_8MT,
    Ka_50,

    SA342L,
    SA342M,
    SA342Minigun,
    SA342Mistral
]

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

def find_infantry(country_name: str) -> typing.List[UnitType]:
    inf = [
        Infantry.Paratrooper_AKS, Infantry.Paratrooper_AKS, Infantry.Paratrooper_AKS, Infantry.Paratrooper_AKS, Infantry.Paratrooper_AKS,
        Infantry.Soldier_RPG,
        Infantry.Infantry_M4, Infantry.Infantry_M4, Infantry.Infantry_M4, Infantry.Infantry_M4, Infantry.Infantry_M4,
        Infantry.Soldier_M249,
        Infantry.Soldier_AK, Infantry.Soldier_AK, Infantry.Soldier_AK, Infantry.Soldier_AK, Infantry.Soldier_AK,
        Infantry.Paratrooper_RPG_16,
        Infantry.Georgian_soldier_with_M4, Infantry.Georgian_soldier_with_M4, Infantry.Georgian_soldier_with_M4, Infantry.Georgian_soldier_with_M4,
        Infantry.Infantry_Soldier_Rus, Infantry.Infantry_Soldier_Rus, Infantry.Infantry_Soldier_Rus, Infantry.Infantry_Soldier_Rus,
        Infantry.Infantry_SMLE_No_4_Mk_1, Infantry.Infantry_SMLE_No_4_Mk_1, Infantry.Infantry_SMLE_No_4_Mk_1,
        Infantry.Infantry_Mauser_98, Infantry.Infantry_Mauser_98, Infantry.Infantry_Mauser_98, Infantry.Infantry_Mauser_98,
        Infantry.Infantry_M1_Garand, Infantry.Infantry_M1_Garand, Infantry.Infantry_M1_Garand,
        Infantry.Infantry_Soldier_Insurgents, Infantry.Infantry_Soldier_Insurgents, Infantry.Infantry_Soldier_Insurgents
    ]
    return [x for x in inf if x in FACTIONS[country_name]["units"]]

def unit_type_name(unit_type) -> str:
    return unit_type.id and unit_type.id or unit_type.name


def unit_type_from_name(name: str) -> UnitType:
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


def unit_type_of(unit: Unit) -> UnitType:
    if isinstance(unit, Vehicle):
        return vehicle_map[unit.type]
    elif isinstance(unit, Ship):
        return ship_map[unit.type]
    else:
        return unit.type


def task_name(task) -> str:
    if task == AirDefence:
        return "AirDefence"
    elif task == Embarking:
        return "Transportation"
    elif task == PinpointStrike:
        return "Frontline units"
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


def country_id_from_name(name):
    for k,v in country_dict.items():
        if v.name == name:
            return k
    return -1


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

class DefaultLiveries:
    class Default(Enum):
        af_standard = ""

OH_58D.Liveries = DefaultLiveries
F_16C_50.Liveries = DefaultLiveries
P_51D_30_NA.Liveries = DefaultLiveries