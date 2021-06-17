from enum import unique, Enum
from typing import Type

from dcs.vehicles import AirDefence, Infantry, Unarmed, Artillery, Armor
from dcs.unittype import VehicleType

from pydcs_extensions.frenchpack import frenchpack


@unique
class GroundUnitClass(Enum):
    Tank = (
        "Tank",
        (
            Armor.T_55,
            Armor.T_72B,
            Armor.T_72B3,
            Armor.T_80UD,
            Armor.T_90,
            Armor.Leopard_2A4,
            Armor.Leopard_2A4_trs,
            Armor.Leopard_2A5,
            Armor.Leopard_2,
            Armor.Leopard1A3,
            Armor.Leclerc,
            Armor.Challenger2,
            Armor.Chieftain_mk3,
            Armor.M_1_Abrams,
            Armor.M_60,
            Armor.Merkava_Mk4,
            Armor.ZTZ96B,
            # WW2
            # Axis
            Armor.Pz_IV_H,
            Armor.SturmPzIV,
            Armor.Pz_V_Panther_G,
            Armor.Tiger_I,
            Armor.Tiger_II_H,
            # Allies
            Armor.M4_Sherman,
            Armor.Centaur_IV,
            Armor.Cromwell_IV,
            Armor.Churchill_VII,
            # Mods
            frenchpack.DIM__TOYOTA_BLUE,
            frenchpack.DIM__TOYOTA_GREEN,
            frenchpack.DIM__TOYOTA_DESERT,
            frenchpack.DIM__KAMIKAZE,
            frenchpack.AMX_30B2,
            frenchpack.Leclerc_Serie_XXI,
        ),
    )

    Atgm = (
        "ATGM",
        (
            Armor.M1043_HMMWV_Armament,
            Armor.VAB_Mephisto,
            Armor.M1134_Stryker_ATGM,
            Armor.BMP_2,
            # WW2 (Tank Destroyers)
            # Axxis
            Armor.Stug_III,
            Armor.Stug_IV,
            Armor.JagdPz_IV,
            Armor.Jagdpanther_G1,
            Armor.Elefant_SdKfz_184,
            # Allies
            Armor.M10_GMC,
            Armor.M4A4_Sherman_FF,
            # Mods
            frenchpack.VBAE_CRAB_MMP,
            frenchpack.VAB_MEPHISTO,
            frenchpack.TRM_2000_PAMELA,
        ),
    )

    Ifv = (
        "IFV",
        (
            Armor.BMP_3,
            Armor.BMP_2,
            Armor.BMP_1,
            Armor.Marder,
            Armor.MCV_80,
            Armor.M1128_Stryker_MGS,
            Armor.M_2_Bradley,
            Armor.BMD_1,
            Armor.ZBD04A,
            # Mods
            frenchpack.VBAE_CRAB,
            frenchpack.VAB_T20_13,
        ),
    )

    Apc = (
        "APC",
        (
            Armor.M1126_Stryker_ICV,
            Armor.M_113,
            Armor.BTR_80,
            Armor.BTR_82A,
            Armor.MTLB,
            Armor.AAV7,
            Armor.TPZ,
            Armor.BTR_D,
            # WW2
            Armor.M2A1_halftrack,
            Armor.Sd_Kfz_251,
            # Mods
            frenchpack.VAB__50,
            frenchpack.VBL__50,
            frenchpack.VBL_AANF1,
        ),
    )

    Artillery = (
        "Artillery",
        (
            Artillery.Grad_FDDM,
            Artillery.Smerch_HE,
            Artillery.SAU_Gvozdika,
            Artillery.SAU_Akatsia,
            Artillery.Grad_URAL,
            Artillery.Uragan_BM_27,
            Artillery.M_109,
            Artillery.MLRS,
            Artillery.SAU_2_C9,
            Artillery.SpGH_Dana,
            Artillery.T155_Firtina,
            Artillery.PLZ05,
            Artillery.SAU_Msta,
            Artillery.Smerch,
            # WW2
            Artillery.M12_GMC,
        ),
    )

    Logistics = (
        "Logistics",
        (
            Unarmed.M30_CC,
            Unarmed.M_818,
            Unarmed.KAMAZ_Truck,
            Unarmed.Ural_375,
            Unarmed.GAZ_66,
            Unarmed.GAZ_3307,
            Unarmed.GAZ_3308,
            Unarmed.Ural_4320_31,
            Unarmed.Ural_4320T,
            Unarmed.Blitz_36_6700A,
            Unarmed.Kubelwagen_82,
            Unarmed.Sd_Kfz_7,
            Unarmed.Sd_Kfz_2,
            Unarmed.Willys_MB,
            Unarmed.Land_Rover_109_S3,
            Unarmed.Land_Rover_101_FC,
            # Mods
            frenchpack.VBL,
            frenchpack.VAB,
        ),
    )

    Recon = (
        "Recon",
        (
            Armor.M1043_HMMWV_Armament,
            Armor.Cobra,
            Armor.PT_76,
            Armor.LAV_25,
            Armor.BRDM_2,
            # WW2
            Armor.Tetrarch,
            Armor.Sd_Kfz_234_2_Puma,
            Armor.M8_Greyhound,
            Armor.Daimler_AC,
            # Mods
            frenchpack.ERC_90,
            frenchpack.AMX_10RCR,
            frenchpack.AMX_10RCR_SEPAR,
        ),
    )

    Infantry = (
        "Infantry",
        (
            Infantry.Infantry_AK_Ins,
            Infantry.Soldier_AK,
            Infantry.Soldier_wwii_us,
            Infantry.Soldier_mauser98,
            Infantry.Soldier_wwii_br_01,
            Infantry.Soldier_M4_GRG,
            Infantry.Infantry_AK,
            Infantry.Paratrooper_AKS_74,
            Infantry.Paratrooper_RPG_16,
            Infantry.Soldier_M249,
            Infantry.Soldier_M4,
            Infantry.Soldier_RPG,
        ),
    )

    Shorads = (
        "SHORADS",
        (
            AirDefence.Ural_375_ZU_23,
            AirDefence.Ural_375_ZU_23_Insurgent,
            AirDefence.ZSU_57_2,
            AirDefence.ZSU_23_4_Shilka,
            AirDefence.Osa_9A33_ln,
            AirDefence.Strela_1_9P31,
            AirDefence.Strela_10M3,
            AirDefence.Tor_9A331,
            AirDefence._2S6_Tunguska,
            AirDefence.Gepard,
            AirDefence.Vulcan,
            AirDefence.M6_Linebacker,
            AirDefence.M48_Chaparral,
            AirDefence.M1097_Avenger,
            AirDefence.Roland_ADS,
            AirDefence.HQ_7_LN_SP,
            AirDefence.Flak18,
            AirDefence.Flak36,
            AirDefence.Flak37,
            AirDefence.Flak41,
            AirDefence.Bofors40,
            AirDefence.S_60_Type59_Artillery,
            AirDefence.M1_37mm,
            AirDefence.QF_37_AA,
        ),
    )

    def __init__(
        self, class_name: str, unit_list: tuple[Type[VehicleType], ...]
    ) -> None:
        self.class_name = class_name
        self.unit_list = unit_list

    def __contains__(self, unit_type: Type[VehicleType]) -> bool:
        return unit_type in self.unit_list
