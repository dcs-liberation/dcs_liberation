from dcs.helicopters import *
from dcs.planes import *
from dcs.ships import *
from dcs.vehicles import *

Japan_2005 = {
    "country": "Japan",
    "side": "blue",
    "units": [
        F_15C,     # F-15J/DJ
        F_16C_50,  # F-2A/B
        F_4E,      # F-4EJ

        KC_135,
        KC130,
        C_130,
        E_3A,

        AH_1W,
        AH_64D,

        Armor.MBT_Merkava_Mk__4,  # Standing as Type 10 MBT
        Armor.MBT_M1A2_Abrams,    # Standing as Type 90 MBT
        Armor.IFV_Marder,         # Standing as Type 89 IFV
        Armor.TPz_Fuchs,          # Standing as Type 96 APC
        Armor.IFV_LAV_25,         # Standing as Type 16 or Type 87
        Armor.APC_M1043_HMMWV_Armament,

        Artillery.MLRS_M270,
        Artillery.SPH_M109_Paladin,  # Standing as Type 99 SPH

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.SAM_Hawk_PCP,
        AirDefence.SAM_Patriot_EPP_III,

        LHA_1_Tarawa,
    ], "shorad": [
        AirDefence.SPAAA_Gepard,  # Type 87 SPAG
    ], "helicopter_carrier": [
        LHA_1_Tarawa, # Standing as Hyuga-class helicopter carrier
    ], "destroyer": [
        USS_Arleigh_Burke_IIa,
    ], "cruiser": [
        Ticonderoga_class,
    ], "lhanames": [
        "Hyuga",
        "Ise",
    ], "boat":[
        "ArleighBurkeGroupGenerator"
    ], "has_jtac": True
}
