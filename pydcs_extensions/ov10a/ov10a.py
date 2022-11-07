from typing import Any, Dict, Set

from dcs import task
from dcs.liveries_scanner import Liveries
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsOV10A:
    OV10_SMOKE = {"clsid": "{OV10_SMOKE}", "name": "OV10_SMOKE", "weight": 1}
    ParaTrooper = {"clsid": "{PARA}", "name": "ParaTrooper", "weight": 80}
    Fuel_Tank_150_gallons_ = {
        "clsid": "{150gal}",
        "name": "Fuel Tank 150 gallons",
        "weight": 499.5592,
    }


inject_weapons(WeaponsOV10A)


@planemod
class Bronco_OV_10A(PlaneType):
    id = "Bronco-OV-10A"
    flyable = True
    height = 4.62
    width = 12.9
    length = 12.76
    fuel_max = 940
    max_speed = 684
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    panel_radio = {
        1: {
            "channels": {6: 41, 2: 31, 8: 50, 3: 32, 1: 30, 4: 33, 5: 40, 7: 42},
        },
    }

    livery_name = "BRONCO-OV-10A"  # from type
    Liveries = Liveries()[livery_name]

    class Pylon1:
        LAU_7_with_AIM_9P_Sidewinder_IR_AAM = (
            1,
            Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM,
        )

    # ERRR {MK-81}

    class Pylon2:
        Mk_82___500lb_GP_Bomb_LD = (2, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (2, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (2, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (2, Weapons.M117___750lb_GP_Bomb_LD)
        LAU3_WP156 = (2, Weapons.LAU3_WP156)
        LAU3_WP1B = (2, Weapons.LAU3_WP1B)
        LAU3_WP61 = (2, Weapons.LAU3_WP61)
        LAU3_HE5 = (2, Weapons.LAU3_HE5)
        LAU3_HE151 = (2, Weapons.LAU3_HE151)
        M260_HYDRA = (2, Weapons.M260_HYDRA)
        LAU_10R_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.LAU_10R_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            2,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )

    # ERRR {MK-81}

    class Pylon3:
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (3, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (3, Weapons.M117___750lb_GP_Bomb_LD)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        M260_HYDRA = (3, Weapons.M260_HYDRA)
        LAU_10R_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            3,
            Weapons.LAU_10R_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            3,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )

    class Pylon4:
        Fuel_Tank_150_gallons_ = (4, Weapons.Fuel_Tank_150_gallons_)
        # ERRR {MK-81}
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (4, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (4, Weapons.M117___750lb_GP_Bomb_LD)

    # ERRR {MK-81}

    class Pylon5:
        Mk_82___500lb_GP_Bomb_LD = (5, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (5, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (5, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (5, Weapons.M117___750lb_GP_Bomb_LD)
        LAU3_WP156 = (5, Weapons.LAU3_WP156)
        LAU3_WP1B = (5, Weapons.LAU3_WP1B)
        LAU3_WP61 = (5, Weapons.LAU3_WP61)
        LAU3_HE5 = (5, Weapons.LAU3_HE5)
        LAU3_HE151 = (5, Weapons.LAU3_HE151)
        M260_HYDRA = (5, Weapons.M260_HYDRA)
        LAU_10R_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            5,
            Weapons.LAU_10R_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            5,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )

    # ERRR {MK-81}

    class Pylon6:
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_83___1000lb_GP_Bomb_LD = (6, Weapons.Mk_83___1000lb_GP_Bomb_LD)
        M117___750lb_GP_Bomb_LD = (6, Weapons.M117___750lb_GP_Bomb_LD)
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_WP1B = (6, Weapons.LAU3_WP1B)
        LAU3_WP61 = (6, Weapons.LAU3_WP61)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        M260_HYDRA = (6, Weapons.M260_HYDRA)
        LAU_10R_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            6,
            Weapons.LAU_10R_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )
        LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG = (
            6,
            Weapons.LAU_10_pod___4_x_127mm_ZUNI__UnGd_Rkts_Mk71__HE_FRAG,
        )

    class Pylon7:
        LAU_7_with_AIM_9P_Sidewinder_IR_AAM = (
            7,
            Weapons.LAU_7_with_AIM_9P_Sidewinder_IR_AAM,
        )

    class Pylon8:
        ParaTrooper = (8, Weapons.ParaTrooper)

    class Pylon9:
        OV10_SMOKE = (9, Weapons.OV10_SMOKE)

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    tasks = [
        task.GroundAttack,
        task.RunwayAttack,
        task.PinpointStrike,
        task.CAS,
        task.AFAC,
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
    ]
    task_default = task.CAS
