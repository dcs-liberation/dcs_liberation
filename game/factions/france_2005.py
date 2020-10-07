from dcs.helicopters import (
    SA342L,
    SA342M,
    SA342Mistral,
)
from dcs.planes import (
    C_130,
    E_3A,
    FA_18C_hornet,
    KC130,
    KC_135,
    M_2000C,
    Mirage_2000_5,
)
from dcs.ships import (
    Armed_speedboat,
    CVN_74_John_C__Stennis,
    LHA_1_Tarawa,
    Oliver_Hazzard_Perry_class,
    Ticonderoga_class,
)
from dcs.vehicles import (
    AirDefence,
    Armor,
    Artillery,
    Infantry,
    Unarmed,
)

France_2005 = {
    "country": "France",
    "side": "blue",
    "units":[
        M_2000C,
        Mirage_2000_5,
        FA_18C_hornet, # Standing as Rafale M

        KC_135,
        KC130,
        C_130,
        E_3A,

        SA342M,
        SA342L,
        SA342Mistral,

        Armor.MBT_Leclerc,
        Armor.TPz_Fuchs, # Standing as VAB
        Armor.APC_Cobra, # Standing as VBL
        Armor.ATGM_M1134_Stryker, # Standing as VAB Mephisto
        Artillery.SPH_M109_Paladin, # Standing as AMX30 AuF1
        Artillery.MLRS_M270,

        Unarmed.Transport_M818,
        Infantry.Infantry_M4,
        Infantry.Soldier_M249,

        AirDefence.SAM_Roland_ADS,
        AirDefence.SAM_Hawk_PCP,
        AirDefence.HQ_7_Self_Propelled_LN, # Standing as Crotale

        CVN_74_John_C__Stennis,
        LHA_1_Tarawa,
        Armed_speedboat,
        
    ], "shorad":[
        AirDefence.HQ_7_Self_Propelled_LN,
        AirDefence.SAM_Roland_ADS
    ], "aircraft_carrier": [
        CVN_74_John_C__Stennis, # Standing as CDG Aircraft Carrier
    ], "helicopter_carrier": [
        LHA_1_Tarawa, # Standing as Mistral Class
    ], "destroyer": [
        Oliver_Hazzard_Perry_class,
    ], "cruiser": [
        Ticonderoga_class,
    ], "carrier_names": [
        "PA Charles de Gaulle",
    ], "lhanames": [
        "L9013 Mistral",
        "L9014 Tonerre",
        "L9015 Dixmude"
    ], "boat":[
        "ArleighBurkeGroupGenerator", "OliverHazardPerryGroupGenerator"
    ], "has_jtac": True
}