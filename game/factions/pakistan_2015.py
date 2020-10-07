from dcs.helicopters import (
    AH_1W,
    UH_1H,
)
from dcs.planes import (
    E_3A,
    F_16C_50,
    IL_78M,
    JF_17,
    MiG_19P,
    MiG_21Bis,
    WingLoong_I,
)
from dcs.ships import (
    Armed_speedboat,
)
from dcs.vehicles import (
    AirDefence,
    Armor,
    Infantry,
    Unarmed,
)

Pakistan_2015 = {
    "country": "Pakistan",
    "side": "blue",
    "units": [
        JF_17,
        F_16C_50,
        MiG_21Bis, # Standing as J-7
        MiG_19P, # Standing as J-6
        IL_78M,
        E_3A,

        UH_1H,
        AH_1W,

        Armor.MBT_T_80U,
        Armor.MBT_T_55, # Standing as Al-Zarrar / Type 59 MBT
        Armor.ZBD_04A,
        Armor.APC_BTR_80,
        Armor.APC_M113,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,

        AirDefence.SAM_SA_2_LN_SM_90,          # Standing as HQ-2
        AirDefence.SAM_SA_10_S_300PS_LN_5P85C, # Standing as HQ-9

        Armed_speedboat,
    ], "shorad": [
        AirDefence.HQ_7_Self_Propelled_LN,
        AirDefence.AAA_ZU_23_Insurgent_on_Ural_375,
        AirDefence.AAA_ZU_23_Closed
    ], "boat": [
        "Type54GroupGenerator", "OliverHazardPerryGroupGenerator"
    ],
    "has_jtac": True,
    "jtac_unit": WingLoong_I
}
