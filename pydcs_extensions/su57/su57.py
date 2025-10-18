from typing import Set

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class Su57Weapons:
    RVV_AE = {"clsid": "{RVV-AE}", "name": "RVV-AE", "weight": 250}
    RVV_BD = {"clsid": "{RVV-BD}", "name": "RVV-BD", "weight": 600}
    RVV_L = {"clsid": "{RVV-L}", "name": "RVV-L", "weight": 748}
    RVV_M = {"clsid": "{RVV-M}", "name": "RVV-M", "weight": 190}
    R_37M_Active_Rdr = {"clsid": "{RVV-BD}", "name": "R-37M Active Rdr", "weight": 600}
    R_77PD_Active_rdr = {
        "clsid": "{RVV-AE}",
        "name": "R-77PD Active rdr",
        "weight": 250,
    }
    K_77M_Active_Rdr = {"clsid": "{RVV-M}", "name": "K-77M Active Rdr", "weight": 190}
    KS_172_Passive_Rdr = {
        "clsid": "{RVV-L}",
        "name": "KS-172 Passive Rdr",
        "weight": 748,
    }


inject_weapons(Su57Weapons)


@planemod
class Su_57(PlaneType):
    id = "Su-57"
    flyable = True
    height = 4.074
    width = 13.95
    length = 19.008
    fuel_max = 10300
    max_speed = 2499.984
    chaff = 100
    flare = 96
    charge_total = 200
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}

    livery_name = "SU-57"  # from type

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        KS_172_Passive_Rdr = (1, Weapons.KS_172_Passive_Rdr)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (1, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (1, Weapons.K_77M_Active_Rdr)
        L_081_Fantasmagoria_ELINT_pod = (1, Weapons.L_081_Fantasmagoria_ELINT_pod)
        Smoke_Generator___red = (1, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (1, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (1, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (1, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (1, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (1, Weapons.Smoke_Generator___orange)

    class Pylon2:
        R_27R__AA_10_Alamo_A____Semi_Act_Rdr = (
            2,
            Weapons.R_27R__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            2,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27T__AA_10_Alamo_B____Infra_Red = (
            2,
            Weapons.R_27T__AA_10_Alamo_B____Infra_Red,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            2,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_77__AA_12_Adder____Active_Rdr = (2, Weapons.R_77__AA_12_Adder____Active_Rdr)
        R_73__AA_11_Archer____Infra_Red = (2, Weapons.R_73__AA_11_Archer____Infra_Red)
        Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr = (
            2,
            Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr,
        )
        Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr = (
            2,
            Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr,
        )
        Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser_ = (
            2,
            Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser_,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            2,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            2,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        MBD3_U6_68___6_x_OFAB_100_120___100_kg_GP_Bomb_LD = (
            2,
            Weapons.MBD3_U6_68___6_x_OFAB_100_120___100_kg_GP_Bomb_LD,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            2,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            2,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            2,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        BetAB_500___500_kg_Concrete_Piercing_Bomb_LD = (
            2,
            Weapons.BetAB_500___500_kg_Concrete_Piercing_Bomb_LD,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            2,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            2,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        OFAB_250_270___250_kg_GP_Bomb_LD = (2, Weapons.OFAB_250_270___250_kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            2,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500M_62___500_kg_GP_Bomb_LD = (2, Weapons.FAB_500M_62___500_kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            2,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            2,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (2, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        FAB_1500_M_54___1500kg_GP_Bomb_LD = (
            2,
            Weapons.FAB_1500_M_54___1500kg_GP_Bomb_LD,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            2,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        MBD3_U6_68___6_x_OFAB_250_270___250_kg_GP_Bomb_LD = (
            2,
            Weapons.MBD3_U6_68___6_x_OFAB_250_270___250_kg_GP_Bomb_LD,
        )
        R_37M_Active_Rdr = (2, Weapons.R_37M_Active_Rdr)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (2, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (2, Weapons.K_77M_Active_Rdr)
        KS_172_Passive_Rdr = (2, Weapons.KS_172_Passive_Rdr)
        Fuel_tank_800L_Wing = (2, Weapons.Fuel_tank_800L_Wing)
        RN_28___260_kg__nuclear_bomb__free_fall = (
            2,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )
        Smoke_Generator___red = (2, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (2, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (2, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (2, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (2, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (2, Weapons.Smoke_Generator___orange)

    class Pylon3:
        R_73__AA_11_Archer____Infra_Red = (3, Weapons.R_73__AA_11_Archer____Infra_Red)
        Smoke_Generator___red = (3, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (3, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (3, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (3, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (3, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (3, Weapons.Smoke_Generator___orange)

    class Pylon4:
        R_27R__AA_10_Alamo_A____Semi_Act_Rdr = (
            4,
            Weapons.R_27R__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            4,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27T__AA_10_Alamo_B____Infra_Red = (
            4,
            Weapons.R_27T__AA_10_Alamo_B____Infra_Red,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            4,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_77__AA_12_Adder____Active_Rdr = (4, Weapons.R_77__AA_12_Adder____Active_Rdr)
        R_73__AA_11_Archer____Infra_Red = (4, Weapons.R_73__AA_11_Archer____Infra_Red)
        Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr = (
            4,
            Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr,
        )
        Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr = (
            4,
            Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr,
        )
        Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser_ = (
            4,
            Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser_,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            4,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        MBD3_U6_68___6_x_OFAB_100_120___100_kg_GP_Bomb_LD = (
            4,
            Weapons.MBD3_U6_68___6_x_OFAB_100_120___100_kg_GP_Bomb_LD,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            4,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            4,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            4,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        BetAB_500___500_kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500_kg_Concrete_Piercing_Bomb_LD,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        OFAB_250_270___250_kg_GP_Bomb_LD = (4, Weapons.OFAB_250_270___250_kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500M_62___500_kg_GP_Bomb_LD = (4, Weapons.FAB_500M_62___500_kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            4,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (4, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        FAB_1500_M_54___1500kg_GP_Bomb_LD = (
            4,
            Weapons.FAB_1500_M_54___1500kg_GP_Bomb_LD,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            4,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        MBD3_U6_68___6_x_OFAB_250_270___250_kg_GP_Bomb_LD = (
            4,
            Weapons.MBD3_U6_68___6_x_OFAB_250_270___250_kg_GP_Bomb_LD,
        )
        R_37M_Active_Rdr = (4, Weapons.R_37M_Active_Rdr)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (4, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (4, Weapons.K_77M_Active_Rdr)
        KS_172_Passive_Rdr = (4, Weapons.KS_172_Passive_Rdr)
        RN_28___260_kg__nuclear_bomb__free_fall = (
            4,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )

    class Pylon5:
        R_77__AA_12_Adder____Active_Rdr = (5, Weapons.R_77__AA_12_Adder____Active_Rdr)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (5, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (5, Weapons.K_77M_Active_Rdr)
        KS_172_Passive_Rdr = (5, Weapons.KS_172_Passive_Rdr)

    class Pylon6:
        R_77__AA_12_Adder____Active_Rdr = (6, Weapons.R_77__AA_12_Adder____Active_Rdr)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (6, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (6, Weapons.K_77M_Active_Rdr)
        KS_172_Passive_Rdr = (6, Weapons.KS_172_Passive_Rdr)

    class Pylon7:
        R_77__AA_12_Adder____Active_Rdr = (7, Weapons.R_77__AA_12_Adder____Active_Rdr)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (7, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (7, Weapons.K_77M_Active_Rdr)
        KS_172_Passive_Rdr = (7, Weapons.KS_172_Passive_Rdr)

    class Pylon8:
        R_77__AA_12_Adder____Active_Rdr = (8, Weapons.R_77__AA_12_Adder____Active_Rdr)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (8, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (8, Weapons.K_77M_Active_Rdr)
        KS_172_Passive_Rdr = (8, Weapons.KS_172_Passive_Rdr)

    class Pylon9:
        R_77__AA_12_Adder____Active_Rdr = (9, Weapons.R_77__AA_12_Adder____Active_Rdr)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (9, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (9, Weapons.K_77M_Active_Rdr)
        KS_172_Passive_Rdr = (9, Weapons.KS_172_Passive_Rdr)

    class Pylon10:
        R_77__AA_12_Adder____Active_Rdr = (10, Weapons.R_77__AA_12_Adder____Active_Rdr)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (10, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (10, Weapons.K_77M_Active_Rdr)
        KS_172_Passive_Rdr = (10, Weapons.KS_172_Passive_Rdr)

    class Pylon11:
        R_27R__AA_10_Alamo_A____Semi_Act_Rdr = (
            11,
            Weapons.R_27R__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            11,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27T__AA_10_Alamo_B____Infra_Red = (
            11,
            Weapons.R_27T__AA_10_Alamo_B____Infra_Red,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            11,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_77__AA_12_Adder____Active_Rdr = (11, Weapons.R_77__AA_12_Adder____Active_Rdr)
        R_73__AA_11_Archer____Infra_Red = (11, Weapons.R_73__AA_11_Archer____Infra_Red)
        Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr = (
            11,
            Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr,
        )
        Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr = (
            11,
            Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr,
        )
        Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser_ = (
            11,
            Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser_,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            11,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            11,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        MBD3_U6_68___6_x_OFAB_100_120___100_kg_GP_Bomb_LD = (
            11,
            Weapons.MBD3_U6_68___6_x_OFAB_100_120___100_kg_GP_Bomb_LD,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            11,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            11,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            11,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        BetAB_500___500_kg_Concrete_Piercing_Bomb_LD = (
            11,
            Weapons.BetAB_500___500_kg_Concrete_Piercing_Bomb_LD,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            11,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            11,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        OFAB_250_270___250_kg_GP_Bomb_LD = (
            11,
            Weapons.OFAB_250_270___250_kg_GP_Bomb_LD,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            11,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500M_62___500_kg_GP_Bomb_LD = (11, Weapons.FAB_500M_62___500_kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            11,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            11,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            11,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        FAB_1500_M_54___1500kg_GP_Bomb_LD = (
            11,
            Weapons.FAB_1500_M_54___1500kg_GP_Bomb_LD,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            11,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        MBD3_U6_68___6_x_OFAB_250_270___250_kg_GP_Bomb_LD = (
            11,
            Weapons.MBD3_U6_68___6_x_OFAB_250_270___250_kg_GP_Bomb_LD,
        )
        R_37M_Active_Rdr = (11, Weapons.R_37M_Active_Rdr)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (11, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (11, Weapons.K_77M_Active_Rdr)
        KS_172_Passive_Rdr = (11, Weapons.KS_172_Passive_Rdr)
        RN_28___260_kg__nuclear_bomb__free_fall = (
            11,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    class Pylon13:
        R_27R__AA_10_Alamo_A____Semi_Act_Rdr = (
            13,
            Weapons.R_27R__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            13,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27T__AA_10_Alamo_B____Infra_Red = (
            13,
            Weapons.R_27T__AA_10_Alamo_B____Infra_Red,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            13,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_77__AA_12_Adder____Active_Rdr = (13, Weapons.R_77__AA_12_Adder____Active_Rdr)
        R_73__AA_11_Archer____Infra_Red = (13, Weapons.R_73__AA_11_Archer____Infra_Red)
        Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr = (
            13,
            Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr,
        )
        Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr = (
            13,
            Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr,
        )
        Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser_ = (
            13,
            Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser_,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_ = (
            13,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided_,
        )
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            13,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        MBD3_U6_68___6_x_OFAB_100_120___100_kg_GP_Bomb_LD = (
            13,
            Weapons.MBD3_U6_68___6_x_OFAB_100_120___100_kg_GP_Bomb_LD,
        )
        B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag = (
            13,
            Weapons.B_8M1___20_x_UnGd_Rkts__80_mm_S_8KOM_HEAT_Frag,
        )
        B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation = (
            13,
            Weapons.B_13L___5_x_UnGd_Rkts__122_mm_S_13OF_Blast_Fragmentation,
        )
        O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator = (
            13,
            Weapons.O_25___1_x_UnGd_Rkts__340_mm_S_25_OFM_Hardened_Target_Penetrator,
        )
        BetAB_500___500_kg_Concrete_Piercing_Bomb_LD = (
            13,
            Weapons.BetAB_500___500_kg_Concrete_Piercing_Bomb_LD,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            13,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            13,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        OFAB_250_270___250_kg_GP_Bomb_LD = (
            13,
            Weapons.OFAB_250_270___250_kg_GP_Bomb_LD,
        )
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            13,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500M_62___500_kg_GP_Bomb_LD = (13, Weapons.FAB_500M_62___500_kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            13,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            13,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (
            13,
            Weapons.KAB_500Kr___500kg_TV_Guided_Bomb,
        )
        FAB_1500_M_54___1500kg_GP_Bomb_LD = (
            13,
            Weapons.FAB_1500_M_54___1500kg_GP_Bomb_LD,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            13,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        MBD3_U6_68___6_x_OFAB_250_270___250_kg_GP_Bomb_LD = (
            13,
            Weapons.MBD3_U6_68___6_x_OFAB_250_270___250_kg_GP_Bomb_LD,
        )
        # ERRR {R-33}
        R_37M_Active_Rdr = (13, Weapons.R_37M_Active_Rdr)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (13, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (13, Weapons.K_77M_Active_Rdr)
        KS_172_Passive_Rdr = (13, Weapons.KS_172_Passive_Rdr)
        Fuel_tank_800L_Wing = (13, Weapons.Fuel_tank_800L_Wing)
        RN_28___260_kg__nuclear_bomb__free_fall = (
            13,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )
        Smoke_Generator___red = (13, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (13, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (13, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (13, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (13, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (13, Weapons.Smoke_Generator___orange)

    class Pylon14:
        R_73__AA_11_Archer____Infra_Red = (14, Weapons.R_73__AA_11_Archer____Infra_Red)
        # ERRR {RVV-AE}
        R_77PD_Active_rdr = (14, Weapons.R_77PD_Active_rdr)
        K_77M_Active_Rdr = (14, Weapons.K_77M_Active_Rdr)
        Smoke_Generator___red = (14, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (14, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (14, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (14, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (14, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (14, Weapons.Smoke_Generator___orange)

    class Pylon15:
        Mercury_LLTV_Pod = (15, Weapons.Mercury_LLTV_Pod)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}

    tasks = [
        task.CAP,
        task.Intercept,
        task.Escort,
        task.FighterSweep,
        task.AFAC,
        task.GroundAttack,
        task.RunwayAttack,
        task.AntishipStrike,
        task.CAS,
    ]
    task_default = task.CAP
