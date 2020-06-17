from dcs.planes import *
from dcs.vehicles import *

from game.data.building_data import WW2_GERMANY_BUILDINGS
from game.data.doctrine import WWII_DOCTRINE

Germany_1944 = {
    "country": "Third Reich",
    "side": "red",
    "units": [

        FW_190A8,
        FW_190D9,
        Bf_109K_4,
        Ju_88A4,

        Armor.MT_Pz_Kpfw_V_Panther_Ausf_G,
        Armor.MT_Pz_Kpfw_IV_Ausf_H,
        Armor.HT_Pz_Kpfw_VI_Tiger_I,
        Armor.HT_Pz_Kpfw_VI_Ausf__B__Tiger_II,
        Armor.APC_Sd_Kfz_251,
        Armor.IFV_Sd_Kfz_234_2_Puma,
        Armor.Sd_Kfz_184_Elefant,
        Armor.TD_Jagdpanther_G1,
        Armor.TD_Jagdpanzer_IV,

        Artillery.Sturmpanzer_IV_Brummbär,

        Unarmed.Sd_Kfz_2,
        Unarmed.Sd_Kfz_7,
        Unarmed.Kübelwagen_82,

        Infantry.Infantry_Mauser_98,
        AirDefence.AAA_8_8cm_Flak_36,
    ],
    "shorad": [
        AirDefence.AAA_8_8cm_Flak_36,
    ],
    "objects": WW2_GERMANY_BUILDINGS,
    "doctrine": WWII_DOCTRINE,
    "boat": ["UBoatGroupGenerator", "SchnellbootGroupGenerator"],
    "boat_count": 4,
    "missiles": ["V1GroupGenerator"],
    "missiles_count": 1
}