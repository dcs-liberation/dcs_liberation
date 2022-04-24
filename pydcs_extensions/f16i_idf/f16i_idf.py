from enum import Enum
from pathlib import Path
from typing import Dict, List, Any

from dcs import task
from dcs.planes import F_16C_50, PlaneType
from dcs.weapons_data import Weapons

from game.modsupport import planemod
from pydcs_extensions.pylon_injector import inject_pylon
from pydcs_extensions.weapon_injector import inject_weapons
from qt_ui.uiconstants import AIRCRAFT_ICONS, AIRCRAFT_BANNERS


class WeaponsF16I:
    ANAXQ_14 = {"clsid": "{ANAXQ-14}", "name": "ANAXQ-14", "weight": 0}
    AN_AAQ_13 = {"clsid": "{ANAAQ-13}", "name": "AN/AAQ-13", "weight": 211}
    Barak_lights = {"clsid": "{Barak lights}", "name": "Barak lights", "weight": 2}
    Barak_tail_1 = {"clsid": "{Barak tail 1}", "name": "Barak tail 1", "weight": 208}
    Barak_tail_2 = {"clsid": "{Barak tail 2}", "name": "Barak tail 2", "weight": 208}
    CREW = {"clsid": "{CREW}", "name": "CREW", "weight": 0}
    Crew_Ladder = {
        "clsid": "{IDF Mods Project LDR}",
        "name": "Crew Ladder",
        "weight": 0,
    }
    Delilah_cover_Pylon_3 = {
        "clsid": "{Delilah cover S 3}",
        "name": "Delilah cover Pylon 3",
        "weight": 0,
    }
    Delilah_cover_Pylon_3_7 = {
        "clsid": "{Delilah cover S 3-7}",
        "name": "Delilah cover Pylon 3-7",
        "weight": 0,
    }
    Delilah_cover_Pylon_7 = {
        "clsid": "{Delilah cover S 7}",
        "name": "Delilah cover Pylon 7",
        "weight": 0,
    }
    Fuel_tank_300_gal_ = {
        "clsid": "{IDF Mods Project 300gal}",
        "name": "Fuel tank 300 gal",
        "weight": 1197.4895155,
    }
    Fuel_tank_300_gal__ = {
        "clsid": "{F14-300gal}",
        "name": "Fuel tank 300 gal",
        "weight": 958.4,
    }
    Fuel_tank_600_gal = {
        "clsid": "{600gal}",
        "name": "Fuel tank 600 gal",
        "weight": 2107.806774925,
    }
    Fuel_tank_600_gal__EMPTY_ = {
        "clsid": "{600gal_Empty}",
        "name": "Fuel tank 600 gal *EMPTY*",
        "weight": 172,
    }
    IDF_Mods_Project_Fuel_Tank_370_EMPTY = {
        "clsid": "{IDF Mods Project Fuel Tank 370 EMPTY}",
        "name": "IDF Mods Project Fuel Tank 370 EMPTY",
        "weight": 250,
    }
    IDF_Mods_Project_F_16I_CFT = {
        "clsid": "{IDF Mods Project F-16I CFT}",
        "name": "IDF Mods Project F-16I CFT",
        "weight": 408,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Left}",
        "name": "IDF Mods Project F-16I CFT Fuel Left 1500lb",
        "weight": 884.0827540681,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Left + Fuel Tank 370}",
        "name": "IDF Mods Project F-16I CFT Fuel Left 1500lb + 370Gal",
        "weight": 2063.8845750252,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal = {
        "clsid": "{600gal+CFT Fuel Left 1500lb}",
        "name": "IDF Mods Project F-16I CFT Fuel Left 1500lb + 600Gal",
        "weight": 2991.8895289931,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Right}",
        "name": "IDF Mods Project F-16I CFT Fuel Right 1500lb",
        "weight": 884.0827540681,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal = {
        "clsid": "{IDF Mods Project F-16I CFT Fuel Right + Fuel Tank 370}",
        "name": "IDF Mods Project F-16I CFT Fuel Right 1500lb + 370Gal",
        "weight": 2063.8845750252,
    }
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal = {
        "clsid": "{600gal+CFT Fuel Right 1500lb}",
        "name": "IDF Mods Project F-16I CFT Fuel Right 1500lb + 600Gal",
        "weight": 2991.8895289931,
    }
    Python_5_Cover_Pylon_2 = {
        "clsid": "{Python 5 cover S 2}",
        "name": "Python 5 Cover Pylon 2",
        "weight": 0,
    }
    Python_5_Cover_Pylon_2_8 = {
        "clsid": "{Python 5 cover S 2-8}",
        "name": "Python 5 Cover Pylon 2-8",
        "weight": 0,
    }
    Python_5_Cover_Pylon_8 = {
        "clsid": "{Python 5 cover S 8}",
        "name": "Python 5 Cover Pylon 8",
        "weight": 0,
    }
    Remove_Before_Flight = {
        "clsid": "{IDF Mods Project RBF}",
        "name": "Remove Before Flight",
        "weight": 0,
    }
    Remove_Before_Flight_without_Lantirn = {
        "clsid": "{IDF Mods Project Remove Before Flight without Lantirn}",
        "name": "Remove Before Flight without Lantirn",
        "weight": 0,
    }
    Remove_Before_Flight_without_TGP_ = {
        "clsid": "{IDF Mods Project Remove Before Flight without TGP}",
        "name": "Remove Before Flight without TGP ",
        "weight": 0,
    }
    Remove_Before_Flight_without_TGP_And_Lantirn = {
        "clsid": "{Remove Before Flight without TGP And Lantirn}",
        "name": "Remove Before Flight without TGP And Lantirn",
        "weight": 0,
    }
    Spice_2000_Cover_Pylon_3 = {
        "clsid": "{Spice 2000 cov S 4}",
        "name": "Spice 2000 Cover Pylon 3",
        "weight": 0,
    }
    Spice_2000_Cover_Pylon_3_7 = {
        "clsid": "{Spice 2000 cov S 4-6}",
        "name": "Spice 2000 Cover Pylon 3-7",
        "weight": 0,
    }
    Spice_2000_Cover_Pylon_7 = {
        "clsid": "{Spice 2000 cov S 6}",
        "name": "Spice 2000 Cover Pylon 7",
        "weight": 0,
    }
    # LAU_7_with_Python_5_ = {"clsid": "{AIM-9X-ON-ADAPTER}", "name": "LAU-7 with Python-5 ", "weight": 120}
    # Python_5_ = {"clsid": "{5CE2FF2A-645A-4197-B48D-8720AC69394F}", "name": "Python-5 ", "weight": 105}
    Python_5_Training = {
        "clsid": "{Python-5 Training}",
        "name": "Python-5 Training",
        "weight": 105,
    }
    Delilah = {"clsid": "{AGM-154A}", "name": "Delilah", "weight": 250}
    # Spice_1000 = {"clsid": "{AGM-154A}", "name": "Spice-1000", "weight": 450}


class F16IPylon3:
    GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
        3,
        Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
    )


class F16IPylon4:
    Fuel_tank_600_gal = (4, WeaponsF16I.Fuel_tank_600_gal)
    Fuel_tank_600_gal__EMPTY_ = (4, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
    IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
        4,
        WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb = (
        4,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal = (
        4,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__600Gal,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal = (
        4,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Left_1500lb__370Gal,
    )
    GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
        4,
        Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
    )


class F16IPylon5:
    Fuel_tank_300_gal_ = (5, Weapons.Fuel_tank_300_gal_)
    Fuel_tank_300_gal__ = (5, WeaponsF16I.Fuel_tank_300_gal_)
    Fuel_tank_300_gal___ = (5, WeaponsF16I.Fuel_tank_300_gal__)
    ANAXQ_14 = (5, WeaponsF16I.ANAXQ_14)


class F16IPylon6:
    Fuel_tank_600_gal = (6, WeaponsF16I.Fuel_tank_600_gal)
    Fuel_tank_600_gal__EMPTY_ = (6, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
    IDF_Mods_Project_Fuel_Tank_370_EMPTY = (
        6,
        WeaponsF16I.IDF_Mods_Project_Fuel_Tank_370_EMPTY,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb = (
        6,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal = (
        6,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__370Gal,
    )
    IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal = (
        6,
        WeaponsF16I.IDF_Mods_Project_F_16I_CFT_Fuel_Right_1500lb__600Gal,
    )
    GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
        6,
        Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
    )


class F16IPylon7:
    GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
        7,
        Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
    )


class F16IPylon10:
    AN_AAQ_13 = (10, WeaponsF16I.AN_AAQ_13)


class Pylon12:
    ALQ_184 = (12, Weapons.ALQ_184)


class Pylon13:
    Crew_Ladder = (13, WeaponsF16I.Crew_Ladder)


class Pylon14:
    Remove_Before_Flight = (14, WeaponsF16I.Remove_Before_Flight)
    Remove_Before_Flight_without_Lantirn = (
        14,
        WeaponsF16I.Remove_Before_Flight_without_Lantirn,
    )
    Remove_Before_Flight_without_TGP_ = (
        14,
        WeaponsF16I.Remove_Before_Flight_without_TGP_,
    )
    Remove_Before_Flight_without_TGP_And_Lantirn = (
        14,
        WeaponsF16I.Remove_Before_Flight_without_TGP_And_Lantirn,
    )


class Pylon15:
    Python_5_Cover_Pylon_2 = (15, WeaponsF16I.Python_5_Cover_Pylon_2)
    Python_5_Cover_Pylon_8 = (15, WeaponsF16I.Python_5_Cover_Pylon_8)
    Python_5_Cover_Pylon_2_8 = (15, WeaponsF16I.Python_5_Cover_Pylon_2_8)


class Pylon16:
    Spice_2000_Cover_Pylon_3 = (16, WeaponsF16I.Spice_2000_Cover_Pylon_3)
    Spice_2000_Cover_Pylon_7 = (16, WeaponsF16I.Spice_2000_Cover_Pylon_7)
    Spice_2000_Cover_Pylon_3_7 = (16, WeaponsF16I.Spice_2000_Cover_Pylon_3_7)
    IDF_Mods_Project_F_16I_CFT = (16, WeaponsF16I.IDF_Mods_Project_F_16I_CFT)


inject_weapons(WeaponsF16I)


def inject_F16I() -> None:
    from qt_ui.main import inject_custom_payloads, THIS_DIR

    # Injects modified weapons from the IDF Mods Project F-16I Sufa
    # into pydcs databases via introspection.
    AIRCRAFT_ICONS["F-16C_50"] = AIRCRAFT_ICONS["F-16I"]
    AIRCRAFT_BANNERS["F-16C_50"] = AIRCRAFT_BANNERS["F-16I"]
    setattr(F_16C_50, "fuel_max", 2585.48)
    F_16C_50.pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}
    inject_pylon(F_16C_50.Pylon3, F16IPylon3)
    inject_pylon(F_16C_50.Pylon4, F16IPylon4)
    inject_pylon(F_16C_50.Pylon5, F16IPylon5)
    inject_pylon(F_16C_50.Pylon6, F16IPylon6)
    inject_pylon(F_16C_50.Pylon7, F16IPylon7)
    inject_pylon(F_16C_50.Pylon10, F16IPylon10)
    F_16C_50.Pylon12 = Pylon12
    F_16C_50.Pylon13 = Pylon13
    F_16C_50.Pylon14 = Pylon14
    F_16C_50.Pylon15 = Pylon15
    F_16C_50.Pylon16 = Pylon16
    inject_custom_payloads(Path(THIS_DIR.parent / "resources/mod_payloads/f16i_idf"))


@planemod
class F_16I(PlaneType):
    id = "F-16I"
    flyable = True
    height = 5.02
    width = 9.45
    length = 14.52
    fuel_max = 3249
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 127,
                2: 135,
                4: 127,
                8: 128,
                16: 132,
                17: 138,
                9: 126,
                18: 122,
                5: 125,
                10: 133,
                20: 137,
                11: 130,
                3: 136,
                6: 121,
                12: 139,
                13: 140,
                7: 141,
                14: 131,
                19: 124,
                15: 134,
            },
        },
    }

    property_defaults: Dict[str, Any] = {
        "LAU3ROF": 0,
        "LaserCode100": 6,
        "LaserCode10": 8,
        "LaserCode1": 8,
        "HelmetMountedDevice": 1,
    }

    class Properties:
        class LAU3ROF:
            id = "LAU3ROF"

            class Values:
                Single = 0
                Ripple = 1

        class LaserCode100:
            id = "LaserCode100"

        class LaserCode10:
            id = "LaserCode10"

        class LaserCode1:
            id = "LaserCode1"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

    class Liveries:
        class USSR(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Georgia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Venezuela(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Australia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Israel(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Combined_Joint_Task_Forces_Blue(Enum):
            default = "default"
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Sudan(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Norway(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Romania(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Iran(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Ukraine(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Libya(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Belgium(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Slovakia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Greece(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class UK(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Third_Reich(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Hungary(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Abkhazia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Morocco(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class United_Nations_Peacekeepers(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Switzerland(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class SouthOssetia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Vietnam(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class China(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Yemen(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Kuwait(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Serbia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Oman(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class India(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Egypt(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class TheNetherlands(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Poland(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Syria(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Finland(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Kazakhstan(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Denmark(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Sweden(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Croatia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class CzechRepublic(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class GDR(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Yugoslavia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Bulgaria(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class SouthKorea(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Tunisia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Combined_Joint_Task_Forces_Red(Enum):
            default = "default"
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Lebanon(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Portugal(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Cuba(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Insurgents(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class SaudiArabia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class France(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class USA(Enum):
            default = "default"
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Honduras(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Qatar(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Russia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class United_Arab_Emirates(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Italian_Social_Republi(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Austria(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Bahrain(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Italy(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Chile(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Turkey(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Philippines(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Algeria(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Pakistan(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Malaysia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Indonesia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Iraq(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Germany(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class South_Africa(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Jordan(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Mexico(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class USAFAggressors(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Brazil(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Spain(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Belarus(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Canada(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class NorthKorea(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Ethiopia(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Japan(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

        class Thailand(Enum):
            IAF_F_16I_107_Sqn = "IAF F-16I 107 Sqn"
            IAF_F_16I_119_Sqn = "IAF F-16I 119 Sqn"
            IAF_F_16I_201_Sqn = "IAF F-16I 201 Sqn"
            IAF_F_16I_253_Sqn = "IAF F-16I 253 Sqn"
            F16I___107___SUFA = "F16I - 107 - SUFA"
            F16I___119___SUFA = "F16I - 119 - SUFA"
            F16I___201__SUFA = "F16I - 201- SUFA"
            F16I___253___SUFA = "F16I - 253 - SUFA"
            F16I___5601___SUFA = "F16I - 5601 - SUFA"
            Polish = "Polish"
            Banshee_F16I___SUFA___Experimental___Released = (
                "Banshee F16I - SUFA - Experimental - Released"
            )
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"
            IAF_110th_squadron = "IAF 110th squadron"
            IAF_110th_squadron_60th_anniversary = "IAF 110th squadron 60th anniversary"
            IAF_110th_squadron_barak_2020 = "IAF 110th squadron barak 2020"
            IAF_110th_squadron_barak_2020___60th_anniversary = (
                "IAF 110th squadron barak 2020 + 60th anniversary"
            )
            IAF_115th_aggressors_squadron = "IAF 115th aggressors squadron"
            IAF_115th_aggressors_squadron_60th_anniversary = (
                "IAF 115th aggressors squadron 60th anniversary"
            )
            IAF_115th_aggressors_squadron_barak_2020 = (
                "IAF 115th aggressors squadron barak 2020"
            )
            IAF_115th_aggressors_squadron_barak_2020___60th_anniversary = (
                "IAF 115th aggressors squadron barak 2020 + 60th anniversary"
            )
            IAF_117th_squadron = "IAF 117th squadron"
            IAF_117th_squadron_60th_anniversary = "IAF 117th squadron 60th anniversary"
            IAF_117th_squadron_barak_2020 = "IAF 117th squadron barak 2020"
            IAF_117th_squadron_barak_2020___60th_anniversary = (
                "IAF 117th squadron barak 2020 + 60th anniversary"
            )

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (1, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (1, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            1,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (1, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (2, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (2, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            2,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (2, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (2, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    # ERRR <CLEAN>

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (3, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            3,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (3, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            3,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (3, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (3, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (3, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            3,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        MXU_648_TP = (3, Weapons.MXU_648_TP)
        ALQ_184 = (3, Weapons.ALQ_184)
        ALQ_184_Long = (3, Weapons.ALQ_184_Long)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H_2_L = (3, Weapons.LAU_88_AGM_65H_2_L)

    class Pylon4:
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            4,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            4,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        Fuel_tank_370_gal = (4, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (4, Weapons.MXU_648_TP)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )

    class Pylon5:
        Fuel_tank_300_gal = (5, Weapons.Fuel_tank_300_gal)
        MXU_648_TP = (5, Weapons.MXU_648_TP)

    # ERRR <CLEAN>

    class Pylon6:
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_WP1B = (6, Weapons.LAU3_WP1B)
        LAU3_WP61 = (6, Weapons.LAU3_WP61)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            6,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            6,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        Fuel_tank_370_gal = (6, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (6, Weapons.MXU_648_TP)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (7, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (7, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            7,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (7, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (7, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_WP1B = (7, Weapons.LAU3_WP1B)
        LAU3_WP61 = (7, Weapons.LAU3_WP61)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            7,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (7, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (7, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (7, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        MXU_648_TP = (7, Weapons.MXU_648_TP)
        ALQ_184 = (7, Weapons.ALQ_184)
        ALQ_184_Long = (7, Weapons.ALQ_184_Long)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__,
        )
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (8, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (8, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            8,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (8, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (9, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            9,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (9, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon10:
        AN_ASQ_213_HTS___HARM_Targeting_System = (
            10,
            Weapons.AN_ASQ_213_HTS___HARM_Targeting_System,
        )

    class Pylon11:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            11,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )

    class Pylon12:
        ALQ_184 = (12, Weapons.ALQ_184)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP


@planemod
class F_16C_BARAK_2020(PlaneType):
    id = "F-16C-BARAK 2020"
    flyable = True
    height = 5.02
    width = 9.45
    length = 14.52
    fuel_max = 3249
    max_speed = 2120.04
    chaff = 60
    flare = 60
    charge_total = 120
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 305

    panel_radio = {
        1: {
            "channels": {
                1: 305,
                2: 264,
                4: 256,
                8: 257,
                16: 261,
                17: 267,
                9: 255,
                18: 251,
                5: 254,
                10: 262,
                20: 266,
                11: 259,
                3: 265,
                6: 250,
                12: 268,
                13: 269,
                7: 270,
                14: 260,
                19: 253,
                15: 263,
            },
        },
        2: {
            "channels": {
                1: 127,
                2: 135,
                4: 127,
                8: 128,
                16: 132,
                17: 138,
                9: 126,
                18: 122,
                5: 125,
                10: 133,
                20: 137,
                11: 130,
                3: 136,
                6: 121,
                12: 139,
                13: 140,
                7: 141,
                14: 131,
                19: 124,
                15: 134,
            },
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Viper",
            "Venom",
            "Lobo",
            "Cowboy",
            "Python",
            "Rattler",
            "Panther",
            "Wolf",
            "Weasel",
            "Wild",
            "Ninja",
            "Jedi",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "LAU3ROF": 0,
        "LaserCode100": 6,
        "LaserCode10": 8,
        "LaserCode1": 8,
        "HelmetMountedDevice": 1,
    }

    class Properties:
        class LAU3ROF:
            id = "LAU3ROF"

            class Values:
                Single = 0
                Ripple = 1

        class LaserCode100:
            id = "LaserCode100"

        class LaserCode10:
            id = "LaserCode10"

        class LaserCode1:
            id = "LaserCode1"

        class HelmetMountedDevice:
            id = "HelmetMountedDevice"

            class Values:
                Not_installed = 0
                JHMCS = 1
                NVG = 2

    class Liveries:
        class USSR(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Georgia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Venezuela(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Australia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Israel(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Combined_Joint_Task_Forces_Blue(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Sudan(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Norway(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Romania(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Iran(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Ukraine(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Libya(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Belgium(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Slovakia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Greece(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class UK(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Third_Reich(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Hungary(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Abkhazia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Morocco(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class United_Nations_Peacekeepers(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Switzerland(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class SouthOssetia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Vietnam(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class China(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Yemen(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Kuwait(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Serbia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Oman(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class India(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Egypt(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class TheNetherlands(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Poland(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Syria(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Finland(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Kazakhstan(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Denmark(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Sweden(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Croatia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class CzechRepublic(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class GDR(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Yugoslavia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Bulgaria(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class SouthKorea(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Tunisia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Combined_Joint_Task_Forces_Red(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Lebanon(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Portugal(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Cuba(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Insurgents(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class SaudiArabia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class France(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class USA(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Honduras(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Qatar(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Russia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class United_Arab_Emirates(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Italian_Social_Republi(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Austria(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Bahrain(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Italy(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Chile(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Turkey(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Philippines(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Algeria(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Pakistan(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Malaysia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Indonesia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Iraq(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Germany(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class South_Africa(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Jordan(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Mexico(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class USAFAggressors(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Brazil(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Spain(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Belarus(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Canada(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class NorthKorea(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Ethiopia(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Japan(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

        class Thailand(Enum):
            IAF_101st_squadron = "IAF 101st squadron"
            IAF_101st_squadron_barak_2020 = "IAF 101st squadron barak 2020"

    class Pylon1:
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (1, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (1, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            1,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (1, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (1, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon2:
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (2, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (2, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            2,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (2, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (2, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    # ERRR <CLEAN>

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (3, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (3, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            3,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (3, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (3, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU3_WP1B = (3, Weapons.LAU3_WP1B)
        LAU3_WP61 = (3, Weapons.LAU3_WP61)
        LAU3_HE5 = (3, Weapons.LAU3_HE5)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            3,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            3,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (3, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (3, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (3, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            3,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (3, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (3, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (3, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            3,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (3, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (3, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            3,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (3, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (3, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (3, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            3,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            3,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            3,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (3, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            3,
            Weapons.BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            3,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            3,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        MXU_648_TP = (3, Weapons.MXU_648_TP)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            3,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            3,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            3,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H_2_L = (3, Weapons.LAU_88_AGM_65H_2_L)

    class Pylon4:
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU3_WP1B = (4, Weapons.LAU3_WP1B)
        LAU3_WP61 = (4, Weapons.LAU3_WP61)
        LAU3_HE5 = (4, Weapons.LAU3_HE5)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            4,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            4,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (4, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (4, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (4, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            4,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (4, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (4, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (4, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            4,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        Fuel_tank_370_gal = (4, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (4, Weapons.MXU_648_TP)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        # ERRR <CLEAN>
        Fuel_tank_600_gal = (4, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (4, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            4,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            4,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            4,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )

    class Pylon5:
        Fuel_tank_300_gal = (5, Weapons.Fuel_tank_300_gal)

    # ERRR {fuel_tank_300gal Empty}
    # ERRR <CLEAN>

    class Pylon6:
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU3_WP1B = (6, Weapons.LAU3_WP1B)
        LAU3_WP61 = (6, Weapons.LAU3_WP61)
        LAU3_HE5 = (6, Weapons.LAU3_HE5)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            6,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            6,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (6, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (6, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            6,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (6, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            6,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (6, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (6, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (6, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_87___202_x_CEM_Cluster_Bomb,
        )
        TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb = (
            6,
            Weapons.TER_9A_with_3_x_CBU_97___10_x_SFW_Cluster_Bomb,
        )
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            6,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        Fuel_tank_370_gal = (6, Weapons.Fuel_tank_370_gal)
        MXU_648_TP = (6, Weapons.MXU_648_TP)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            6,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        # ERRR <CLEAN>
        Fuel_tank_600_gal = (6, WeaponsF16I.Fuel_tank_600_gal)
        Fuel_tank_600_gal__EMPTY_ = (6, WeaponsF16I.Fuel_tank_600_gal__EMPTY_)
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            6,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            6,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            6,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (7, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (7, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (7, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            7,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (7, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (7, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)
        LAU3_WP156 = (7, Weapons.LAU3_WP156)
        LAU3_WP1B = (7, Weapons.LAU3_WP1B)
        LAU3_WP61 = (7, Weapons.LAU3_WP61)
        LAU3_HE5 = (7, Weapons.LAU3_HE5)
        LAU3_HE151 = (7, Weapons.LAU3_HE151)
        BDU_50LD___500lb_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LD___500lb_Inert_Practice_Bomb_LD,
        )
        BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD = (
            7,
            Weapons.BDU_50LGB___500lb_Laser_Guided_Inert_Practice_Bomb_LD,
        )
        BDU_50HD___500lb_Inert_Practice_Bomb_HD = (
            7,
            Weapons.BDU_50HD___500lb_Inert_Practice_Bomb_HD,
        )
        Mk_82___500lb_GP_Bomb_LD = (7, Weapons.Mk_82___500lb_GP_Bomb_LD)
        Mk_82_Snakeye___500lb_GP_Bomb_HD = (7, Weapons.Mk_82_Snakeye___500lb_GP_Bomb_HD)
        Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82___500lb_GP_Bomb_LD,
        )
        TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_Snakeye___500lb_GP_Bomb_HD,
        )
        TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD = (
            7,
            Weapons.TER_9A_with_3_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD,
        )
        Mk_84___2000lb_GP_Bomb_LD = (7, Weapons.Mk_84___2000lb_GP_Bomb_LD)
        GBU_10___2000lb_Laser_Guided_Bomb = (
            7,
            Weapons.GBU_10___2000lb_Laser_Guided_Bomb,
        )
        GBU_12___500lb_Laser_Guided_Bomb = (7, Weapons.GBU_12___500lb_Laser_Guided_Bomb)
        CBU_87___202_x_CEM_Cluster_Bomb = (7, Weapons.CBU_87___202_x_CEM_Cluster_Bomb)
        CBU_97___10_x_SFW_Cluster_Bomb = (7, Weapons.CBU_97___10_x_SFW_Cluster_Bomb)
        TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD = (
            7,
            Weapons.TER_9A_with_3_x_BDU_33___25lb_Practice_Bomb_LD,
        )
        LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_117_AGM_65G = (7, Weapons.LAU_117_AGM_65G)
        LAU_117_AGM_65H = (7, Weapons.LAU_117_AGM_65H)
        LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_ = (
            7,
            Weapons.LAU_117_with_AGM_65K___Maverick_K__CCD_Imp_ASM_,
        )
        LAU_88_AGM_65D_ONE = (7, Weapons.LAU_88_AGM_65D_ONE)
        LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_ = (
            7,
            Weapons.LAU_88_with_3_x_AGM_65D___Maverick_D__IIR_ASM_,
        )
        LAU_88_AGM_65H = (7, Weapons.LAU_88_AGM_65H)
        LAU_88_AGM_65H_3 = (7, Weapons.LAU_88_AGM_65H_3)
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            7,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_31_V_1_B___JDAM__2000lb_GPS_Guided_Bomb,
        )
        GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb = (
            7,
            Weapons.GBU_31_V_3_B___JDAM__2000lb_GPS_Guided_Penetrator_Bomb,
        )
        GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb = (
            7,
            Weapons.BRU_57_with_2_x_GBU_38___JDAM__500lb_GPS_Guided_Bomb,
        )
        AGM_154A___JSOW_CEB__CBU_type_ = (7, Weapons.AGM_154A___JSOW_CEB__CBU_type_)
        BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_ = (
            7,
            Weapons.BRU_57_with_2_x_AGM_154A___JSOW_CEB__CBU_type_,
        )
        CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_105___10_x_SFW__CBU_with_WCMD,
        )
        CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD = (
            7,
            Weapons.BRU_57_with_2_x_CBU_103___202_x_CEM__CBU_with_WCMD,
        )
        GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.GBU_24_Paveway_III___2000lb_Laser_Guided_Bomb_,
        )
        MXU_648_TP = (7, Weapons.MXU_648_TP)
        # ERRR <CLEAN>
        TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82___500lb_GP_Bomb_LD_,
        )
        TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_Snakeye___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_ = (
            7,
            Weapons.TER_9A_with_2_x_Mk_82_AIR_Ballute___500lb_GP_Bomb_HD_,
        )
        TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_GBU_12___500lb_Laser_Guided_Bomb_,
        )
        TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_87___202_x_CEM_Cluster_Bomb_,
        )
        TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_ = (
            7,
            Weapons.TER_9A_with_2_x_CBU_97___10_x_SFW_Cluster_Bomb_,
        )
        LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__ = (
            7,
            Weapons.LAU_88_with_2_x_AGM_65D___Maverick_D__IIR_ASM__,
        )
        LAU_88_AGM_65H_2_R = (7, Weapons.LAU_88_AGM_65H_2_R)

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (8, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (8, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (8, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            8,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (8, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (8, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    # ERRR <CLEAN>

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9L_Sidewinder_IR_AAM = (9, Weapons.AIM_9L_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120B_AMRAAM___Active_Rdr_AAM = (9, Weapons.AIM_120B_AMRAAM___Active_Rdr_AAM)
        AIM_120C_5_AMRAAM___Active_Rdr_AAM = (
            9,
            Weapons.AIM_120C_5_AMRAAM___Active_Rdr_AAM,
        )
        CATM_9M = (9, Weapons.CATM_9M)
        AN_ASQ_T50_TCTS_Pod___ACMI_Pod = (9, Weapons.AN_ASQ_T50_TCTS_Pod___ACMI_Pod)

    class Pylon10:
        AN_ASQ_213_HTS___HARM_Targeting_System = (
            10,
            Weapons.AN_ASQ_213_HTS___HARM_Targeting_System,
        )

    class Pylon11:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            11,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )

    class Pylon12:
        Barak_tail_1 = (12, WeaponsF16I.Barak_tail_1)
        Barak_tail_2 = (12, WeaponsF16I.Barak_tail_2)

    class Pylon13:
        Barak_lights = (13, WeaponsF16I.Barak_lights)

    class Pylon14:
        ALQ_184 = (14, Weapons.ALQ_184)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.PinpointStrike,
        task.CAS,
        task.GroundAttack,
        task.RunwayAttack,
        task.SEAD,
        task.AFAC,
        task.AntishipStrike,
        task.Reconnaissance,
    ]
    task_default = task.CAP
