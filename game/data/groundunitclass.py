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
            Armor.MBT_T_55,
            Armor.MBT_T_72B,
            Armor.MBT_T_72B3,
            Armor.MBT_T_80U,
            Armor.MBT_T_90,
            Armor.MBT_Leopard_2A4,
            Armor.MBT_Leopard_2A4_Trs,
            Armor.MBT_Leopard_2A5,
            Armor.MBT_Leopard_2A6M,
            Armor.MBT_Leopard_1A3,
            Armor.MBT_Leclerc,
            Armor.MBT_Challenger_II,
            Armor.MBT_Chieftain_Mk_3,
            Armor.MBT_M1A2_Abrams,
            Armor.MBT_M60A3_Patton,
            Armor.MBT_Merkava_IV,
            Armor.ZTZ_96B,
            # WW2
            # Axis
            Armor.Tk_PzIV_H,
            Armor.SPG_Sturmpanzer_IV_Brummbar,
            Armor.MT_Pz_Kpfw_V_Panther_Ausf_G,
            Armor.HT_Pz_Kpfw_VI_Tiger_I,
            Armor.HT_Pz_Kpfw_VI_Ausf__B_Tiger_II,
            # Allies
            Armor.Tk_M4_Sherman,
            Armor.CT_Centaur_IV,
            Armor.CT_Cromwell_IV,
            Armor.HIT_Churchill_VII,
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
            Armor.ATGM_HMMWV,
            Armor.ATGM_VAB_Mephisto,
            Armor.ATGM_Stryker,
            Armor.IFV_BMP_2,
            # WW2 (Tank Destroyers)
            # Axxis
            Armor.SPG_StuG_III_Ausf__G,
            Armor.SPG_StuG_IV,
            Armor.SPG_Jagdpanzer_IV,
            Armor.SPG_Jagdpanther_G1,
            Armor.SPG_Sd_Kfz_184_Elefant,
            # Allies
            Armor.SPG_M10_GMC,
            Armor.MT_M4A4_Sherman_Firefly,
            # Mods
            frenchpack.VBAE_CRAB_MMP,
            frenchpack.VAB_MEPHISTO,
            frenchpack.TRM_2000_PAMELA,
        ),
    )

    Ifv = (
        "IFV",
        (
            Armor.IFV_BMP_3,
            Armor.IFV_BMP_2,
            Armor.IFV_BMP_1,
            Armor.IFV_Marder,
            Armor.IFV_Warrior,
            Armor.SPG_Stryker_MGS,
            Armor.IFV_M2A2_Bradley,
            Armor.IFV_BMD_1,
            Armor.ZBD_04A,
            # Mods
            frenchpack.VBAE_CRAB,
            frenchpack.VAB_T20_13,
        ),
    )

    Apc = (
        "APC",
        (
            Armor.IFV_M1126_Stryker_ICV,
            Armor.APC_M113,
            Armor.APC_BTR_80,
            Armor.IFV_BTR_82A,
            Armor.APC_MTLB,
            Armor.APC_AAV_7_Amphibious,
            Armor.APC_TPz_Fuchs,
            Armor.APC_BTR_RD,
            # WW2
            Armor.APC_M2A1_Halftrack,
            Armor.APC_Sd_Kfz_251_Halftrack,
            # Mods
            frenchpack.VAB__50,
            frenchpack.VBL__50,
            frenchpack.VBL_AANF1,
        ),
    )

    Artillery = (
        "Artillery",
        (
            Artillery.Grad_MRL_FDDM__FC,
            Artillery.MLRS_9A52_Smerch_HE_300mm,
            Artillery.SPH_2S1_Gvozdika_122mm,
            Artillery.SPH_2S3_Akatsia_152mm,
            Artillery.MLRS_BM_21_Grad_122mm,
            Artillery.MLRS_9K57_Uragan_BM_27_220mm,
            Artillery.SPH_M109_Paladin_155mm,
            Artillery.MLRS_M270_227mm,
            Artillery.SPM_2S9_Nona_120mm_M,
            Artillery.SPH_Dana_vz77_152mm,
            Artillery.SPH_T155_Firtina_155mm,
            Artillery.PLZ_05,
            Artillery.SPH_2S19_Msta_152mm,
            Artillery.MLRS_9A52_Smerch_CM_300mm,
            # WW2
            Artillery.SPG_M12_GMC_155mm,
        ),
    )

    Logistics = (
        "Logistics",
        (
            Unarmed.Carrier_M30_Cargo,
            Unarmed.Truck_M818_6x6,
            Unarmed.Truck_KAMAZ_43101,
            Unarmed.Truck_Ural_375,
            Unarmed.Truck_GAZ_66,
            Unarmed.Truck_GAZ_3307,
            Unarmed.Truck_GAZ_3308,
            Unarmed.Truck_Ural_4320_31_Arm_d,
            Unarmed.Truck_Ural_4320T,
            Unarmed.Truck_Opel_Blitz,
            Unarmed.LUV_Kubelwagen_82,
            Unarmed.Carrier_Sd_Kfz_7_Tractor,
            Unarmed.LUV_Kettenrad,
            Unarmed.Car_Willys_Jeep,
            Unarmed.LUV_Land_Rover_109,
            Unarmed.Truck_Land_Rover_101_FC,
            # Mods
            frenchpack.VBL,
            frenchpack.VAB,
        ),
    )

    Recon = (
        "Recon",
        (
            Armor.Scout_HMMWV,
            Armor.Scout_Cobra,
            Armor.LT_PT_76,
            Armor.IFV_LAV_25,
            Armor.Scout_BRDM_2,
            # WW2
            Armor.LT_Mk_VII_Tetrarch,
            Armor.IFV_Sd_Kfz_234_2_Puma,
            Armor.Car_M8_Greyhound_Armored,
            Armor.Car_Daimler_Armored,
            # Mods
            frenchpack.ERC_90,
            frenchpack.AMX_10RCR,
            frenchpack.AMX_10RCR_SEPAR,
        ),
    )

    Infantry = (
        "Infantry",
        (
            Infantry.Insurgent_AK_74,
            Infantry.Infantry_AK_74,
            Infantry.Infantry_M1_Garand,
            Infantry.Infantry_Mauser_98,
            Infantry.Infantry_SMLE_No_4_Mk_1,
            Infantry.Infantry_M4_Georgia,
            Infantry.Infantry_AK_74_Rus,
            Infantry.Paratrooper_AKS,
            Infantry.Paratrooper_RPG_16,
            Infantry.Infantry_M249,
            Infantry.Infantry_M4,
            Infantry.Infantry_RPG,
        ),
    )

    Shorads = (
        "SHORADS",
        (
            AirDefence.SPAAA_ZU_23_2_Mounted_Ural_375,
            AirDefence.SPAAA_ZU_23_2_Insurgent_Mounted_Ural_375,
            AirDefence.SPAAA_ZSU_57_2,
            AirDefence.SPAAA_ZSU_23_4_Shilka_Gun_Dish,
            AirDefence.SAM_SA_8_Osa_Gecko_TEL,
            AirDefence.SAM_SA_9_Strela_1_Gaskin_TEL,
            AirDefence.SAM_SA_13_Strela_10M3_Gopher_TEL,
            AirDefence.SAM_SA_15_Tor_Gauntlet,
            AirDefence.SAM_SA_19_Tunguska_Grison,
            AirDefence.SPAAA_Gepard,
            AirDefence.SPAAA_Vulcan_M163,
            AirDefence.SAM_Linebacker___Bradley_M6,
            AirDefence.SAM_Chaparral_M48,
            AirDefence.SAM_Avenger__Stinger,
            AirDefence.SAM_Roland_ADS,
            AirDefence.HQ_7_Self_Propelled_LN,
            AirDefence.AAA_8_8cm_Flak_18,
            AirDefence.AAA_8_8cm_Flak_36,
            AirDefence.AAA_8_8cm_Flak_37,
            AirDefence.AAA_8_8cm_Flak_41,
            AirDefence.AAA_Bofors_40mm,
            AirDefence.AAA_S_60_57mm,
            AirDefence.AAA_M1_37mm,
            AirDefence.AAA_QF_3_7,
        ),
    )

    def __init__(
        self, class_name: str, unit_list: tuple[Type[VehicleType], ...]
    ) -> None:
        self.class_name = class_name
        self.unit_list = unit_list

    def __contains__(self, unit_type: Type[VehicleType]) -> bool:
        return unit_type in self.unit_list
