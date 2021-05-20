from dcs.unit import Unit
from dcs.vehicles import AirDefence


class AlicCodes:
    CODES = {
        AirDefence.EWR_1L13.id: 101,
        AirDefence.EWR_55G6.id: 102,
        AirDefence.SAM_SA_10_S_300_Grumble_Clam_Shell_SR.id: 103,
        AirDefence.SAM_SA_10_S_300_Grumble_Big_Bird_SR.id: 104,
        AirDefence.SAM_SA_11_Buk_Gadfly_Snow_Drift_SR.id: 107,
        AirDefence.SAM_SA_6_Kub_Long_Track_STR.id: 108,
        AirDefence.MCC_SR_Sborka_Dog_Ear_SR.id: 109,
        AirDefence.SAM_SA_10_S_300_Grumble_Flap_Lid_TR.id: 110,
        AirDefence.SAM_SA_11_Buk_Gadfly_Fire_Dome_TEL.id: 115,
        AirDefence.SAM_SA_8_Osa_Gecko_TEL.id: 117,
        AirDefence.SAM_SA_13_Strela_10M3_Gopher_TEL.id: 118,
        AirDefence.SAM_SA_15_Tor_Gauntlet.id: 119,
        AirDefence.SAM_SA_19_Tunguska_Grison.id: 120,
        AirDefence.SPAAA_ZSU_23_4_Shilka_Gun_Dish.id: 121,
        AirDefence.SAM_P19_Flat_Face_SR__SA_2_3.id: 122,
        AirDefence.SAM_SA_3_S_125_Low_Blow_TR.id: 123,
        AirDefence.SAM_Rapier_Blindfire_TR.id: 124,
        AirDefence.SAM_Rapier_LN.id: 125,
        AirDefence.SAM_SA_2_S_75_Fan_Song_TR.id: 126,
        AirDefence.HQ_7_Self_Propelled_LN.id: 127,
        AirDefence.HQ_7_Self_Propelled_STR.id: 128,
        AirDefence.SAM_Roland_ADS.id: 201,
        AirDefence.SAM_Patriot_STR.id: 202,
        AirDefence.SAM_Hawk_SR__AN_MPQ_50.id: 203,
        AirDefence.SAM_Hawk_TR__AN_MPQ_46.id: 204,
        AirDefence.SAM_Roland_EWR.id: 205,
        AirDefence.SAM_Hawk_CWAR_AN_MPQ_55.id: 206,
        AirDefence.SPAAA_Gepard.id: 207,
        AirDefence.SPAAA_Vulcan_M163.id: 208,
    }

    @classmethod
    def code_for(cls, unit: Unit) -> int:
        return cls.CODES[unit.type]
