from typing import Set

from dcs import task
from dcs.liveries_scanner import Liveries
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class Su57Weapons:
    Kh_59MK2 = {"clsid": "{KH_59MK2}", "name": "Kh-59MK2", "weight": None}
    RVV_AE = {"clsid": "{RVV-AE}", "name": "RVV-AE", "weight": 250}
    RVV_BD = {"clsid": "{RVV-BD}", "name": "RVV-BD", "weight": 600}
    RVV_L = {"clsid": "{RVV-L}", "name": "RVV-L", "weight": 748}
    RVV_M = {"clsid": "{RVV-M}", "name": "RVV-M", "weight": 190}
    Su_57_Fuel_Tank = {
        "clsid": "{SU_57Tank}",
        "name": "Su-57 Fuel Tank",
        "weight": 1561.421,
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
    Liveries = Liveries()[livery_name]

    class Pylon1:
        R_73__AA_11_Archer____Infra_Red = (1, Weapons.R_73__AA_11_Archer____Infra_Red)
        RVV_AE = (1, Su57Weapons.RVV_AE)
        RVV_M = (1, Su57Weapons.RVV_M)
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
        Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser = (
            2,
            Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided = (
            2,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided,
        )
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            2,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            2,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            2,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        B_13L_pod___5_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            2,
            Weapons.B_13L_pod___5_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        S_25_OFM___340mm_UnGd_Rkt__480kg_Penetrator = (
            2,
            Weapons.S_25_OFM___340mm_UnGd_Rkt__480kg_Penetrator,
        )
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            2,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            2,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            2,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (2, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            2,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (2, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
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
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            2,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        RVV_BD = (2, Su57Weapons.RVV_BD)
        RVV_AE = (2, Su57Weapons.RVV_AE)
        RVV_M = (2, Su57Weapons.RVV_M)
        RVV_L = (2, Su57Weapons.RVV_L)
        Fuel_tank_800L_Wing = (2, Weapons.Fuel_tank_800L_Wing)
        RN_28___260_kg__nuclear_bomb__free_fall = (
            2,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )
        Su_57_Fuel_Tank = (2, Su57Weapons.Su_57_Fuel_Tank)
        Kh_59MK2 = (2, Su57Weapons.Kh_59MK2)
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
        Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser = (
            4,
            Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided = (
            4,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided,
        )
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            4,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            4,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        B_13L_pod___5_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            4,
            Weapons.B_13L_pod___5_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        S_25_OFM___340mm_UnGd_Rkt__480kg_Penetrator = (
            4,
            Weapons.S_25_OFM___340mm_UnGd_Rkt__480kg_Penetrator,
        )
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            4,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            4,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            4,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (4, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            4,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (4, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
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
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            4,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        RVV_BD = (4, Su57Weapons.RVV_BD)
        RVV_AE = (4, Su57Weapons.RVV_AE)
        RVV_M = (4, Su57Weapons.RVV_M)
        RVV_L = (4, Su57Weapons.RVV_L)
        RN_28___260_kg__nuclear_bomb__free_fall = (
            4,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )
        Su_57_Fuel_Tank = (4, Su57Weapons.Su_57_Fuel_Tank)
        Kh_59MK2 = (4, Su57Weapons.Kh_59MK2)

    class Pylon5:
        R_77__AA_12_Adder____Active_Rdr = (5, Weapons.R_77__AA_12_Adder____Active_Rdr)
        RVV_AE = (5, Su57Weapons.RVV_AE)
        RVV_M = (5, Su57Weapons.RVV_M)
        Kh_59MK2 = (5, Su57Weapons.Kh_59MK2)

    class Pylon6:
        R_77__AA_12_Adder____Active_Rdr = (6, Weapons.R_77__AA_12_Adder____Active_Rdr)
        RVV_AE = (6, Su57Weapons.RVV_AE)
        RVV_M = (6, Su57Weapons.RVV_M)
        Kh_59MK2 = (6, Su57Weapons.Kh_59MK2)

    class Pylon7:
        R_77__AA_12_Adder____Active_Rdr = (7, Weapons.R_77__AA_12_Adder____Active_Rdr)
        RVV_AE = (7, Su57Weapons.RVV_AE)
        RVV_M = (7, Su57Weapons.RVV_M)
        Kh_59MK2 = (7, Su57Weapons.Kh_59MK2)

    class Pylon8:
        R_77__AA_12_Adder____Active_Rdr = (8, Weapons.R_77__AA_12_Adder____Active_Rdr)
        RVV_AE = (8, Su57Weapons.RVV_AE)
        RVV_M = (8, Su57Weapons.RVV_M)
        Kh_59MK2 = (8, Su57Weapons.Kh_59MK2)

    class Pylon9:
        R_27R__AA_10_Alamo_A____Semi_Act_Rdr = (
            9,
            Weapons.R_27R__AA_10_Alamo_A____Semi_Act_Rdr,
        )
        R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range = (
            9,
            Weapons.R_27ER__AA_10_Alamo_C____Semi_Act_Extended_Range,
        )
        R_27T__AA_10_Alamo_B____Infra_Red = (
            9,
            Weapons.R_27T__AA_10_Alamo_B____Infra_Red,
        )
        R_27ET__AA_10_Alamo_D____IR_Extended_Range = (
            9,
            Weapons.R_27ET__AA_10_Alamo_D____IR_Extended_Range,
        )
        R_77__AA_12_Adder____Active_Rdr = (9, Weapons.R_77__AA_12_Adder____Active_Rdr)
        R_73__AA_11_Archer____Infra_Red = (9, Weapons.R_73__AA_11_Archer____Infra_Red)
        Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr = (
            9,
            Weapons.Kh_31P__AS_17_Krypton____600kg__ARM__IN__Pas_Rdr,
        )
        Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr = (
            9,
            Weapons.Kh_31A__AS_17_Krypton____610kg__AShM__IN__Act_Rdr,
        )
        Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser = (
            9,
            Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided = (
            9,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided,
        )
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            9,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            9,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        B_13L_pod___5_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            9,
            Weapons.B_13L_pod___5_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        S_25_OFM___340mm_UnGd_Rkt__480kg_Penetrator = (
            9,
            Weapons.S_25_OFM___340mm_UnGd_Rkt__480kg_Penetrator,
        )
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            9,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            9,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            9,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (9, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            9,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (9, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
        RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP = (
            9,
            Weapons.RBK_500_255___30_x_PTAB_10_5__500kg_CBU_Heavy_HEAT_AP,
        )
        KAB_500LG___500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_500LG___500kg_Laser_Guided_Bomb,
        )
        KAB_500Kr___500kg_TV_Guided_Bomb = (9, Weapons.KAB_500Kr___500kg_TV_Guided_Bomb)
        FAB_1500_M_54___1500kg_GP_Bomb_LD = (
            9,
            Weapons.FAB_1500_M_54___1500kg_GP_Bomb_LD,
        )
        KAB_1500L___1500kg_Laser_Guided_Bomb = (
            9,
            Weapons.KAB_1500L___1500kg_Laser_Guided_Bomb,
        )
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            9,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        RVV_BD = (9, Su57Weapons.RVV_BD)
        RVV_AE = (9, Su57Weapons.RVV_AE)
        RVV_M = (9, Su57Weapons.RVV_M)
        RVV_L = (9, Su57Weapons.RVV_L)
        RN_28___260_kg__nuclear_bomb__free_fall = (
            9,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )
        Su_57_Fuel_Tank = (9, Su57Weapons.Su_57_Fuel_Tank)
        Kh_59MK2 = (9, Su57Weapons.Kh_59MK2)

    class Pylon10:
        R_73__AA_11_Archer____Infra_Red = (10, Weapons.R_73__AA_11_Archer____Infra_Red)
        Smoke_Generator___red = (10, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (10, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (10, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (10, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (10, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (10, Weapons.Smoke_Generator___orange)

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
        Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser = (
            11,
            Weapons.Kh_29L__AS_14_Kedge____657kg__ASM__Semi_Act_Laser,
        )
        Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided = (
            11,
            Weapons.Kh_29T__AS_14_Kedge____670kg__ASM__TV_Guided,
        )
        Kh_59M__AS_18_Kazoo____930kg__ASM__IN = (
            11,
            Weapons.Kh_59M__AS_18_Kazoo____930kg__ASM__IN,
        )
        MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD = (
            11,
            Weapons.MBD3_U6_68_with_6_x_FAB_100___100kg_GP_Bombs_LD,
        )
        B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP = (
            11,
            Weapons.B_8M1_pod___20_x_S_8KOM__80mm_UnGd_Rkts__HEAT_AP,
        )
        B_13L_pod___5_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag = (
            11,
            Weapons.B_13L_pod___5_x_S_13_OF__122mm_UnGd_Rkts__Blast_Frag,
        )
        S_25_OFM___340mm_UnGd_Rkt__480kg_Penetrator = (
            11,
            Weapons.S_25_OFM___340mm_UnGd_Rkt__480kg_Penetrator,
        )
        BetAB_500___500kg_Concrete_Piercing_Bomb_LD = (
            11,
            Weapons.BetAB_500___500kg_Concrete_Piercing_Bomb_LD,
        )
        KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag = (
            11,
            Weapons.KMGU_2___96_x_AO_2_5RT_Dispenser__CBU__HE_Frag,
        )
        KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP = (
            11,
            Weapons.KMGU_2___96_x_PTAB_2_5KO_Dispenser__CBU__HEAT_AP,
        )
        FAB_250___250kg_GP_Bomb_LD = (11, Weapons.FAB_250___250kg_GP_Bomb_LD)
        RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP = (
            11,
            Weapons.RBK_250___42_x_PTAB_2_5M__250kg_CBU_Medium_HEAT_AP,
        )
        FAB_500_M_62___500kg_GP_Bomb_LD = (11, Weapons.FAB_500_M_62___500kg_GP_Bomb_LD)
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
        MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD = (
            11,
            Weapons.MBD3_U6_68_with_6_x_FAB_250___250kg_GP_Bombs_LD,
        )
        # ERRR {R-33}
        RVV_BD = (11, Su57Weapons.RVV_BD)
        RVV_AE = (11, Su57Weapons.RVV_AE)
        RVV_M = (11, Su57Weapons.RVV_M)
        RVV_L = (11, Su57Weapons.RVV_L)
        Fuel_tank_800L_Wing = (11, Weapons.Fuel_tank_800L_Wing)
        Su_57_Fuel_Tank = (11, Su57Weapons.Su_57_Fuel_Tank)
        RN_28___260_kg__nuclear_bomb__free_fall = (
            11,
            Weapons.RN_28___260_kg__nuclear_bomb__free_fall,
        )
        Smoke_Generator___red = (11, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (11, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (11, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (11, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (11, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (11, Weapons.Smoke_Generator___orange)
        Kh_59MK2 = (11, Su57Weapons.Kh_59MK2)

    class Pylon12:
        R_73__AA_11_Archer____Infra_Red = (12, Weapons.R_73__AA_11_Archer____Infra_Red)
        RVV_AE = (12, Su57Weapons.RVV_AE)
        RVV_M = (12, Su57Weapons.RVV_M)
        Smoke_Generator___red = (12, Weapons.Smoke_Generator___red)
        Smoke_Generator___green = (12, Weapons.Smoke_Generator___green)
        Smoke_Generator___blue = (12, Weapons.Smoke_Generator___blue)
        Smoke_Generator___white = (12, Weapons.Smoke_Generator___white)
        Smoke_Generator___yellow = (12, Weapons.Smoke_Generator___yellow)
        Smoke_Generator___orange = (12, Weapons.Smoke_Generator___orange)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

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
