from enum import Enum
from typing import Dict, Any, List, Set

from dcs import task
from dcs.helicopters import HelicopterType
from dcs.weapons_data import Weapons

from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsAH64D:
    M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M257__Illum_ = {
        "clsid": "{M261_M257}",
        "name": 'M261 pod - 19 x 2.75" Hydra, UnGd Rkts M257, Illum.',
        "weight": 271.5,
    }
    M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M274__Smk = {
        "clsid": "{M261_M274}",
        "name": 'M261 pod - 19 x 2.75" Hydra, UnGd Rkts M274, Smk',
        "weight": 286.7,
    }
    M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M229__HEDP = {
        "clsid": "{M261_M229}",
        "name": 'M261 pod - 19 x 2.75" Hydra, UnGd Rkts M229, HEDP',
        "weight": 338.19,
    }
    M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__MPP = {
        "clsid": "{M261_M282}",
        "name": 'M261 pod - 19 x 2.75" Hydra, UnGd Rkts M282, MPP',
        "weight": 309.88,
    }
    M261_Outboard_Launcher__Zones_A_B_M151_Hydra__6PD___Zone_E_M274_Hydra__6SK_ = {
        "clsid": "{M261_OUTBOARD_AB_M151_E_M274}",
        "name": "M261: Outboard Launcher, Zones A/B: M151 Hydra (6PD), Zone E: M274 Hydra (6SK)",
        "weight": 273.1,
    }
    M261_Outboard_Launcher__Zones_A_B_M151_Hydra__6PD___Zone_E_M257_Hydra__6IL_ = {
        "clsid": "{M261_OUTBOARD_AB_M151_E_M257}",
        "name": "M261: Outboard Launcher, Zones A/B: M151 Hydra (6PD), Zone E: M257 Hydra (6IL)",
        "weight": 275.5,
    }
    M299___4_x_AGM_114K_Hellfire = {
        "clsid": "{88D18A5E-99C8-4B04-B40B-1C02F2018B6E}",
        "name": "M299 - 4 x AGM-114K Hellfire",
        "weight": 247.4,
    }
    M299___3_x_AGM_114K_Hellfire__Port = {
        "clsid": "{M299_3xAGM_114K_OUTBOARD_PORT}",
        "name": "M299 - 3 x AGM-114K Hellfire, Port",
        "weight": 202,
    }
    M299___2_x_AGM_114K_Hellfire = {
        "clsid": "{M299_2xAGM_114K}",
        "name": "M299 - 2 x AGM-114K Hellfire",
        "weight": 156.6,
    }
    M299___1_x_AGM_114K_Hellfire__Port = {
        "clsid": "{M299_1xAGM_114K_OUTBOARD_PORT}",
        "name": "M299 - 1 x AGM-114K Hellfire, Port",
        "weight": 111.2,
    }
    M299___Empty_Launcher = {
        "clsid": "{M299_EMPTY}",
        "name": "M299 - Empty Launcher",
        "weight": 65.8,
    }
    Fuel_tank_230_gal = {
        "clsid": "{EFT_230GAL}",
        "name": "Fuel tank 230 gal",
        "weight": 765.45,
    }
    M261_Inboard_Launcher__Zone_C_M274_Hydra__6SK___Zones_D_E_M151_Hydra__6PD_ = {
        "clsid": "{M261_INBOARD_DE_M151_C_M274}",
        "name": "M261: Inboard Launcher, Zone C: M274 Hydra (6SK), Zones D/E: M151 Hydra (6PD)",
        "weight": 273.1,
    }
    M261_Inboard_Launcher__Zone_C_M257_Hydra__6IL___Zones_D_E_M151_Hydra__6PD_ = {
        "clsid": "{M261_INBOARD_DE_M151_C_M257}",
        "name": "M261: Inboard Launcher, Zone C: M257 Hydra (6IL), Zones D/E: M151 Hydra (6PD)",
        "weight": 275.5,
    }
    M299___3_x_AGM_114K_Hellfire__Starboard = {
        "clsid": "{M299_3xAGM_114K_OUTBOARD_STARBOARD}",
        "name": "M299 - 3 x AGM-114K Hellfire, Starboard",
        "weight": 202,
    }
    M299___1_x_AGM_114K_Hellfire__Starboard = {
        "clsid": "{M299_1xAGM_114K_OUTBOARD_STARBOARD}",
        "name": "M299 - 1 x AGM-114K Hellfire, Starboard",
        "weight": 111.2,
    }


inject_weapons(WeaponsAH64D)


class AH_64D_BLK_II(HelicopterType):
    id = "AH-64D_BLK_II"
    flyable = True
    height = 4.15
    width = 14.63
    length = 17.87
    fuel_max = 1438
    max_speed = 365
    chaff = 30
    flare = 60
    charge_total = 90
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True

    panel_radio = {
        1: {
            "channels": {
                7: 141,
                1: 127.5,
                2: 135,
                4: 127,
                8: 128,
                9: 126,
                5: 125,
                10: 137,
                3: 136,
                6: 121,
            },
        },
        2: {
            "channels": {
                7: 325,
                1: 225,
                2: 240,
                4: 270,
                8: 350,
                9: 375,
                5: 285,
                10: 390,
                3: 255,
                6: 300,
            },
        },
        4: {
            "channels": {
                7: 30.035,
                1: 30,
                2: 30.01,
                4: 30.02,
                8: 30.04,
                9: 30.045,
                5: 30.025,
                10: 30.05,
                3: 30.015,
                6: 30.03,
            },
        },
        3: {
            "channels": {
                7: 30.035,
                1: 30,
                2: 30.01,
                4: 30.02,
                8: 30.04,
                9: 30.045,
                5: 30.025,
                10: 30.05,
                3: 30.015,
                6: 30.03,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "ArmyAir",
            "Apache",
            "Crow",
            "Chaos",
            "Sioux",
            "Gatling",
            "Gunslinger",
            "Hammerhead",
            "Bootleg",
            "Palehorse",
            "Carnivore",
            "Saber",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "FCR_RFI_removed": True,
        "NetCrewControlPriority": 0,
        "AIDisabled": False,
        "FlareBurstCount": 0,
        "FlareBurstInterval": 0,
        "FlareSalvoCount": 0,
        "FlareSalvoInterval": 0,
        "FlareProgramDelay": 0,
        "PltNVG": True,
        "CpgNVG": True,
    }

    class Properties:
        class FCR_RFI_removed:
            id = "FCR_RFI_removed"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                CPG = 1
                Ask_Always = -1
                Equally_Responsible = -2

        class AIDisabled:
            id = "AIDisabled"

        class FlareBurstCount:
            id = "FlareBurstCount"

            class Values:
                _1 = 0
                _2 = 1
                _3 = 2
                _4 = 3
                _6 = 4
                _8 = 5

        class FlareBurstInterval:
            id = "FlareBurstInterval"

            class Values:
                _0_1 = 0
                _0_2 = 1
                _0_3 = 2
                _0_4 = 3

        class FlareSalvoCount:
            id = "FlareSalvoCount"

            class Values:
                _1 = 0
                _2 = 1
                _4 = 2
                _8 = 3
                Continuous = 4

        class FlareSalvoInterval:
            id = "FlareSalvoInterval"

            class Values:
                _1 = 0
                _2 = 1
                _3 = 2
                _4 = 3
                _5 = 4
                _8 = 5
                Random = 6

        class FlareProgramDelay:
            id = "FlareProgramDelay"

            class Values:
                _1 = 0
                _2 = 1
                _3 = 2
                _4 = 3

        class PltNVG:
            id = "PltNVG"

        class CpgNVG:
            id = "CpgNVG"

    class Liveries:
        class Combined_Joint_Task_Forces_Blue(Enum):
            default = "default"
            _1st_Attack_Helicopter_Battalion_Greece = (
                "1st Attack Helicopter Battalion Greece"
            )
            _301_Squadron_Redskins_Netherlands = "301 Squadron Redskins Netherlands"
            _664_Squadron_9_Regiment_UK = "664 Squadron 9 Regiment UK"
            Archangel_4_2_ARB = "Archangel 4-2 ARB"
            Avengers_1_227th_ARB = "Avengers 1-227th ARB"
            Devils_1_1_ARB = "Devils 1-1 ARB"
            The_Air_Pirates_1_211th_ARB = "The Air Pirates 1-211th ARB"
            Silver_Spurs_3_17_CAV = "Silver Spurs 3-17 CAV"
            Grim_Reapers_4_2_ARB = "Grim Reapers 4-2 ARB"
            Killer_Bees_1_130th_ARB_NCNG = "Killer Bees 1-130th ARB NCNG"
            Gunslingers_2_159th_ARB = "Gunslingers 2-159th ARB"
            Slayers_4_2_ARB = "Slayers 4-2 ARB"
            General_Attack_Recon_Battalion = "General Attack Recon Battalion"
            Wolfpack_1_82_ARB = "Wolfpack 1-82 ARB"

        class UK(Enum):
            _664_Squadron_9_Regiment_UK = "664 Squadron 9 Regiment UK"

        class TheNetherlands(Enum):
            _301_Squadron_Redskins_Netherlands = "301 Squadron Redskins Netherlands"

        class Combined_Joint_Task_Forces_Red(Enum):
            default = "default"
            _1st_Attack_Helicopter_Battalion_Greece = (
                "1st Attack Helicopter Battalion Greece"
            )
            _301_Squadron_Redskins_Netherlands = "301 Squadron Redskins Netherlands"
            _664_Squadron_9_Regiment_UK = "664 Squadron 9 Regiment UK"
            Archangel_4_2_ARB = "Archangel 4-2 ARB"
            Avengers_1_227th_ARB = "Avengers 1-227th ARB"
            Devils_1_1_ARB = "Devils 1-1 ARB"
            The_Air_Pirates_1_211th_ARB = "The Air Pirates 1-211th ARB"
            Silver_Spurs_3_17_CAV = "Silver Spurs 3-17 CAV"
            Grim_Reapers_4_2_ARB = "Grim Reapers 4-2 ARB"
            Killer_Bees_1_130th_ARB_NCNG = "Killer Bees 1-130th ARB NCNG"
            Gunslingers_2_159th_ARB = "Gunslingers 2-159th ARB"
            Slayers_4_2_ARB = "Slayers 4-2 ARB"
            General_Attack_Recon_Battalion = "General Attack Recon Battalion"
            Wolfpack_1_82_ARB = "Wolfpack 1-82 ARB"

        class USA(Enum):
            default = "default"
            Archangel_4_2_ARB = "Archangel 4-2 ARB"
            Avengers_1_227th_ARB = "Avengers 1-227th ARB"
            Devils_1_1_ARB = "Devils 1-1 ARB"
            The_Air_Pirates_1_211th_ARB = "The Air Pirates 1-211th ARB"
            Silver_Spurs_3_17_CAV = "Silver Spurs 3-17 CAV"
            Grim_Reapers_4_2_ARB = "Grim Reapers 4-2 ARB"
            Killer_Bees_1_130th_ARB_NCNG = "Killer Bees 1-130th ARB NCNG"
            Gunslingers_2_159th_ARB = "Gunslingers 2-159th ARB"
            Slayers_4_2_ARB = "Slayers 4-2 ARB"
            General_Attack_Recon_Battalion = "General Attack Recon Battalion"
            Wolfpack_1_82_ARB = "Wolfpack 1-82 ARB"

    class Pylon1:
        M261_MK151 = (1, Weapons.M261_MK151)
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M257__Illum_ = (
            1,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M257__Illum_,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M274__Smk = (
            1,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M274__Smk,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M229__HEDP = (
            1,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M229__HEDP,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__MPP = (
            1,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__MPP,
        )
        M261_Outboard_Launcher__Zones_A_B_M151_Hydra__6PD___Zone_E_M274_Hydra__6SK_ = (
            1,
            WeaponsAH64D.M261_Outboard_Launcher__Zones_A_B_M151_Hydra__6PD___Zone_E_M274_Hydra__6SK_,
        )
        M261_Outboard_Launcher__Zones_A_B_M151_Hydra__6PD___Zone_E_M257_Hydra__6IL_ = (
            1,
            WeaponsAH64D.M261_Outboard_Launcher__Zones_A_B_M151_Hydra__6PD___Zone_E_M257_Hydra__6IL_,
        )
        M299___4_x_AGM_114K_Hellfire = (1, WeaponsAH64D.M299___4_x_AGM_114K_Hellfire)
        M299___3_x_AGM_114K_Hellfire__Port = (
            1,
            WeaponsAH64D.M299___3_x_AGM_114K_Hellfire__Port,
        )
        M299___2_x_AGM_114K_Hellfire = (1, WeaponsAH64D.M299___2_x_AGM_114K_Hellfire)
        M299___1_x_AGM_114K_Hellfire__Port = (
            1,
            WeaponsAH64D.M299___1_x_AGM_114K_Hellfire__Port,
        )
        M299___Empty_Launcher = (1, WeaponsAH64D.M299___Empty_Launcher)
        Fuel_tank_230_gal = (1, WeaponsAH64D.Fuel_tank_230_gal)

    class Pylon2:
        M261_MK151 = (2, Weapons.M261_MK151)
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M257__Illum_ = (
            2,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M257__Illum_,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M274__Smk = (
            2,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M274__Smk,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M229__HEDP = (
            2,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M229__HEDP,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__MPP = (
            2,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__MPP,
        )
        M261_Inboard_Launcher__Zone_C_M274_Hydra__6SK___Zones_D_E_M151_Hydra__6PD_ = (
            2,
            WeaponsAH64D.M261_Inboard_Launcher__Zone_C_M274_Hydra__6SK___Zones_D_E_M151_Hydra__6PD_,
        )
        M261_Inboard_Launcher__Zone_C_M257_Hydra__6IL___Zones_D_E_M151_Hydra__6PD_ = (
            2,
            WeaponsAH64D.M261_Inboard_Launcher__Zone_C_M257_Hydra__6IL___Zones_D_E_M151_Hydra__6PD_,
        )
        M299___4_x_AGM_114K_Hellfire = (2, WeaponsAH64D.M299___4_x_AGM_114K_Hellfire)
        M299___3_x_AGM_114K_Hellfire__Port = (
            2,
            WeaponsAH64D.M299___3_x_AGM_114K_Hellfire__Port,
        )
        M299___2_x_AGM_114K_Hellfire = (2, WeaponsAH64D.M299___2_x_AGM_114K_Hellfire)
        M299___1_x_AGM_114K_Hellfire__Port = (
            2,
            WeaponsAH64D.M299___1_x_AGM_114K_Hellfire__Port,
        )
        M299___Empty_Launcher = (2, WeaponsAH64D.M299___Empty_Launcher)
        Fuel_tank_230_gal = (2, WeaponsAH64D.Fuel_tank_230_gal)

    class Pylon3:
        M261_MK151 = (3, Weapons.M261_MK151)
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M257__Illum_ = (
            3,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M257__Illum_,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M274__Smk = (
            3,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M274__Smk,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M229__HEDP = (
            3,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M229__HEDP,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__MPP = (
            3,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__MPP,
        )
        M261_Inboard_Launcher__Zone_C_M274_Hydra__6SK___Zones_D_E_M151_Hydra__6PD_ = (
            3,
            WeaponsAH64D.M261_Inboard_Launcher__Zone_C_M274_Hydra__6SK___Zones_D_E_M151_Hydra__6PD_,
        )
        M261_Inboard_Launcher__Zone_C_M257_Hydra__6IL___Zones_D_E_M151_Hydra__6PD_ = (
            3,
            WeaponsAH64D.M261_Inboard_Launcher__Zone_C_M257_Hydra__6IL___Zones_D_E_M151_Hydra__6PD_,
        )
        M299___4_x_AGM_114K_Hellfire = (3, WeaponsAH64D.M299___4_x_AGM_114K_Hellfire)
        M299___3_x_AGM_114K_Hellfire__Starboard = (
            3,
            WeaponsAH64D.M299___3_x_AGM_114K_Hellfire__Starboard,
        )
        M299___2_x_AGM_114K_Hellfire = (3, WeaponsAH64D.M299___2_x_AGM_114K_Hellfire)
        M299___1_x_AGM_114K_Hellfire__Starboard = (
            3,
            WeaponsAH64D.M299___1_x_AGM_114K_Hellfire__Starboard,
        )
        M299___Empty_Launcher = (3, WeaponsAH64D.M299___Empty_Launcher)
        Fuel_tank_230_gal = (3, WeaponsAH64D.Fuel_tank_230_gal)

    class Pylon4:
        M261_MK151 = (4, Weapons.M261_MK151)
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M257__Illum_ = (
            4,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M257__Illum_,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M274__Smk = (
            4,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M274__Smk,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M229__HEDP = (
            4,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M229__HEDP,
        )
        M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__MPP = (
            4,
            WeaponsAH64D.M261_pod___19_x_2_75_Hydra__UnGd_Rkts_M282__MPP,
        )
        M261_Outboard_Launcher__Zones_A_B_M151_Hydra__6PD___Zone_E_M274_Hydra__6SK_ = (
            4,
            WeaponsAH64D.M261_Outboard_Launcher__Zones_A_B_M151_Hydra__6PD___Zone_E_M274_Hydra__6SK_,
        )
        M261_Outboard_Launcher__Zones_A_B_M151_Hydra__6PD___Zone_E_M257_Hydra__6IL_ = (
            4,
            WeaponsAH64D.M261_Outboard_Launcher__Zones_A_B_M151_Hydra__6PD___Zone_E_M257_Hydra__6IL_,
        )
        M299___4_x_AGM_114K_Hellfire = (4, WeaponsAH64D.M299___4_x_AGM_114K_Hellfire)
        M299___3_x_AGM_114K_Hellfire__Starboard = (
            4,
            WeaponsAH64D.M299___3_x_AGM_114K_Hellfire__Starboard,
        )
        M299___2_x_AGM_114K_Hellfire = (4, WeaponsAH64D.M299___2_x_AGM_114K_Hellfire)
        M299___1_x_AGM_114K_Hellfire__Starboard = (
            4,
            WeaponsAH64D.M299___1_x_AGM_114K_Hellfire__Starboard,
        )
        M299___Empty_Launcher = (4, WeaponsAH64D.M299___Empty_Launcher)
        Fuel_tank_230_gal = (4, WeaponsAH64D.Fuel_tank_230_gal)

    pylons: Set[int] = {1, 2, 3, 4}

    tasks = [task.CAS, task.GroundAttack, task.Escort, task.AFAC, task.AntishipStrike]
    task_default = task.CAS
