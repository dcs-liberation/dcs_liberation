from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

import pydcs_extensions.frenchpack.frenchpack as frenchpack
from pydcs_extensions.rafale.rafale import Rafale_M, Rafale_A_S

France_2005_Modded = {
    "country": "France",
    "side": "blue",
    "units": [
        M_2000C,
        Mirage_2000_5,
        Rafale_M,
        Rafale_A_S,

        KC_135,
        KC130,
        C_130,
        E_3A,

        SA342M,
        SA342L,

        Armor.MBT_Leclerc,
        Artillery.SPH_M109_Paladin,  # Standing as AMX30 AuF1
        Artillery.MLRS_M270,

        frenchpack.AMX_10RCR,
        frenchpack.AMX_10RCR_SEPAR,
        frenchpack.ERC_90,
        frenchpack.TRM_2000_PAMELA,
        frenchpack.VAB__50,
        frenchpack.VAB_MEPHISTO,
        frenchpack.VAB_T20_13,
        frenchpack.VBL__50,
        frenchpack.VBL_AANF1,
        frenchpack.VBAE_CRAB,
        frenchpack.VBAE_CRAB_MMP,
        frenchpack.AMX_30B2,
        frenchpack.Leclerc_Serie_XXI,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.SAM_Roland_ADS,
        AirDefence.SAM_Hawk_PCP,
        AirDefence.HQ_7_Self_Propelled_LN,  # Standing as Crotale

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,

    ], "shorad": [
        AirDefence.HQ_7_Self_Propelled_LN,
        AirDefence.SAM_Roland_ADS
    ], "aircraft_carrier": [
        CVN_74_John_C__Stennis,  # Standing as CDG Aircraft Carrier
    ], "helicopter_carrier": [
        LHA_1_Tarawa,  # Standing as Mistral Class
    ], "destroyer": [
        Oliver_Hazzard_Perry_class,
    ], "cruiser": [
        Ticonderoga_class,
    ], "carrier_names": [
        "R91 Charles de Gaulle",
    ], "lhanames": [
        "L9013 Mistral",
        "L9014 Tonerre",
        "L9015 Dixmude"
    ], "boat": [
        "ArleighBurkeGroupGenerator", "OliverHazardPerryGroupGenerator"
    ], "requirements": {
        "frenchpack V3.5": "https://forums.eagle.ru/showthread.php?t=279974",
        "RAFALE 2.5.5": "https://www.digitalcombatsimulator.com/fr/files/3307478/",
    }
}