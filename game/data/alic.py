from dcs.vehicles import AirDefence

from game.theater.theatergroup import TheaterUnit


class AlicCodes:
    CODES = {
        AirDefence.X_1L13_EWR.id: 101,
        AirDefence.X_55G6_EWR.id: 102,
        AirDefence.S_300PS_40B6MD_sr.id: 103,
        AirDefence.S_300PS_64H6E_sr.id: 104,
        AirDefence.SA_11_Buk_SR_9S18M1.id: 107,
        AirDefence.Kub_1S91_str.id: 108,
        AirDefence.Dog_Ear_radar.id: 109,
        AirDefence.S_300PS_40B6M_tr.id: 110,
        AirDefence.SA_11_Buk_LN_9A310M1.id: 115,
        AirDefence.Osa_9A33_ln.id: 117,
        AirDefence.Strela_10M3.id: 118,
        AirDefence.Tor_9A331.id: 119,
        AirDefence.X_2S6_Tunguska.id: 120,
        AirDefence.ZSU_23_4_Shilka.id: 121,
        AirDefence.P_19_s_125_sr.id: 122,
        AirDefence.Snr_s_125_tr.id: 123,
        AirDefence.Rapier_fsa_blindfire_radar.id: 124,
        AirDefence.Rapier_fsa_launcher.id: 125,
        AirDefence.SNR_75V.id: 126,
        AirDefence.HQ_7_LN_SP.id: 127,
        AirDefence.HQ_7_STR_SP.id: 128,
        AirDefence.RLS_19J6.id: 130,
        AirDefence.Roland_ADS.id: 201,
        AirDefence.Patriot_str.id: 202,
        AirDefence.Hawk_sr.id: 203,
        AirDefence.Hawk_tr.id: 204,
        AirDefence.Roland_Radar.id: 205,
        AirDefence.Hawk_cwar.id: 206,
        AirDefence.Gepard.id: 207,
        AirDefence.Vulcan.id: 208,
        AirDefence.NASAMS_Radar_MPQ64F1.id: 209,
    }

    @classmethod
    def code_for(cls, unit: TheaterUnit) -> int:
        return cls.CODES[unit.type.id]
