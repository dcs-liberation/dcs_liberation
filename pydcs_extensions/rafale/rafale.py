from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

class RafaleWeapons:
    SCALP = {"clsid": "{SCALP}", "name": "SCALP", "weight": None}
    AS_30L = {"clsid": "{AS_30L}", "name": "AS_30L", "weight": 292}
    Exocet = {"clsid": "{Exocet}", "name": "Exocet", "weight": 640}
    Thales_RBE2 = {"clsid": "{Thales_RBE2}", "name": "Thales_RBE2", "weight": 1.4789}
    Thales_RBE2_ = {"clsid": "{Thales_RBE2}", "name": "Thales_RBE2", "weight": 1.4789}
    DAMOCLES = {"clsid": "{DAMOCLES}", "name": "DAMOCLES", "weight": 265}
    DAMOCLES_ = {"clsid": "{DAMOCLES}", "name": "DAMOCLES", "weight": 265}
    DAMOCLES__ = {"clsid": "{DAMOCLES}", "name": "DAMOCLES", "weight": 265}
    _2300_PTB_RAF = {"clsid": "{2300-PTB RAF}", "name": "2300-PTB RAF", "weight": 70}
    _2300_PTB_RAF_ = {"clsid": "{2300-PTB RAF}", "name": "2300-PTB RAF", "weight": 70}
    PTB_1500 = {"clsid": "{PTB-1500}", "name": "PTB-1500", "weight": 70}
    RPL_711 = {"clsid": "{RPL 711}", "name": "RPL 711", "weight": 70}
    RPL_711_ = {"clsid": "{RPL 711}", "name": "RPL 711", "weight": 70}
    RPL_711__ = {"clsid": "{RPL 711}", "name": "RPL 711", "weight": 70}
    RPL_711___ = {"clsid": "{PTB-1500}", "name": "RPL 711", "weight": 50}
    RPL_751 = {"clsid": "{RPL-751}", "name": "RPL-751", "weight": 50}
    RPL751 = {"clsid": "{RPL751}", "name": "RPL751", "weight": 70}
    RPL751_ = {"clsid": "{RPL751}", "name": "RPL751", "weight": 70}
    RPL751__ = {"clsid": "{RPL751}", "name": "RPL751", "weight": 70}
    METEOR = {"clsid": "{RAFALE_MBDA_METEOR}", "name": "METEOR", "weight": 199}
    METEOR_x2 = {"clsid": "{LAU-115_2xLAU-127_MBDA_METEOR}", "name": "METEOR x2", "weight": 445}
    GBU_49 = {"clsid": "{GBU_49}", "name": "GBU_49", "weight": 525}
    GBU12PII = {"clsid": "{GBU12PII}", "name": "GBU12PII", "weight": 525}
    AASM_250 = {"clsid": "{AASM_250}", "name": "AASM_250", "weight": 250}
    AASM_250_L = {"clsid": "{AASM_250_L}", "name": "AASM_250_L", "weight": 500}
    AASM_250_R = {"clsid": "{AASM_250_R}", "name": "AASM_250_R", "weight": 500}
    AASM_250_RIGHT = {"clsid": "{AASM_250_RIGHT}", "name": "AASM_250_RIGHT", "weight": 250}
    _2_GBU_54_V_1_B = {"clsid": "{BRU-70A_2*GBU-54_LEFT}", "name": "2 GBU-54(V)1/B", "weight": 566}
    _2_GBU_54_V_1_B_ = {"clsid": "{BRU-70A_2*GBU-54_RIGHT}", "name": "2 GBU-54(V)1/B", "weight": 566}
    _3_GBU_54_V_1_B = {"clsid": "{BRU-70A_3*GBU-54}", "name": "3 GBU-54(V)1/B", "weight": 819}


class Rafale_A_S(PlaneType):
    id = "Rafale_A_S"
    flyable = True
    height = 5.28
    width = 10.13
    length = 15.96
    fuel_max = 5000
    max_speed = 2001.996
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  #{78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Liveries:

        class USSR(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Georgia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Venezuela(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Australia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Israel(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Combined_Joint_Task_Forces_Blue(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Sudan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Norway(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Romania(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Iran(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Ukraine(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Libya(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Belgium(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Slovakia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Greece(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class UK(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Third_Reich(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Hungary(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Abkhazia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Morocco(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class United_Nations_Peacekeepers(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Switzerland(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class SouthOssetia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Vietnam(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class China(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Yemen(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Kuwait(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Serbia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Oman(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class India(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Egypt(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class TheNetherlands(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Poland(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Syria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Finland(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Kazakhstan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Denmark(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Sweden(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Croatia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class CzechRepublic(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class GDR(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Yugoslavia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Bulgaria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class SouthKorea(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Tunisia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Combined_Joint_Task_Forces_Red(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Lebanon(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Portugal(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Cuba(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Insurgents(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class SaudiArabia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class France(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class USA(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Honduras(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Qatar(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Russia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class United_Arab_Emirates(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Italian_Social_Republi(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Austria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Bahrain(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Italy(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Chile(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Turkey(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Philippines(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Algeria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Pakistan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Malaysia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Indonesia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Iraq(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Germany(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class South_Africa(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Jordan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Mexico(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class USAFAggressors(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Brazil(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Spain(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Belarus(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Canada(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class NorthKorea(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Ethiopia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Japan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Thailand(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

    class Pylon1:
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        R_550_Magic_2 = (1, Weapons.R_550_Magic_2)

    class Pylon2:
        AASM_250_L = (2, RafaleWeapons.AASM_250_L)
        GBU_49 = (2, RafaleWeapons.GBU_49)
        MER_2_MK_82 = (2, Weapons.MER_2_MK_82)
        _3_Mk_82 = (2, Weapons._3_Mk_82)
        GBU12PII = (2, RafaleWeapons.GBU12PII)
        Mk_20 = (2, Weapons.Mk_20)
        _3_Mk_20_Rockeye = (2, Weapons._3_Mk_20_Rockeye)
        Mk_84 = (2, Weapons.Mk_84)
        GBU_24 = (2, Weapons.GBU_24)
        LAU_131___7_2_75__rockets_M151__HE_ = (2, Weapons.LAU_131___7_2_75__rockets_M151__HE_)
        LAU3_HE151 = (2, Weapons.LAU3_HE151)
        LAU3_WP156 = (2, Weapons.LAU3_WP156)
        LAU3_HE5 = (2, Weapons.LAU3_HE5)
        SCALP = (2, RafaleWeapons.SCALP)
        AS_30L = (2, RafaleWeapons.AS_30L)
        AGM_88C_ = (2, Weapons.AGM_88C_)

    class Pylon3:
        GBU_49 = (3, RafaleWeapons.GBU_49)
        GBU_24 = (3, Weapons.GBU_24)
        GBU12PII = (3, RafaleWeapons.GBU12PII)
        MER_2_MK_82 = (3, Weapons.MER_2_MK_82)
        _3_Mk_82 = (3, Weapons._3_Mk_82)
        AGM_88C_ = (3, Weapons.AGM_88C_)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU_131x3_HYDRA_70_M151 = (3, Weapons.LAU_131x3_HYDRA_70_M151)
        AS_30L = (3, RafaleWeapons.AS_30L)
        RPL_711__ = (3, RafaleWeapons.RPL_711__)
        RPL751__ = (3, RafaleWeapons.RPL751__)

    class Pylon4:
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (4, Weapons.AIM_9P_Sidewinder_IR_AAM)
        MICA_IR = (4, Weapons.MICA_IR)
        LAU_10___4_ZUNI_MK_71 = (4, Weapons.LAU_10___4_ZUNI_MK_71)
        LAU_61___19_2_75__rockets_MK151_HE = (4, Weapons.LAU_61___19_2_75__rockets_MK151_HE)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)

    class Pylon5:
        GBU12PII = (5, RafaleWeapons.GBU12PII)
        RPL_711__ = (5, RafaleWeapons.RPL_711__)
        RPL751__ = (5, RafaleWeapons.RPL751__)
        Mercury_LLTV_Pod = (5, Weapons.Mercury_LLTV_Pod)
        SCALP = (5, RafaleWeapons.SCALP)
        Exocet = (5, RafaleWeapons.Exocet)
        GBU_49 = (5, RafaleWeapons.GBU_49)

    class Pylon6:
        LAU_10___4_ZUNI_MK_71 = (6, Weapons.LAU_10___4_ZUNI_MK_71)
        LAU_61___19_2_75__rockets_MK151_HE = (6, Weapons.LAU_61___19_2_75__rockets_MK151_HE)
        AIM_9M_Sidewinder_IR_AAM = (6, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (6, Weapons.AIM_9P_Sidewinder_IR_AAM)
        MICA_IR = (6, Weapons.MICA_IR)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)

    class Pylon7:
        AN_AAQ_28_LITENING = (7, Weapons.AN_AAQ_28_LITENING)
        DAMOCLES__ = (7, RafaleWeapons.DAMOCLES__)
        Thales_RBE2_ = (7, RafaleWeapons.Thales_RBE2_)

    class Pylon8:
        GBU_49 = (8, RafaleWeapons.GBU_49)
        GBU_24 = (8, Weapons.GBU_24)
        GBU12PII = (8, RafaleWeapons.GBU12PII)
        MER_2_MK_82 = (8, Weapons.MER_2_MK_82)
        _3_Mk_20_Rockeye = (8, Weapons._3_Mk_20_Rockeye)
        _3_Mk_82 = (8, Weapons._3_Mk_82)
        LAU3_HE151 = (8, Weapons.LAU3_HE151)
        LAU3_WP156 = (8, Weapons.LAU3_WP156)
        LAU_131x3_HYDRA_70_M151 = (8, Weapons.LAU_131x3_HYDRA_70_M151)
        AS_30L = (8, RafaleWeapons.AS_30L)
        AGM_88C_ = (8, Weapons.AGM_88C_)
        RPL_711__ = (8, RafaleWeapons.RPL_711__)
        RPL751__ = (8, RafaleWeapons.RPL751__)

    class Pylon9:
        AASM_250_R = (9, RafaleWeapons.AASM_250_R)
        GBU_49 = (9, RafaleWeapons.GBU_49)
        GBU_24 = (9, Weapons.GBU_24)
        MER_2_MK_82 = (9, Weapons.MER_2_MK_82)
        GBU12PII = (9, RafaleWeapons.GBU12PII)
        _3_Mk_20_Rockeye = (9, Weapons._3_Mk_20_Rockeye)
        Mk_84 = (9, Weapons.Mk_84)
        _3_Mk_82 = (9, Weapons._3_Mk_82)
        AGM_88C_ = (9, Weapons.AGM_88C_)
        LAU_131___7_2_75__rockets_M151__HE_ = (9, Weapons.LAU_131___7_2_75__rockets_M151__HE_)
        LAU3_HE151 = (9, Weapons.LAU3_HE151)
        LAU3_WP156 = (9, Weapons.LAU3_WP156)
        LAU3_HE5 = (9, Weapons.LAU3_HE5)
        SCALP = (9, RafaleWeapons.SCALP)
        AS_30L = (9, RafaleWeapons.AS_30L)

    class Pylon10:
        R_550_Magic_2 = (10, Weapons.R_550_Magic_2)
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (10, Weapons.Smokewinder___orange)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [task.CAP, task.Escort, task.FighterSweep, task.GroundAttack, task.CAS, task.AFAC, task.RunwayAttack, task.AntishipStrike, task.SEAD, task.PinpointStrike]
    task_default = task.CAP


class Rafale_M(PlaneType):
    id = "Rafale_M"
    flyable = True
    height = 5.28
    width = 10.13
    length = 15.96
    fuel_max = 5000
    max_speed = 2001.996
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  #{78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Liveries:

        class USSR(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Georgia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Venezuela(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Australia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Israel(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Combined_Joint_Task_Forces_Blue(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Sudan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Norway(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Romania(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Iran(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Ukraine(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Libya(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Belgium(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Slovakia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Greece(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class UK(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Third_Reich(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Hungary(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Abkhazia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Morocco(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class United_Nations_Peacekeepers(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Switzerland(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class SouthOssetia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Vietnam(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class China(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Yemen(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Kuwait(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Serbia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Oman(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class India(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Egypt(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class TheNetherlands(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Poland(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Syria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Finland(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Kazakhstan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Denmark(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Sweden(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Croatia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class CzechRepublic(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class GDR(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Yugoslavia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Bulgaria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class SouthKorea(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Tunisia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Combined_Joint_Task_Forces_Red(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Lebanon(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Portugal(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Cuba(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Insurgents(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class SaudiArabia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class France(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class USA(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Honduras(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Qatar(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Russia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class United_Arab_Emirates(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Italian_Social_Republi(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Austria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Bahrain(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Italy(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Chile(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Turkey(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Philippines(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Algeria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Pakistan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Malaysia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Indonesia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Iraq(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Germany(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class South_Africa(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Jordan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Mexico(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class USAFAggressors(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Brazil(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Spain(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Belarus(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Canada(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class NorthKorea(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Ethiopia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Japan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

        class Thailand(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"
            _04_11f_tiger_meet = "04 11f tiger meet"
            _05_brazil = "05 brazil"
            _07_marine_tiger_2014 = "07 marine tiger 2014"
            _08_flottile_12_f_90_ans = "08 flottile 12-f.90 ans"
            _09_marine_mat_17f = "09 marine mat 17f"

    class Pylon1:
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        R_550_Magic_2 = (1, Weapons.R_550_Magic_2)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)

    class Pylon2:
        Mk_84 = (2, Weapons.Mk_84)
        MER_2_MK_83 = (2, Weapons.MER_2_MK_83)
        MER_2_MK_82 = (2, Weapons.MER_2_MK_82)
        _3_Mk_82 = (2, Weapons._3_Mk_82)
        LAU_131___7_2_75__rockets_M151__HE_ = (2, Weapons.LAU_131___7_2_75__rockets_M151__HE_)
        LAU3_HE151 = (2, Weapons.LAU3_HE151)
        LAU3_WP156 = (2, Weapons.LAU3_WP156)
        LAU3_HE5 = (2, Weapons.LAU3_HE5)
        MICA_IR = (2, Weapons.MICA_IR)
        AIM_7M = (2, Weapons.AIM_7M)
        AIM_120B = (2, Weapons.AIM_120B)
        AIM_120C = (2, Weapons.AIM_120C)
        LAU_115_2_LAU_127_AIM_120C = (2, Weapons.LAU_115_2_LAU_127_AIM_120C)
        Super_530D = (2, Weapons.Super_530D)
        METEOR = (2, RafaleWeapons.METEOR)
        AASM_250 = (2, RafaleWeapons.AASM_250)

    class Pylon3:
        Mk_84 = (3, Weapons.Mk_84)
        MER_2_MK_83 = (3, Weapons.MER_2_MK_83)
        MER_2_MK_82 = (3, Weapons.MER_2_MK_82)
        _3_Mk_82 = (3, Weapons._3_Mk_82)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU_131x3_HYDRA_70_M151 = (3, Weapons.LAU_131x3_HYDRA_70_M151)
        MICA_IR = (3, Weapons.MICA_IR)
        AIM_7M = (3, Weapons.AIM_7M)
        AIM_120B = (3, Weapons.AIM_120B)
        AIM_120C = (3, Weapons.AIM_120C)
        Super_530D = (3, Weapons.Super_530D)
        RPL_711__ = (3, RafaleWeapons.RPL_711__)
        RPL751__ = (3, RafaleWeapons.RPL751__)
        METEOR = (3, RafaleWeapons.METEOR)

    class Pylon4:
        MICA_IR = (4, Weapons.MICA_IR)
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (4, Weapons.AIM_9P_Sidewinder_IR_AAM)
        LAU3_WP156 = (4, Weapons.LAU3_WP156)
        LAU_10___4_ZUNI_MK_71 = (4, Weapons.LAU_10___4_ZUNI_MK_71)
        LAU_61___19_2_75__rockets_MK151_HE = (4, Weapons.LAU_61___19_2_75__rockets_MK151_HE)
        Mk_82 = (4, Weapons.Mk_82)

    class Pylon5:
        RPL_711__ = (5, RafaleWeapons.RPL_711__)
        RPL751__ = (5, RafaleWeapons.RPL751__)
        MICA_IR = (5, Weapons.MICA_IR)
        AIM_7M = (5, Weapons.AIM_7M)
        AIM_120B = (5, Weapons.AIM_120B)
        AIM_120C = (5, Weapons.AIM_120C)
        Super_530D = (5, Weapons.Super_530D)
        METEOR = (5, RafaleWeapons.METEOR)

    class Pylon6:
        MICA_IR = (6, Weapons.MICA_IR)
        AIM_9M_Sidewinder_IR_AAM = (6, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (6, Weapons.AIM_9P_Sidewinder_IR_AAM)
        LAU3_WP156 = (6, Weapons.LAU3_WP156)
        LAU_10___4_ZUNI_MK_71 = (6, Weapons.LAU_10___4_ZUNI_MK_71)
        LAU_61___19_2_75__rockets_MK151_HE = (6, Weapons.LAU_61___19_2_75__rockets_MK151_HE)
        Mk_82 = (6, Weapons.Mk_82)

    class Pylon7:
        AN_AAQ_28_LITENING = (7, Weapons.AN_AAQ_28_LITENING)
        DAMOCLES__ = (7, RafaleWeapons.DAMOCLES__)

    class Pylon8:
        Mk_84 = (8, Weapons.Mk_84)
        MER_2_MK_83 = (8, Weapons.MER_2_MK_83)
        MER_2_MK_82 = (8, Weapons.MER_2_MK_82)
        _3_Mk_82 = (8, Weapons._3_Mk_82)
        LAU3_HE151 = (8, Weapons.LAU3_HE151)
        LAU3_WP156 = (8, Weapons.LAU3_WP156)
        LAU_131x3_HYDRA_70_M151 = (8, Weapons.LAU_131x3_HYDRA_70_M151)
        MICA_IR = (8, Weapons.MICA_IR)
        AIM_7M = (8, Weapons.AIM_7M)
        AIM_120B = (8, Weapons.AIM_120B)
        AIM_120C = (8, Weapons.AIM_120C)
        Super_530D = (8, Weapons.Super_530D)
        RPL_711__ = (8, RafaleWeapons.RPL_711__)
        RPL751__ = (8, RafaleWeapons.RPL751__)
        METEOR = (8, RafaleWeapons.METEOR)

    class Pylon9:
        METEOR = (9, RafaleWeapons.METEOR)
        Mk_84 = (9, Weapons.Mk_84)
        MER_2_MK_83 = (9, Weapons.MER_2_MK_83)
        MER_2_MK_82 = (9, Weapons.MER_2_MK_82)
        _3_Mk_82 = (9, Weapons._3_Mk_82)
        LAU_131___7_2_75__rockets_M151__HE_ = (9, Weapons.LAU_131___7_2_75__rockets_M151__HE_)
        LAU3_HE151 = (9, Weapons.LAU3_HE151)
        LAU3_WP156 = (9, Weapons.LAU3_WP156)
        LAU3_HE5 = (9, Weapons.LAU3_HE5)
        MICA_IR = (9, Weapons.MICA_IR)
        AIM_7M = (9, Weapons.AIM_7M)
        AIM_120B = (9, Weapons.AIM_120B)
        AIM_120C = (9, Weapons.AIM_120C)
        LAU_115_2_LAU_127_AIM_120C = (9, Weapons.LAU_115_2_LAU_127_AIM_120C)
        Super_530D = (9, Weapons.Super_530D)
        AASM_250_RIGHT = (9, RafaleWeapons.AASM_250_RIGHT)

    class Pylon10:
        R_550_Magic_2 = (10, Weapons.R_550_Magic_2)
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (10, Weapons.Smokewinder___orange)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [task.CAP, task.Escort, task.FighterSweep, task.GroundAttack, task.CAS, task.AFAC, task.RunwayAttack, task.AntishipStrike, task.Reconnaissance, task.Intercept]
    task_default = task.CAP


class Rafale_B(PlaneType):
    id = "Rafale_B"
    flyable = True
    height = 5.28
    width = 10.13
    length = 15.96
    fuel_max = 5000
    max_speed = 2001.996
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  #{78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Liveries:

        class USSR(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Georgia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Venezuela(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Australia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Israel(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Combined_Joint_Task_Forces_Blue(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Sudan(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Norway(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Romania(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Iran(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Ukraine(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Libya(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Belgium(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Slovakia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Greece(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class UK(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Third_Reich(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Hungary(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Abkhazia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Morocco(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class United_Nations_Peacekeepers(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Switzerland(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class SouthOssetia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Vietnam(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class China(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Yemen(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Kuwait(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Serbia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Oman(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class India(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Egypt(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class TheNetherlands(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Poland(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Syria(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Finland(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Kazakhstan(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Denmark(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Sweden(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Croatia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class CzechRepublic(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class GDR(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Yugoslavia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Bulgaria(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class SouthKorea(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Tunisia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Combined_Joint_Task_Forces_Red(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Lebanon(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Portugal(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Cuba(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Insurgents(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class SaudiArabia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class France(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class USA(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Honduras(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Qatar(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Russia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class United_Arab_Emirates(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Italian_Social_Republi(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Austria(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Bahrain(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Italy(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Chile(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Turkey(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Philippines(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Algeria(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Pakistan(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Malaysia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Indonesia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Iraq(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Germany(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class South_Africa(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Jordan(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Mexico(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class USAFAggressors(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Brazil(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Spain(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Belarus(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Canada(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class NorthKorea(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Ethiopia(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Japan(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

        class Thailand(Enum):
            _01_rafale_b_lafayette = "01 rafale b lafayette"
            _02_rafale_b_mt_de_marsan = "02 rafale b mt de marsan"
            _03_standard = "03 standard"

    class Pylon1:
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
        R_550_Magic_2 = (1, Weapons.R_550_Magic_2)

    class Pylon2:
        AASM_250_L = (2, RafaleWeapons.AASM_250_L)
        GBU_49 = (2, RafaleWeapons.GBU_49)
        MER_2_MK_82 = (2, Weapons.MER_2_MK_82)
        _3_Mk_82 = (2, Weapons._3_Mk_82)
        GBU12PII = (2, RafaleWeapons.GBU12PII)
        Mk_20 = (2, Weapons.Mk_20)
        _3_Mk_20_Rockeye = (2, Weapons._3_Mk_20_Rockeye)
        Mk_84 = (2, Weapons.Mk_84)
        GBU_24 = (2, Weapons.GBU_24)
        LAU_131___7_2_75__rockets_M151__HE_ = (2, Weapons.LAU_131___7_2_75__rockets_M151__HE_)
        LAU3_HE151 = (2, Weapons.LAU3_HE151)
        LAU3_WP156 = (2, Weapons.LAU3_WP156)
        LAU3_HE5 = (2, Weapons.LAU3_HE5)
        SCALP = (2, RafaleWeapons.SCALP)
        AS_30L = (2, RafaleWeapons.AS_30L)
        AGM_88C_ = (2, Weapons.AGM_88C_)

    class Pylon3:
        GBU_49 = (3, RafaleWeapons.GBU_49)
        GBU_24 = (3, Weapons.GBU_24)
        GBU12PII = (3, RafaleWeapons.GBU12PII)
        MER_2_MK_82 = (3, Weapons.MER_2_MK_82)
        _3_Mk_82 = (3, Weapons._3_Mk_82)
        AGM_88C_ = (3, Weapons.AGM_88C_)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU_131x3_HYDRA_70_M151 = (3, Weapons.LAU_131x3_HYDRA_70_M151)
        AS_30L = (3, RafaleWeapons.AS_30L)
        RPL_711__ = (3, RafaleWeapons.RPL_711__)
        RPL751__ = (3, RafaleWeapons.RPL751__)
        Mk_84 = (3, Weapons.Mk_84)

    class Pylon4:
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (4, Weapons.AIM_9P_Sidewinder_IR_AAM)
        MICA_IR = (4, Weapons.MICA_IR)
        LAU_10___4_ZUNI_MK_71 = (4, Weapons.LAU_10___4_ZUNI_MK_71)
        LAU_61___19_2_75__rockets_MK151_HE = (4, Weapons.LAU_61___19_2_75__rockets_MK151_HE)
        LAU3_HE151 = (4, Weapons.LAU3_HE151)

    class Pylon5:
        GBU12PII = (5, RafaleWeapons.GBU12PII)
        Mk_84 = (5, Weapons.Mk_84)
        RPL_711__ = (5, RafaleWeapons.RPL_711__)
        RPL751__ = (5, RafaleWeapons.RPL751__)
        Mercury_LLTV_Pod = (5, Weapons.Mercury_LLTV_Pod)
        SCALP = (5, RafaleWeapons.SCALP)
        Exocet = (5, RafaleWeapons.Exocet)
        GBU_49 = (5, RafaleWeapons.GBU_49)
        MER_2_MK_83 = (5, Weapons.MER_2_MK_83)
        MER_2_MK_82 = (5, Weapons.MER_2_MK_82)

    class Pylon6:
        LAU_10___4_ZUNI_MK_71 = (6, Weapons.LAU_10___4_ZUNI_MK_71)
        LAU_61___19_2_75__rockets_MK151_HE = (6, Weapons.LAU_61___19_2_75__rockets_MK151_HE)
        AIM_9M_Sidewinder_IR_AAM = (6, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (6, Weapons.AIM_9P_Sidewinder_IR_AAM)
        MICA_IR = (6, Weapons.MICA_IR)
        LAU3_HE151 = (6, Weapons.LAU3_HE151)

    class Pylon7:
        AN_AAQ_28_LITENING = (7, Weapons.AN_AAQ_28_LITENING)
        DAMOCLES__ = (7, RafaleWeapons.DAMOCLES__)
        Thales_RBE2_ = (7, RafaleWeapons.Thales_RBE2_)

    class Pylon8:
        GBU_49 = (8, RafaleWeapons.GBU_49)
        GBU_24 = (8, Weapons.GBU_24)
        GBU12PII = (8, RafaleWeapons.GBU12PII)
        MER_2_MK_82 = (8, Weapons.MER_2_MK_82)
        _3_Mk_20_Rockeye = (8, Weapons._3_Mk_20_Rockeye)
        _3_Mk_82 = (8, Weapons._3_Mk_82)
        Mk_84 = (8, Weapons.Mk_84)
        LAU3_HE151 = (8, Weapons.LAU3_HE151)
        LAU3_WP156 = (8, Weapons.LAU3_WP156)
        LAU_131x3_HYDRA_70_M151 = (8, Weapons.LAU_131x3_HYDRA_70_M151)
        AS_30L = (8, RafaleWeapons.AS_30L)
        AGM_88C_ = (8, Weapons.AGM_88C_)
        RPL_711__ = (8, RafaleWeapons.RPL_711__)
        RPL751__ = (8, RafaleWeapons.RPL751__)

    class Pylon9:
        AASM_250_R = (9, RafaleWeapons.AASM_250_R)
        GBU_49 = (9, RafaleWeapons.GBU_49)
        GBU_24 = (9, Weapons.GBU_24)
        MER_2_MK_82 = (9, Weapons.MER_2_MK_82)
        GBU12PII = (9, RafaleWeapons.GBU12PII)
        _3_Mk_20_Rockeye = (9, Weapons._3_Mk_20_Rockeye)
        Mk_84 = (9, Weapons.Mk_84)
        _3_Mk_82 = (9, Weapons._3_Mk_82)
        AGM_88C_ = (9, Weapons.AGM_88C_)
        LAU_131___7_2_75__rockets_M151__HE_ = (9, Weapons.LAU_131___7_2_75__rockets_M151__HE_)
        LAU3_HE151 = (9, Weapons.LAU3_HE151)
        LAU3_WP156 = (9, Weapons.LAU3_WP156)
        LAU3_HE5 = (9, Weapons.LAU3_HE5)
        SCALP = (9, RafaleWeapons.SCALP)
        AS_30L = (9, RafaleWeapons.AS_30L)

    class Pylon10:
        R_550_Magic_2 = (10, Weapons.R_550_Magic_2)
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (10, Weapons.Smokewinder___orange)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [task.CAP, task.Escort, task.FighterSweep, task.GroundAttack, task.CAS, task.AFAC, task.RunwayAttack, task.AntishipStrike, task.SEAD, task.PinpointStrike]
    task_default = task.GroundAttack


class Rafale_M_NOUNOU(PlaneType):
    id = "Rafale_M_NOUNOU"
    group_size_max = 1
    height = 5.28
    width = 10.13
    length = 15.96
    fuel_max = 4500
    max_speed = 2001.996
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    tacan = True
    category = "Tankers"  #{8A302789-A55D-4897-B647-66493FA6826F}
    radio_frequency = 127.5

    class Liveries:

        class USSR(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Georgia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Venezuela(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Australia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Israel(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Combined_Joint_Task_Forces_Blue(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Sudan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Norway(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Romania(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Iran(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Ukraine(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Libya(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Belgium(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Slovakia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Greece(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class UK(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Third_Reich(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Hungary(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Abkhazia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Morocco(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class United_Nations_Peacekeepers(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Switzerland(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class SouthOssetia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Vietnam(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class China(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Yemen(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Kuwait(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Serbia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Oman(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class India(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Egypt(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class TheNetherlands(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Poland(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Syria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Finland(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Kazakhstan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Denmark(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Sweden(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Croatia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class CzechRepublic(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class GDR(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Yugoslavia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Bulgaria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class SouthKorea(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Tunisia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Combined_Joint_Task_Forces_Red(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Lebanon(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Portugal(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Cuba(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Insurgents(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class SaudiArabia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class France(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class USA(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Honduras(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Qatar(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Russia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class United_Arab_Emirates(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Italian_Social_Republi(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Austria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Bahrain(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Italy(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Chile(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Turkey(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Philippines(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Algeria(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Pakistan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Malaysia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Indonesia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Iraq(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Germany(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class South_Africa(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Jordan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Mexico(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class USAFAggressors(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Brazil(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Spain(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Belarus(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Canada(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class NorthKorea(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Ethiopia(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Japan(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

        class Thailand(Enum):
            _01_marine_12_f = "01 marine 12 f"
            _02_rafale_export = "02 rafale export"
            _03_black_derive_11f = "03 black derive 11f"

    class Pylon1:
        MICA_IR = (1, Weapons.MICA_IR)
        R_550_Magic_2 = (1, Weapons.R_550_Magic_2)

    class Pylon3:
        RPL_751 = (3, RafaleWeapons.RPL_751)
        RPL_711___ = (3, RafaleWeapons.RPL_711___)

    class Pylon8:
        RPL_751 = (8, RafaleWeapons.RPL_751)
        RPL_711___ = (8, RafaleWeapons.RPL_711___)

    class Pylon10:
        MICA_IR = (10, Weapons.MICA_IR)
        R_550_Magic_2 = (10, Weapons.R_550_Magic_2)

    class Pylon11:
        Smokewinder___green = (11, Weapons.Smokewinder___green)
        Smokewinder___blue = (11, Weapons.Smokewinder___blue)
        Smokewinder___orange = (11, Weapons.Smokewinder___orange)
        Smoke_Generator___red_ = (11, Weapons.Smoke_Generator___red_)
        Smoke_Generator___blue_ = (11, Weapons.Smoke_Generator___blue_)
        Smoke_Generator___white_ = (11, Weapons.Smoke_Generator___white_)

    pylons = {1, 3, 8, 10, 11}

    tasks = [task.Refueling]
    task_default = task.Refueling

