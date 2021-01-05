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
    Armor.MBT_Merkava_Mk__4,
    Armor.ZTZ_96B,

    # WW2
    Armor.MT_Pz_Kpfw_V_Panther_Ausf_G,
    Armor.MT_Pz_Kpfw_IV_Ausf_H,
    Armor.HT_Pz_Kpfw_VI_Tiger_I,
    Armor.HT_Pz_Kpfw_VI_Ausf__B_Tiger_II,
    Armor.MT_M4_Sherman,
    Armor.MT_M4A4_Sherman_Firefly,
    Armor.StuG_IV,
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
    Armor.ATGM_M1045_HMMWV_TOW,
    Armor.ATGM_M1134_Stryker,
    Armor.IFV_BMP_2,

    # WW2 (Tank Destroyers)
    Armor.M30_Cargo_Carrier,
    Armor.TD_Jagdpanzer_IV,
    Armor.TD_Jagdpanther_G1,
    Armor.TD_M10_GMC,

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
    Armor.IFV_MCV_80,
    Armor.IFV_LAV_25,
    Armor.SPG_M1128_Stryker_MGS,
    Armor.AC_Sd_Kfz_234_2_Puma,
    Armor.IFV_M2A2_Bradley,
    Armor.IFV_BMD_1,
    Armor.ZBD_04A,

    # WW2
    Armor.AC_Sd_Kfz_234_2_Puma,
    Armor.LAC_M8_Greyhound,
    Armor.Daimler_Armoured_Car,

    # Mods
    frenchpack.ERC_90,
    frenchpack.VBAE_CRAB,
    frenchpack.VAB_T20_13

]

TYPE_APC = [
    Armor.APC_M1043_HMMWV_Armament,
    Armor.APC_M1126_Stryker_ICV,
    Armor.APC_M113,
    Armor.APC_BTR_80,
    Armor.APC_BTR_82A,
    Armor.APC_MTLB,
    Armor.APC_M2A1,
    Armor.APC_Cobra,
    Armor.APC_Sd_Kfz_251,
    Armor.APC_AAV_7,
    Armor.TPz_Fuchs,
    Armor.ARV_BRDM_2,
    Armor.ARV_BTR_RD,
    Armor.FDDM_Grad,

    # WW2
    Armor.APC_M2A1,
    Armor.APC_Sd_Kfz_251,

    # Mods
    frenchpack.VAB__50,
    frenchpack.VBL__50,
    frenchpack.VBL_AANF1,

]

TYPE_ARTILLERY = [
    Artillery.MLRS_9A52_Smerch,
    Artillery.SPH_2S1_Gvozdika,
    Artillery.SPH_2S3_Akatsia,
    Artillery.MLRS_BM_21_Grad,
    Artillery.MLRS_9K57_Uragan_BM_27,
    Artillery.SPH_M109_Paladin,
    Artillery.MLRS_M270,
    Artillery.SPH_2S9_Nona,
    Artillery.SpGH_Dana,
    Artillery.SPH_2S19_Msta,
    Artillery.MLRS_FDDM,

    # WW2
    Artillery.Sturmpanzer_IV_Brummbär,
    Artillery.M12_GMC
]

TYPE_LOGI = [
    Unarmed.Transport_M818,
    Unarmed.Transport_KAMAZ_43101,
    Unarmed.Transport_Ural_375,
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
    Infantry.Infantry_Soldier_Insurgents,
    Infantry.Soldier_AK,
    Infantry.Infantry_M1_Garand,
    Infantry.Infantry_Mauser_98,
    Infantry.Infantry_SMLE_No_4_Mk_1,
    Infantry.Georgian_soldier_with_M4,
    Infantry.Infantry_Soldier_Rus,
    Infantry.Paratrooper_AKS,
    Infantry.Paratrooper_RPG_16,
    Infantry.Soldier_M249,
    Infantry.Infantry_M4,
    Infantry.Soldier_RPG,
]

TYPE_SHORAD = [
    AirDefence.AAA_ZU_23_on_Ural_375,
    AirDefence.AAA_ZU_23_Insurgent_on_Ural_375,
    AirDefence.AAA_ZSU_57_2,
    AirDefence.SPAAA_ZSU_23_4_Shilka,
    AirDefence.SAM_SA_8_Osa_9A33,
    AirDefence.SAM_SA_9_Strela_1_9P31,
    AirDefence.SAM_SA_13_Strela_10M3_9A35M3,
    AirDefence.SAM_SA_15_Tor_9A331,
    AirDefence.SAM_SA_19_Tunguska_2S6,

    AirDefence.SPAAA_Gepard,
    AirDefence.AAA_Vulcan_M163,
    AirDefence.SAM_Linebacker_M6,
    AirDefence.SAM_Chaparral_M48,
    AirDefence.SAM_Avenger_M1097,
    AirDefence.SAM_Roland_ADS,
    AirDefence.HQ_7_Self_Propelled_LN,

    AirDefence.AAA_8_8cm_Flak_18,
    AirDefence.AAA_8_8cm_Flak_36,
    AirDefence.AAA_8_8cm_Flak_37,
    AirDefence.AAA_8_8cm_Flak_41,
    AirDefence.AAA_Bofors_40mm,
    AirDefence.AAA_M1_37mm,
    AirDefence.AA_gun_QF_3_7,

]
