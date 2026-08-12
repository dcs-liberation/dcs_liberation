from typing import Any, Dict, List, Set

from dcs import task
from dcs.helicopters import HelicopterType
from dcs.planes import PlaneType
from dcs.unitpropertydescription import UnitPropertyDescription
from dcs.weapons_data import Weapons

from game.modsupport import helicoptermod, planemod
from pydcs_extensions.weapon_injector import inject_weapons


class WeaponsUH60L:
    Cargo_Seats__Rear_Row_ = {
        "clsid": "{UH60_SEAT_CARGO_REAR}",
        "name": "Cargo Seats (Rear Row)",
        "weight": 20,
    }
    Cargo_Seats__Three_Rows_ = {
        "clsid": "{UH60_SEAT_CARGO_ALL}",
        "name": "Cargo Seats (Three Rows)",
        "weight": 20,
    }
    Dual_Internal_Auxiliary_Fuel_Transfer_System__336_Gallons_ = {
        "clsid": "{UH60_IAFTS}",
        "name": "Dual Internal Auxiliary Fuel Transfer System (336 Gallons)",
        "weight": 1430.8,
    }
    Empty_Gunner_Seat = {
        "clsid": "{UH60_SEAT_GUNNER_L}",
        "name": "Empty Gunner Seat",
        "weight": 20,
    }
    Empty_Gunner_Seat_ = {
        "clsid": "{UH60_SEAT_GUNNER_R}",
        "name": "Empty Gunner Seat",
        "weight": 20,
    }
    GAU_19 = {"clsid": "{UH60_GAU19_LEFT}", "name": "GAU-19", "weight": 172.3}
    GAU_19_ = {"clsid": "{UH60_GAU19_RIGHT}", "name": "GAU-19", "weight": 172.3}
    M134 = {"clsid": "{UH60_M134_LEFT}", "name": "M134", "weight": 68.7}
    M134_ = {"clsid": "{UH60_M134_RIGHT}", "name": "M134", "weight": 68.7}
    M134_Door_Gun = {
        "clsid": "{UH60L_M134_GUNNER}",
        "name": "M134 Door Gun",
        "weight": 180,
    }
    M3M_Door_Gun = {"clsid": "{UH60L_M2_GUNNER}", "name": "M3M Door Gun", "weight": 180}
    M60_Door_Gun = {
        "clsid": "{UH60L_M60_GUNNER}",
        "name": "M60 Door Gun",
        "weight": 180,
    }
    M_230__30MM_M789_HEDP__600_rnds_ = {
        "clsid": "{UH60_M230_LEFT}",
        "name": "M-230, 30MM M789 HEDP (600 rnds)",
        "weight": 60,
    }
    M_230__30MM_M789_HEDP__600_rnds__ = {
        "clsid": "{UH60_M230_RIGHT}",
        "name": "M-230, 30MM M789 HEDP (600 rnds)",
        "weight": 60,
    }
    UH60_LWL12_APKWS = {
        "clsid": "UH60_LWL12_APKWS",
        "name": 'LWL-12 - 12 x 2.75" Hydra, Laser Guided Rkts M151, HE APKWS',
        "weight": 214.5,
    }
    UH60_LWL12_M151 = {
        "clsid": "UH60_LWL12_M151",
        "name": 'LWL-12 - 12 x 2.75" Hydra, UnGd Rkts M151, HE',
        "weight": 81.3,
    }
    UH60_LWL12_M156 = {
        "clsid": "UH60_LWL12_M156",
        "name": 'LWL-12 - 12 x 2.75" Hydra, UnGd Rkts M156, Wht Phos',
        "weight": 87.3,
    }
    UH60_LWL12_M229 = {
        "clsid": "UH60_LWL12_M229",
        "name": 'LWL-12 - 12 x 2.75" Hydra, UnGd Rkts M229, HE',
        "weight": 87.3,
    }
    UH60_LWL12_M257 = {
        "clsid": "UH60_LWL12_M257",
        "name": 'LWL-12 - 12 x 2.75" Hydra, UnGd Rkts M257, Para Illum',
        "weight": 94.5,
    }
    UH60_LWL12_M259 = {
        "clsid": "UH60_LWL12_M259",
        "name": 'LWL-12 - 12 x 2.75" Hydra, UnGd Rkts M259, Smoke Marker',
        "weight": 94.5,
    }
    UH60_LWL12_M274 = {
        "clsid": "UH60_LWL12_M274",
        "name": 'LWL-12 - 12 x 2.75" Hydra, UnGd Rkts M274, Practice Smk',
        "weight": 84.9,
    }
    _200_Gallon_CEFS_Aux_Tank = {
        "clsid": "{UH60_FUEL_TANK_200}",
        "name": "200 Gallon CEFS Aux Tank",
        "weight": 754.1,
    }
    _230_Gallon_Aux_Tank = {
        "clsid": "{UH60_FUEL_TANK_230}",
        "name": "230 Gallon Aux Tank",
        "weight": 746.3,
    }
    _450_Gallon_Aux_Tank = {
        "clsid": "{UH60_FUEL_TANK_450}",
        "name": "450 Gallon Aux Tank",
        "weight": 1451.4,
    }


inject_weapons(WeaponsUH60L)


@helicoptermod
class UH_60L_DAP(HelicopterType):
    id = "UH-60L_DAP"
    flyable = True
    height = 5.13
    width = 16.4
    length = 19.76
    fuel_max = 1362
    max_speed = 355.584
    chaff = 30
    flare = 60
    charge_total = 90
    chaff_charge_size = 1
    flare_charge_size = 1
    radio_frequency = 116

    panel_radio = {
        2: {
            "channels": {
                1: 264,
                2: 265,
                4: 254,
                8: 258,
                16: 267,
                17: 251,
                9: 262,
                18: 253,
                5: 250,
                10: 259,
                20: 252,
                11: 268,
                3: 256,
                6: 270,
                12: 269,
                13: 260,
                7: 257,
                14: 263,
                19: 266,
                15: 261,
            },
        },
        3: {
            "channels": {
                1: 138,
                2: 121.5,
                4: 127.5,
                8: 135,
                16: 118.45,
                17: 134,
                9: 136,
                18: 134.5,
                5: 130,
                10: 139,
                20: 137.5,
                11: 151,
                3: 127,
                6: 133,
                12: 118.5,
                13: 118.1,
                7: 133.5,
                14: 118.9,
                19: 137,
                15: 118.4,
            },
        },
        1: {
            "channels": {6: 41, 2: 31, 8: 50, 3: 32, 1: 30, 4: 33, 5: 40, 7: 42},
        },
        4: {
            "channels": {6: 41, 2: 31, 8: 50, 3: 32, 1: 30, 4: 33, 5: 40, 7: 42},
        },
        5: {
            "channels": {1: 3, 2: 10},
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Jolly",
            "Pedro",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "FuelProbeEnabled": True,
        "NetCrewControlPriority": 1,
    }

    class Properties:

        class FuelProbeEnabled:
            id = "FuelProbeEnabled"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                Instructor = 1
                Ask_Always = -1
                Equally_Responsible = -2

    properties = {
        "FuelProbeEnabled": UnitPropertyDescription(
            identifier="FuelProbeEnabled",
            control="checkbox",
            label="Enable Fuel Probe",
            default=True,
            weight_when_on=0,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Pilot",
                1: "Instructor",
                -1: "Ask Always",
                -2: "Equally Responsible",
            },
        ),
    }

    livery_name = "UH-60L_DAP"  # from type

    class Pylon1:
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            1,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            1,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE = (
            1,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL = (
            1,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM = (
            1,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM = (
            1,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M260___7_x_Laser_Guided_Rkts__70_mm_Hydra_70_M151_HE_APKWS = (
            1,
            Weapons.M260___7_x_Laser_Guided_Rkts__70_mm_Hydra_70_M151_HE_APKWS,
        )
        # ERRR {M261_MK151}
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE__M433_RC_Fuze = (
            1,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE__M433_RC_Fuze,
        )
        # ERRR {M261_MK156}
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE = (
            1,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL = (
            1,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM = (
            1,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM = (
            1,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M282_MPP = (
            1,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M282_MPP,
        )
        UH60_LWL12_M151 = (1, Weapons.UH60_LWL12_M151)
        UH60_LWL12_M156 = (1, Weapons.UH60_LWL12_M156)
        UH60_LWL12_M229 = (1, Weapons.UH60_LWL12_M229)
        UH60_LWL12_M257 = (1, Weapons.UH60_LWL12_M257)
        UH60_LWL12_M259 = (1, Weapons.UH60_LWL12_M259)
        UH60_LWL12_M274 = (1, Weapons.UH60_LWL12_M274)
        UH60_LWL12_APKWS = (1, Weapons.UH60_LWL12_APKWS)
        OH58D_FIM_92_L = (1, Weapons.OH58D_FIM_92_L)
        # ERRR UH60_AGM_114_L1
        # ERRR UH60_AGM_114_L
        M299___Empty_Launcher = (1, Weapons.M299___Empty_Launcher)
        M299___4_x_AGM_114K_Hellfire = (1, Weapons.M299___4_x_AGM_114K_Hellfire)
        M299___3_x_AGM_114K_Hellfire__Port = (
            1,
            Weapons.M299___3_x_AGM_114K_Hellfire__Port,
        )
        M299___3_x_AGM_114K_Hellfire__Starboard = (
            1,
            Weapons.M299___3_x_AGM_114K_Hellfire__Starboard,
        )
        M299___2_x_AGM_114K_Hellfire = (1, Weapons.M299___2_x_AGM_114K_Hellfire)
        M299___1_x_AGM_114K_Hellfire__Port = (
            1,
            Weapons.M299___1_x_AGM_114K_Hellfire__Port,
        )
        M299___1_x_AGM_114K_Hellfire__Starboard = (
            1,
            Weapons.M299___1_x_AGM_114K_Hellfire__Starboard,
        )
        FN_HMP400__400rnds_ = (1, Weapons.FN_HMP400__400rnds_)
        _200_Gallon_CEFS_Aux_Tank = (1, Weapons._200_Gallon_CEFS_Aux_Tank)
        _230_Gallon_Aux_Tank = (1, Weapons._230_Gallon_Aux_Tank)

    # ERRR <CLEAN>

    class Pylon2:
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            2,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            2,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE = (
            2,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL = (
            2,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM = (
            2,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM = (
            2,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M260___7_x_Laser_Guided_Rkts__70_mm_Hydra_70_M151_HE_APKWS = (
            2,
            Weapons.M260___7_x_Laser_Guided_Rkts__70_mm_Hydra_70_M151_HE_APKWS,
        )
        # ERRR {M261_MK151}
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE__M433_RC_Fuze = (
            2,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE__M433_RC_Fuze,
        )
        # ERRR {M261_MK156}
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE = (
            2,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL = (
            2,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM = (
            2,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM = (
            2,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M282_MPP = (
            2,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M282_MPP,
        )
        UH60_LWL12_M151 = (2, Weapons.UH60_LWL12_M151)
        UH60_LWL12_M156 = (2, Weapons.UH60_LWL12_M156)
        UH60_LWL12_M229 = (2, Weapons.UH60_LWL12_M229)
        UH60_LWL12_M257 = (2, Weapons.UH60_LWL12_M257)
        UH60_LWL12_M259 = (2, Weapons.UH60_LWL12_M259)
        UH60_LWL12_M274 = (2, Weapons.UH60_LWL12_M274)
        UH60_LWL12_APKWS = (2, Weapons.UH60_LWL12_APKWS)
        OH58D_FIM_92_L = (2, Weapons.OH58D_FIM_92_L)
        OH58D_AGM_114_L1 = (2, Weapons.OH58D_AGM_114_L1)
        OH58D_AGM_114_L = (2, Weapons.OH58D_AGM_114_L)
        M299___Empty_Launcher = (2, Weapons.M299___Empty_Launcher)
        M299___4_x_AGM_114K_Hellfire = (2, Weapons.M299___4_x_AGM_114K_Hellfire)
        M299___3_x_AGM_114K_Hellfire__Port = (
            2,
            Weapons.M299___3_x_AGM_114K_Hellfire__Port,
        )
        M299___3_x_AGM_114K_Hellfire__Starboard = (
            2,
            Weapons.M299___3_x_AGM_114K_Hellfire__Starboard,
        )
        M299___2_x_AGM_114K_Hellfire = (2, Weapons.M299___2_x_AGM_114K_Hellfire)
        M299___1_x_AGM_114K_Hellfire__Port = (
            2,
            Weapons.M299___1_x_AGM_114K_Hellfire__Port,
        )
        M299___1_x_AGM_114K_Hellfire__Starboard = (
            2,
            Weapons.M299___1_x_AGM_114K_Hellfire__Starboard,
        )
        FN_HMP400__400rnds_ = (2, Weapons.FN_HMP400__400rnds_)
        M_230__30MM_M789_HEDP__600_rnds_ = (2, Weapons.M_230__30MM_M789_HEDP__600_rnds_)
        GAU_19 = (2, Weapons.GAU_19)
        M134 = (2, Weapons.M134)
        _200_Gallon_CEFS_Aux_Tank = (2, Weapons._200_Gallon_CEFS_Aux_Tank)
        _230_Gallon_Aux_Tank = (2, Weapons._230_Gallon_Aux_Tank)
        _450_Gallon_Aux_Tank = (2, Weapons._450_Gallon_Aux_Tank)

    # ERRR <CLEAN>

    class Pylon3:
        Empty_Gunner_Seat = (3, Weapons.Empty_Gunner_Seat)
        M134_Door_Gun = (3, Weapons.M134_Door_Gun)

    class Pylon4:
        Cargo_Seats__Rear_Row_ = (4, Weapons.Cargo_Seats__Rear_Row_)
        Cargo_Seats__Three_Rows_ = (4, Weapons.Cargo_Seats__Three_Rows_)
        Dual_Internal_Auxiliary_Fuel_Transfer_System__336_Gallons_ = (
            4,
            Weapons.Dual_Internal_Auxiliary_Fuel_Transfer_System__336_Gallons_,
        )

    class Pylon5:
        Empty_Gunner_Seat_ = (5, Weapons.Empty_Gunner_Seat_)
        M134_Door_Gun = (5, Weapons.M134_Door_Gun)

    class Pylon6:
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            6,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            6,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE = (
            6,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL = (
            6,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM = (
            6,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM = (
            6,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M260___7_x_Laser_Guided_Rkts__70_mm_Hydra_70_M151_HE_APKWS = (
            6,
            Weapons.M260___7_x_Laser_Guided_Rkts__70_mm_Hydra_70_M151_HE_APKWS,
        )
        # ERRR {M261_MK151}
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE__M433_RC_Fuze = (
            6,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE__M433_RC_Fuze,
        )
        # ERRR {M261_MK156}
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE = (
            6,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL = (
            6,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM = (
            6,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM = (
            6,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M282_MPP = (
            6,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M282_MPP,
        )
        UH60_LWL12_M151 = (6, Weapons.UH60_LWL12_M151)
        UH60_LWL12_M156 = (6, Weapons.UH60_LWL12_M156)
        UH60_LWL12_M229 = (6, Weapons.UH60_LWL12_M229)
        UH60_LWL12_M257 = (6, Weapons.UH60_LWL12_M257)
        UH60_LWL12_M259 = (6, Weapons.UH60_LWL12_M259)
        UH60_LWL12_M274 = (6, Weapons.UH60_LWL12_M274)
        UH60_LWL12_APKWS = (6, Weapons.UH60_LWL12_APKWS)
        FN_HMP400__400rnds_ = (6, Weapons.FN_HMP400__400rnds_)
        M_230__30MM_M789_HEDP__600_rnds__ = (
            6,
            Weapons.M_230__30MM_M789_HEDP__600_rnds__,
        )
        GAU_19_ = (6, Weapons.GAU_19_)
        M134_ = (6, Weapons.M134_)
        OH58D_FIM_92_R = (6, Weapons.OH58D_FIM_92_R)
        OH58D_AGM_114_R1 = (6, Weapons.OH58D_AGM_114_R1)
        OH58D_AGM_114_R = (6, Weapons.OH58D_AGM_114_R)
        M299___Empty_Launcher = (6, Weapons.M299___Empty_Launcher)
        M299___4_x_AGM_114K_Hellfire = (6, Weapons.M299___4_x_AGM_114K_Hellfire)
        M299___3_x_AGM_114K_Hellfire__Port = (
            6,
            Weapons.M299___3_x_AGM_114K_Hellfire__Port,
        )
        M299___3_x_AGM_114K_Hellfire__Starboard = (
            6,
            Weapons.M299___3_x_AGM_114K_Hellfire__Starboard,
        )
        M299___2_x_AGM_114K_Hellfire = (6, Weapons.M299___2_x_AGM_114K_Hellfire)
        M299___1_x_AGM_114K_Hellfire__Port = (
            6,
            Weapons.M299___1_x_AGM_114K_Hellfire__Port,
        )
        M299___1_x_AGM_114K_Hellfire__Starboard = (
            6,
            Weapons.M299___1_x_AGM_114K_Hellfire__Starboard,
        )
        _200_Gallon_CEFS_Aux_Tank = (6, Weapons._200_Gallon_CEFS_Aux_Tank)
        _230_Gallon_Aux_Tank = (6, Weapons._230_Gallon_Aux_Tank)
        _450_Gallon_Aux_Tank = (6, Weapons._450_Gallon_Aux_Tank)

    # ERRR <CLEAN>

    class Pylon7:
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE = (
            7,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM = (
            7,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M156_SM,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE = (
            7,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL = (
            7,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM = (
            7,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM,
        )
        M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM = (
            7,
            Weapons.M260___7_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M260___7_x_Laser_Guided_Rkts__70_mm_Hydra_70_M151_HE_APKWS = (
            7,
            Weapons.M260___7_x_Laser_Guided_Rkts__70_mm_Hydra_70_M151_HE_APKWS,
        )
        # ERRR {M261_MK151}
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE__M433_RC_Fuze = (
            7,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M151_HE__M433_RC_Fuze,
        )
        # ERRR {M261_MK156}
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE = (
            7,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M229_HE,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL = (
            7,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M257_IL,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM = (
            7,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M259_SM,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM = (
            7,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M274_TP_SM,
        )
        M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M282_MPP = (
            7,
            Weapons.M261___19_x_UnGd_Rkts__70_mm_Hydra_70_M282_MPP,
        )
        UH60_LWL12_M151 = (7, Weapons.UH60_LWL12_M151)
        UH60_LWL12_M156 = (7, Weapons.UH60_LWL12_M156)
        UH60_LWL12_M229 = (7, Weapons.UH60_LWL12_M229)
        UH60_LWL12_M257 = (7, Weapons.UH60_LWL12_M257)
        UH60_LWL12_M259 = (7, Weapons.UH60_LWL12_M259)
        UH60_LWL12_M274 = (7, Weapons.UH60_LWL12_M274)
        UH60_LWL12_APKWS = (7, Weapons.UH60_LWL12_APKWS)
        OH58D_FIM_92_R = (7, Weapons.OH58D_FIM_92_R)
        OH58D_AGM_114_R1 = (7, Weapons.OH58D_AGM_114_R1)
        OH58D_AGM_114_R = (7, Weapons.OH58D_AGM_114_R)
        M299___Empty_Launcher = (7, Weapons.M299___Empty_Launcher)
        M299___4_x_AGM_114K_Hellfire = (7, Weapons.M299___4_x_AGM_114K_Hellfire)
        M299___3_x_AGM_114K_Hellfire__Port = (
            7,
            Weapons.M299___3_x_AGM_114K_Hellfire__Port,
        )
        M299___3_x_AGM_114K_Hellfire__Starboard = (
            7,
            Weapons.M299___3_x_AGM_114K_Hellfire__Starboard,
        )
        M299___2_x_AGM_114K_Hellfire = (7, Weapons.M299___2_x_AGM_114K_Hellfire)
        M299___1_x_AGM_114K_Hellfire__Port = (
            7,
            Weapons.M299___1_x_AGM_114K_Hellfire__Port,
        )
        M299___1_x_AGM_114K_Hellfire__Starboard = (
            7,
            Weapons.M299___1_x_AGM_114K_Hellfire__Starboard,
        )
        FN_HMP400__400rnds_ = (7, Weapons.FN_HMP400__400rnds_)
        _200_Gallon_CEFS_Aux_Tank = (7, Weapons._200_Gallon_CEFS_Aux_Tank)
        _230_Gallon_Aux_Tank = (7, Weapons._230_Gallon_Aux_Tank)

    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7}

    tasks = [
        task.CAP,
        task.CAS,
        task.GroundAttack,
        task.Escort,
        task.Transport,
        task.AntishipStrike,
    ]
    task_default = task.CAS


@helicoptermod
class UH_60L(HelicopterType):
    id = "UH-60L"
    flyable = True
    height = 5.13
    width = 16.4
    length = 19.76
    fuel_max = 1362
    max_speed = 355.584
    chaff = 30
    flare = 60
    charge_total = 90
    chaff_charge_size = 1
    flare_charge_size = 1
    radio_frequency = 116

    panel_radio = {
        2: {
            "channels": {
                1: 264,
                2: 265,
                4: 254,
                8: 258,
                16: 267,
                17: 251,
                9: 262,
                18: 253,
                5: 250,
                10: 259,
                20: 252,
                11: 268,
                3: 256,
                6: 270,
                12: 269,
                13: 260,
                7: 257,
                14: 263,
                19: 266,
                15: 261,
            },
        },
        3: {
            "channels": {
                1: 138,
                2: 121.5,
                4: 127.5,
                8: 135,
                16: 118.45,
                17: 134,
                9: 136,
                18: 134.5,
                5: 130,
                10: 139,
                20: 137.5,
                11: 151,
                3: 127,
                6: 133,
                12: 118.5,
                13: 118.1,
                7: 133.5,
                14: 118.9,
                19: 137,
                15: 118.4,
            },
        },
        1: {
            "channels": {6: 41, 2: 31, 8: 50, 3: 32, 1: 30, 4: 33, 5: 40, 7: 42},
        },
        4: {
            "channels": {6: 41, 2: 31, 8: 50, 3: 32, 1: 30, 4: 33, 5: 40, 7: 42},
        },
        5: {
            "channels": {1: 3, 2: 10},
        },
    }

    callnames: Dict[str, List[str]] = {
        "USA": [
            "Jolly",
            "Pedro",
        ]
    }

    property_defaults: Dict[str, Any] = {
        "FuelProbeEnabled": False,
        "NetCrewControlPriority": 1,
    }

    class Properties:

        class FuelProbeEnabled:
            id = "FuelProbeEnabled"

        class NetCrewControlPriority:
            id = "NetCrewControlPriority"

            class Values:
                Pilot = 0
                Instructor = 1
                Ask_Always = -1
                Equally_Responsible = -2

    properties = {
        "FuelProbeEnabled": UnitPropertyDescription(
            identifier="FuelProbeEnabled",
            control="checkbox",
            label="Enable Fuel Probe",
            default=False,
            weight_when_on=0,
        ),
        "NetCrewControlPriority": UnitPropertyDescription(
            identifier="NetCrewControlPriority",
            control="comboList",
            label="Aircraft Control Priority",
            player_only=True,
            default=1,
            w_ctrl=150,
            values={
                0: "Pilot",
                1: "Instructor",
                -1: "Ask Always",
                -2: "Equally Responsible",
            },
        ),
    }

    livery_name = "UH-60L"  # from type

    class Pylon1:
        _200_Gallon_CEFS_Aux_Tank = (1, Weapons._200_Gallon_CEFS_Aux_Tank)
        _230_Gallon_Aux_Tank = (1, Weapons._230_Gallon_Aux_Tank)

    # ERRR <CLEAN>

    class Pylon2:
        _200_Gallon_CEFS_Aux_Tank = (2, Weapons._200_Gallon_CEFS_Aux_Tank)
        _230_Gallon_Aux_Tank = (2, Weapons._230_Gallon_Aux_Tank)
        _450_Gallon_Aux_Tank = (2, Weapons._450_Gallon_Aux_Tank)

    # ERRR <CLEAN>

    class Pylon3:
        Empty_Gunner_Seat = (3, Weapons.Empty_Gunner_Seat)
        M3M_Door_Gun = (3, Weapons.M3M_Door_Gun)
        M60_Door_Gun = (3, Weapons.M60_Door_Gun)

    class Pylon4:
        Cargo_Seats__Rear_Row_ = (4, Weapons.Cargo_Seats__Rear_Row_)
        Cargo_Seats__Three_Rows_ = (4, Weapons.Cargo_Seats__Three_Rows_)
        Dual_Internal_Auxiliary_Fuel_Transfer_System__336_Gallons_ = (
            4,
            Weapons.Dual_Internal_Auxiliary_Fuel_Transfer_System__336_Gallons_,
        )

    class Pylon5:
        Empty_Gunner_Seat_ = (5, Weapons.Empty_Gunner_Seat_)
        M3M_Door_Gun = (5, Weapons.M3M_Door_Gun)
        M60_Door_Gun = (5, Weapons.M60_Door_Gun)

    class Pylon6:
        _200_Gallon_CEFS_Aux_Tank = (6, Weapons._200_Gallon_CEFS_Aux_Tank)
        _230_Gallon_Aux_Tank = (6, Weapons._230_Gallon_Aux_Tank)
        _450_Gallon_Aux_Tank = (6, Weapons._450_Gallon_Aux_Tank)

    # ERRR <CLEAN>

    class Pylon7:
        _200_Gallon_CEFS_Aux_Tank = (7, Weapons._200_Gallon_CEFS_Aux_Tank)
        _230_Gallon_Aux_Tank = (7, Weapons._230_Gallon_Aux_Tank)

    # ERRR <CLEAN>

    pylons: Set[int] = {1, 2, 3, 4, 5, 6, 7}

    tasks = [task.Transport, task.Reconnaissance]
    task_default = task.Transport


@planemod
class KC130J(PlaneType):
    id = "KC130J"
    group_size_max = 1
    height = 11.66
    width = 40.4
    length = 29.79
    fuel_max = 30000
    max_speed = 222.23988
    chaff = 120
    flare = 60
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    tacan = True
    category = "Tankers"  # {8A302789-A55D-4897-B647-66493FA6826F}

    livery_name = "KC130J"  # from type

    pylons: Set[int] = set()

    tasks = [task.Refueling]
    task_default = task.Refueling
