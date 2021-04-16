from dcs.vehicles import AirDefence, Infantry, Unarmed, Artillery, Armor

from pydcs_extensions.frenchpack import frenchpack

TYPE_TANKS = [
    Armor.MBT_T_55,
    Armor.MBT_T_72B,
    Armor.MBT_T_72B3,
    Armor.MBT_T_80U,
    Armor.MBT_T_90,
    Armor.MBT_Leopard_2,
    Armor.MBT_Leopard_1A3,
    Armor.MBT_Leclerc,
    Armor.MBT_Challenger_II,
    Armor.MBT_M1A2_Abrams,
    Armor.MBT_M60A3_Patton,
    Armor.MBT_Merkava_IV,
    Armor.ZTZ_96B,
    # WW2
    Armor.MT_Pz_Kpfw_V_Panther_Ausf_G,
    Armor.MT_PzIV_H,
    Armor.HT_Pz_Kpfw_VI_Tiger_I,
    Armor.HT_Pz_Kpfw_VI_Ausf__B_Tiger_II,
    Armor.MT_M4_Sherman,
    Armor.MT_M4A4_Sherman_Firefly,
    Armor.SPG_StuG_IV,
    Armor.CT_Centaur_IV,
    Armor.CT_Cromwell_IV,
    Armor.HIT_Churchill_VII,
    Armor.LT_Mk_VII_Tetrarch,
    # Mods
    frenchpack.DIM__TOYOTA_BLUE,
    frenchpack.DIM__TOYOTA_GREEN,
    frenchpack.DIM__TOYOTA_DESERT,
    frenchpack.DIM__KAMIKAZE,
    frenchpack.AMX_10RCR,
    frenchpack.AMX_10RCR_SEPAR,
    frenchpack.AMX_30B2,
    frenchpack.Leclerc_Serie_XXI,
]

TYPE_ATGM = [
    Armor.ATGM_HMMWV,
    Armor.ATGM_Stryker,
    Armor.IFV_BMP_2,
    # WW2 (Tank Destroyers)
    Unarmed.Carrier_M30_Cargo,
    Armor.SPG_Jagdpanzer_IV,
    Armor.SPG_Jagdpanther_G1,
    Armor.SPG_M10_GMC,
    # Mods
    frenchpack.VBAE_CRAB_MMP,
    frenchpack.VAB_MEPHISTO,
    frenchpack.TRM_2000_PAMELA,
]

TYPE_IFV = [
    Armor.IFV_BMP_3,
    Armor.IFV_BMP_2,
    Armor.IFV_BMP_1,
    Armor.IFV_Marder,
    Armor.IFV_Warrior,
    Armor.IFV_LAV_25,
    Armor.SPG_Stryker_MGS,
    Armor.IFV_Sd_Kfz_234_2_Puma,
    Armor.IFV_M2A2_Bradley,
    Armor.IFV_BMD_1,
    Armor.ZBD_04A,
    # WW2
    Armor.IFV_Sd_Kfz_234_2_Puma,
    Armor.Car_M8_Greyhound_Armored,
    Armor.Car_Daimler_Armored,
    # Mods
    frenchpack.ERC_90,
    frenchpack.VBAE_CRAB,
    frenchpack.VAB_T20_13,
]

TYPE_APC = [
    Armor.APC_HMMWV__Scout,
    Armor.IFV_M1126_Stryker_ICV,
    Armor.APC_M113,
    Armor.APC_BTR_80,
    Armor.APC_BTR_82A,
    Armor.APC_MTLB,
    Armor.APC_M2A1_Halftrack,
    Armor.APC_Cobra__Scout,
    Armor.APC_Sd_Kfz_251_Halftrack,
    Armor.APC_AAV_7,
    Armor.APC_TPz_Fuchs,
    Armor.IFV_BRDM_2,
    Armor.APC_BTR_RD,
    Artillery.Grad_MRL_FDDM__FC,
    # WW2
    Armor.APC_M2A1_Halftrack,
    Armor.APC_Sd_Kfz_251_Halftrack,
    # Mods
    frenchpack.VAB__50,
    frenchpack.VBL__50,
    frenchpack.VBL_AANF1,
]

TYPE_ARTILLERY = [
    Artillery.MLRS_9A52_Smerch_HE_300mm,
    Artillery.SPH_2S1_Gvozdika_122mm,
    Artillery.SPH_2S3_Akatsia_152mm,
    Artillery.MLRS_BM_21_Grad_122mm,
    Artillery.MLRS_BM_27_Uragan_220mm,
    Artillery.SPH_M109_Paladin_155mm,
    Artillery.MLRS_M270_227mm,
    Artillery.SPH_2S9_Nona_120mm_M,
    Artillery.SPH_Dana_vz77_152mm,
    Artillery.SPH_2S19_Msta_152mm,
    Artillery.MLRS_FDDM,
    # WW2
    Artillery.SPG_Sturmpanzer_IV_Brummbar,
    Artillery.SPG_M12_GMC_155mm,
]

TYPE_LOGI = [
    Unarmed.Truck_M818_6x6,
    Unarmed.Transport_KAMAZ_43101,
    Unarmed.Truck_Ural_375,
    Unarmed.Transport_GAZ_66,
    Unarmed.Transport_GAZ_3307,
    Unarmed.Transport_GAZ_3308,
    Unarmed.Transport_Ural_4320_31_Armored,
    Unarmed.Transport_Ural_4320T,
    Unarmed.Blitz_3_6_6700A,
    Unarmed.Kübelwagen_82,
    Unarmed.Sd_Kfz_7,
    Unarmed.Sd_Kfz_2,
    Unarmed.Willys_MB,
    Unarmed.Land_Rover_109_S3,
    Unarmed.Land_Rover_101_FC,
    # Mods
    frenchpack.VBL,
    frenchpack.VAB,
]

TYPE_INFANTRY = [
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
]

TYPE_SHORAD = [
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
    AirDefence.AAA_40mm_Bofors,
    AirDefence.AAA_M1_37mm,
    AirDefence.AAA_QF_3_7,
]
