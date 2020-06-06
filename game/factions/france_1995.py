from dcs.vehicles import *
from dcs.ships import *
from dcs.planes import *
from dcs.helicopters import *

France_1995 = {
    "country": "France",
    "side": "blue",
    "units": [
        M_2000C,
        Mirage_2000_5,

        KC_135,
        KC130,
        C_130,
        E_3A,

        SA342M,
        SA342L,

        Armor.MBT_Leclerc,
        Armor.TPz_Fuchs,  # Standing as VAB
        Armor.APC_Cobra,  # Standing as VBL
        Armor.ATGM_M1134_Stryker,  # Standing as VAB Mephisto
        Artillery.SPH_M109_Paladin,  # Standing as AMX30 AuF1
        Artillery.MLRS_M270,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.SAM_Roland_ADS,
        AirDefence.SAM_Hawk_PCP,
        AirDefence.HQ_7_Self_Propelled_LN,  # Standing as Crotale

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,

    ], "shorad": [
        AirDefence.HQ_7_Self_Propelled_LN,
        AirDefence.SAM_Roland_ADS
    ]
}