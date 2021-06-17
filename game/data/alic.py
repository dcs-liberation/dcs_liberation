from dcs.unit import Unit
from dcs.vehicles import AirDefence


class AlicCodes:
    CODES = {
        AirDefence.EWR_1L13.id: 101,
        AirDefence.EWR_55G6.id: 102,
        AirDefence.S_300PS_40B6MD_sr.id: 103,
        AirDefence.S_300PS_64H6E_sr.id: 104,
        AirDefence.SAM_SA_11_Buk_Gadfly_Snow_Drift_SR.id: 107,
        AirDefence.Kub_1S91_str.id: 108,
        AirDefence.MCC_SR_Sborka_Dog_Ear_SR.id: 109,
        AirDefence.S_300PS_40B6M_tr.id: 110,
        AirDefence.SA_11_Buk_LN_9A310M1.id: 115,
        AirDefence.Osa_9A33_ln.id: 117,
        AirDefence.Strela_10M3.id: 118,
        AirDefence.Tor_9A331.id: 119,
        AirDefence._2S6_Tunguska.id: 120,
        AirDefence.ZSU_23_4_Shilka.id: 121,
        AirDefence.P_19_s_125_sr.id: 122,
        AirDefence.Snr_s_125_tr.id: 123,
        AirDefence.SAM_Rapier_Blindfire_TR.id: 124,
        AirDefence.Rapier_fsa_launcher.id: 125,
        AirDefence.SAM_SA_2_S_75_Fan_Song_TR.id: 126,
        AirDefence.HQ_7_LN_SP.id: 127,
        AirDefence.HQ_7_Self_Propelled_STR.id: 128,
        AirDefence.Roland_ADS.id: 201,
        AirDefence.Patriot_str.id: 202,
        AirDefence.Hawk_sr.id: 203,
        AirDefence.Hawk_tr.id: 204,
        AirDefence.SAM_Roland_EWR.id: 205,
        AirDefence.SAM_Hawk_CWAR_AN_MPQ_55.id: 206,
        AirDefence.Gepard.id: 207,
        AirDefence.Vulcan.id: 208,
    }

    @classmethod
    def code_for(cls, unit: Unit) -> int:
        return cls.CODES[unit.type]
