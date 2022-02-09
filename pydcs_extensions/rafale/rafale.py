from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from pydcs_extensions.weapon_injector import inject_weapons


class RafaleWeapons:
    MICA_IR_ = {"clsid": "{IR}", "name": "MICA IR", "weight": 90}
    gbu12X3_L = {"clsid": "{gbu12X3_L}", "name": "gbu12X3_L", "weight": 525}
    gbu12X2_L = {"clsid": "{gbu12X2_L}", "name": "gbu12X2_L", "weight": 525}
    AASM_250_L = {"clsid": "{AASM_250_L}", "name": "AASM_250_L", "weight": 500}
    GBU_49 = {"clsid": "{GBU_49}", "name": "GBU_49", "weight": 525}
    GBU12PII = {"clsid": "{GBU12PII}", "name": "GBU12PII", "weight": 525}
    mk_84 = {"clsid": "{mk_84}", "name": "mk_84", "weight": 1000}
    gbu24 = {"clsid": "{gbu24}", "name": "gbu24", "weight": 1000}
    AASM_1000KG = {"clsid": "{AASM_1000KG}", "name": "AASM_1000KG", "weight": 1000}
    AASM_500 = {"clsid": "{AASM_500}", "name": "AASM_500", "weight": 500}
    AS_30L = {"clsid": "{AS_30L}", "name": "AS_30L", "weight": 292}
    SCALP = {"clsid": "{SCALP}", "name": "SCALP", "weight": None}
    RAF_RPL711 = {"clsid": "{RAF_RPL711}", "name": "RAF_RPL711", "weight": 820}
    RAF_RPL751 = {"clsid": "{RAF_RPL751}", "name": "RAF_RPL751", "weight": 1450}
    Exocet = {"clsid": "{Exocet}", "name": "Exocet", "weight": 640}
    Talios_Thales_RBE2 = {
        "clsid": "{Talios_Thales_RBE2}",
        "name": "Talios_Thales_RBE2",
        "weight": 1.4789,
    }
    gbu12X3_R = {"clsid": "{gbu12X3_R}", "name": "gbu12X3_R", "weight": 525}
    gbu12X2_R = {"clsid": "{gbu12X2_R}", "name": "gbu12X2_R", "weight": 525}
    METEOR = {"clsid": "{RAFALE_MBDA_METEOR}", "name": "METEOR", "weight": 199}
    AASMx3L = {"clsid": "{AASMx3L}", "name": "AASMx3L", "weight": 250}
    AASMx3R = {"clsid": "{AASMx3R}", "name": "AASMx3R", "weight": 250}
    MICA_NG = {"clsid": "{RAFALE_MICA_NG}", "name": "MICA_NG", "weight": 199}
    AASM_250_RIGHT = {
        "clsid": "{AASM_250_RIGHT}",
        "name": "AASM_250_RIGHT",
        "weight": 250,
    }
    AASM_250_R = {"clsid": "{AASM_250_R}", "name": "AASM_250_R", "weight": 500}
    AASM_250 = {"clsid": "{AASM_250}", "name": "AASM_250", "weight": 250}


inject_weapons(RafaleWeapons)


class Rafale_B(PlaneType):
    id = "Rafale_B"
    flyable = True
    height = 5.2
    width = 10.86
    length = 14.36
    fuel_max = 3165
    max_speed = 2376
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Liveries:
        class USSR(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Georgia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Venezuela(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Australia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Israel(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Combined_Joint_Task_Forces_Blue(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Sudan(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Norway(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Romania(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Iran(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Ukraine(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Libya(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Belgium(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Slovakia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Greece(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class UK(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Third_Reich(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Hungary(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Abkhazia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Morocco(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class United_Nations_Peacekeepers(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Switzerland(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class SouthOssetia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Vietnam(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class China(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Yemen(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Kuwait(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Serbia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Oman(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class India(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Egypt(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class TheNetherlands(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Poland(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Syria(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Finland(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Kazakhstan(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Denmark(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Sweden(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Croatia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class CzechRepublic(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class GDR(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Yugoslavia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Bulgaria(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class SouthKorea(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Tunisia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Combined_Joint_Task_Forces_Red(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Lebanon(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Portugal(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Cuba(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Insurgents(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class SaudiArabia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class France(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class USA(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Honduras(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Qatar(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Russia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class United_Arab_Emirates(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Italian_Social_Republi(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Austria(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Bahrain(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Italy(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Chile(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Turkey(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Philippines(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Algeria(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Pakistan(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Malaysia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Indonesia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Iraq(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Germany(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class South_Africa(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Jordan(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Mexico(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class USAFAggressors(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Brazil(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Spain(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Belarus(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Canada(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class NorthKorea(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Ethiopia(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Japan(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

        class Thailand(Enum):
            _01_RAFALE_B_Lafayette = "01 RAFALE B Lafayette"
            _02_RAFALE_B_MT_DE_MARSAN = "02 RAFALE B MT DE MARSAN"
            _03_RAFALE_B_QATAR = "03 RAFALE B QATAR"
            _04_RAFALE_B_EGYPTE = "04 RAFALE B EGYPTE"
            _05_RAFALE_B_INDE = "05 RAFALE B INDE"
            _06_Greek_air_forces = "06 Greek air forces"
            _07_Rafale_B_Croatian_air_forces = "07 Rafale B Croatian air forces"
            _08_RAFALE_B_EXPORT = "08 RAFALE B EXPORT"
            _09_RAFALE_B_INDIA_AIR_FORCE_OLD = "09 RAFALE B INDIA AIR FORCE OLD"
            _10_Tiger_Meet_2009 = "10 Tiger Meet 2009"
            _11_RAFALE_B_50_ans_des_FAS = "11 RAFALE B 50 ans des FAS"

    class Pylon1:
        MICA_IR_ = (1, Weapons.MICA_IR_)
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)

    class Pylon2:
        gbu12X3_L = (2, Weapons.gbu12X3_L)
        gbu12X2_L = (2, Weapons.gbu12X2_L)
        AASM_250_L = (2, Weapons.AASM_250_L)
        GBU_49 = (2, Weapons.GBU_49)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        GBU12PII = (2, Weapons.GBU12PII)
        Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets = (
            2,
            Weapons.Mk_20_Rockeye___490lbs_CBU__247_x_HEAT_Bomblets,
        )
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            2,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        mk_84 = (2, Weapons.mk_84)
        gbu24 = (2, Weapons.gbu24)
        AASM_1000KG = (2, Weapons.AASM_1000KG)
        AASM_500 = (2, Weapons.AASM_500)
        SCALP = (2, Weapons.SCALP)
        AS_30L = (2, Weapons.AS_30L)

    class Pylon3:
        GBU_49 = (3, Weapons.GBU_49)
        gbu24 = (3, Weapons.gbu24)
        GBU12PII = (3, Weapons.GBU12PII)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _2_Mk_83 = (3, Weapons._2_Mk_83)
        AS_30L = (3, Weapons.AS_30L)
        RAF_RPL711 = (3, Weapons.RAF_RPL711)
        RAF_RPL751 = (3, Weapons.RAF_RPL751)
        mk_84 = (3, Weapons.mk_84)
        AASM_500 = (3, Weapons.AASM_500)

    class Pylon4:
        MICA_IR_ = (4, Weapons.MICA_IR_)

    class Pylon5:
        GBU12PII = (5, Weapons.GBU12PII)
        mk_84 = (5, Weapons.mk_84)
        RAF_RPL711 = (5, Weapons.RAF_RPL711)
        RAF_RPL751 = (5, Weapons.RAF_RPL751)
        Mercury_LLTV_Pod = (5, Weapons.Mercury_LLTV_Pod)
        SCALP = (5, Weapons.SCALP)
        Exocet = (5, Weapons.Exocet)
        GBU_49 = (5, Weapons.GBU_49)
        AASM_1000KG = (5, Weapons.AASM_1000KG)
        gbu24 = (5, Weapons.gbu24)
        MICA_IR_ = (5, Weapons.MICA_IR_)

    class Pylon6:
        MICA_IR_ = (6, Weapons.MICA_IR_)

    class Pylon7:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            7,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )
        Talios_Thales_RBE2 = (7, Weapons.Talios_Thales_RBE2)

    class Pylon8:
        GBU_49 = (8, Weapons.GBU_49)
        gbu24 = (8, Weapons.gbu24)
        GBU12PII = (8, Weapons.GBU12PII)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            8,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        _2_Mk_83_ = (8, Weapons._2_Mk_83_)
        AS_30L = (8, Weapons.AS_30L)
        RAF_RPL711 = (8, Weapons.RAF_RPL711)
        RAF_RPL751 = (8, Weapons.RAF_RPL751)
        mk_84 = (8, Weapons.mk_84)
        AASM_500 = (8, Weapons.AASM_500)

    class Pylon9:
        gbu12X3_R = (9, Weapons.gbu12X3_R)
        gbu12X2_R = (9, Weapons.gbu12X2_R)
        AASM_250_R = (9, Weapons.AASM_250_R)
        GBU_49 = (9, Weapons.GBU_49)
        gbu24 = (9, Weapons.gbu24)
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        GBU12PII = (9, Weapons.GBU12PII)
        AASM_1000KG = (9, Weapons.AASM_1000KG)
        BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets = (
            9,
            Weapons.BRU_42_with_3_x_Mk_20_Rockeye___490lbs_CBUs__247_x_HEAT_Bomblets,
        )
        mk_84 = (9, Weapons.mk_84)
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        SCALP = (9, Weapons.SCALP)
        AS_30L = (9, Weapons.AS_30L)
        AASM_500 = (9, Weapons.AASM_500)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )

    class Pylon10:
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (10, Weapons.Smokewinder___orange)
        MICA_IR_ = (10, Weapons.MICA_IR_)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
        task.SEAD,
        task.PinpointStrike,
    ]
    task_default = task.GroundAttack


class Rafale_C(PlaneType):
    id = "Rafale_C"
    flyable = True
    height = 5.2
    width = 10.86
    length = 14.36
    fuel_max = 3165
    max_speed = 2376
    chaff = 48
    flare = 48
    charge_total = 96
    chaff_charge_size = 1
    flare_charge_size = 1
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Liveries:
        class USSR(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Georgia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Venezuela(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Australia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Israel(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Combined_Joint_Task_Forces_Blue(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Sudan(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Norway(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Romania(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Iran(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Ukraine(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Libya(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Belgium(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Slovakia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Greece(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class UK(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Third_Reich(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Hungary(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Abkhazia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Morocco(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class United_Nations_Peacekeepers(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Switzerland(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class SouthOssetia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Vietnam(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class China(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Yemen(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Kuwait(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Serbia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Oman(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class India(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Egypt(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class TheNetherlands(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Poland(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Syria(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Finland(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Kazakhstan(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Denmark(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Sweden(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Croatia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class CzechRepublic(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class GDR(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Yugoslavia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Bulgaria(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class SouthKorea(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Tunisia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Combined_Joint_Task_Forces_Red(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Lebanon(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Portugal(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Cuba(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Insurgents(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class SaudiArabia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class France(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class USA(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Honduras(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Qatar(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Russia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class United_Arab_Emirates(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Italian_Social_Republi(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Austria(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Bahrain(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Italy(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Chile(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Turkey(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Philippines(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Algeria(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Pakistan(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Malaysia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Indonesia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Iraq(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Germany(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class South_Africa(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Jordan(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Mexico(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class USAFAggressors(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Brazil(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Spain(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Belarus(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Canada(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class NorthKorea(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Ethiopia(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Japan(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

        class Thailand(Enum):
            _01_RAFALE_C_Lafayette = "01 RAFALE C Lafayette"
            _02_RAFALE_C_MT_DE_MARSAN = "02 RAFALE C MT DE MARSAN"
            _03_RAFALE_C_QATAR = "03 RAFALE C QATAR"
            _04_RAFALE_C_EGYPTE = "04 RAFALE C EGYPTE"
            _05_RAFALE_C_INDE = "05 RAFALE C INDE"
            _06_RAFALE_C__GRECE = "06 RAFALE C  GRECE"
            _07_RAFALE_C_CROATIA = "07 RAFALE C CROATIA"
            _08_RAFALE_C_EXPORT = "08 RAFALE C EXPORT"
            _09_RAFALE_C_INDIA_AIR_FORCE = "09 RAFALE C INDIA AIR FORCE"
            _10_PROVENCE_TIGER_MEET_2013 = "10 PROVENCE TIGER MEET 2013"
            _11_SOLO_DISPLAY_2018 = "11 SOLO DISPLAY 2018"
            _12_Dark_tiger = "12 Dark tiger"
            _13_RAFALE_C_Normandie_Niemen_75_ans = "13 RAFALE C Normandie Niemen 75 ans"
            _14_RAFALE_C_SPA162 = "14 RAFALE C SPA162"
            _15_RAFALE_C_CROATIAN_AIR_FORCES = "15 RAFALE C CROATIAN AIR FORCES"
            _06_Greek_air_forces = "06 Greek air forces"

    class Pylon1:
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        MICA_IR_ = (1, Weapons.MICA_IR_)

    class Pylon2:
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        mk_84 = (2, Weapons.mk_84)
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            2,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        METEOR = (2, Weapons.METEOR)
        AASM_250 = (2, Weapons.AASM_250)
        AASMx3L = (2, Weapons.AASMx3L)
        MICA_NG = (2, Weapons.MICA_NG)
        MICA_IR_ = (2, Weapons.MICA_IR_)
        _2_Mk_83 = (2, Weapons._2_Mk_83)

    class Pylon3:
        mk_84 = (3, Weapons.mk_84)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            3,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        RAF_RPL711 = (3, Weapons.RAF_RPL711)
        RAF_RPL751 = (3, Weapons.RAF_RPL751)
        METEOR = (3, Weapons.METEOR)
        MICA_NG = (3, Weapons.MICA_NG)
        _2_Mk_83 = (3, Weapons._2_Mk_83)

    class Pylon4:
        METEOR = (4, Weapons.METEOR)
        MICA_NG = (4, Weapons.MICA_NG)
        MICA_IR_ = (4, Weapons.MICA_IR_)

    class Pylon5:
        mk_84 = (5, Weapons.mk_84)
        RAF_RPL711 = (5, Weapons.RAF_RPL711)
        RAF_RPL751 = (5, Weapons.RAF_RPL751)
        METEOR = (5, Weapons.METEOR)
        MICA_NG = (5, Weapons.MICA_NG)
        MICA_IR_ = (5, Weapons.MICA_IR_)

    class Pylon6:
        METEOR = (6, Weapons.METEOR)
        MICA_NG = (6, Weapons.MICA_NG)
        MICA_IR_ = (6, Weapons.MICA_IR_)

    class Pylon7:
        AN_AAQ_28_LITENING___Targeting_Pod = (
            7,
            Weapons.AN_AAQ_28_LITENING___Targeting_Pod,
        )
        Talios_Thales_RBE2 = (7, Weapons.Talios_Thales_RBE2)

    class Pylon8:
        mk_84 = (8, Weapons.mk_84)
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            8,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            8,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        RAF_RPL711 = (8, Weapons.RAF_RPL711)
        RAF_RPL751 = (8, Weapons.RAF_RPL751)
        METEOR = (8, Weapons.METEOR)
        MICA_NG = (8, Weapons.MICA_NG)
        _2_Mk_83_ = (8, Weapons._2_Mk_83_)

    class Pylon9:
        METEOR = (9, Weapons.METEOR)
        MICA_NG = (9, Weapons.MICA_NG)
        mk_84 = (9, Weapons.mk_84)
        BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.BRU_42_with_3_x_Mk_82___500lb_GP_Bombs_LD,
        )
        MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_83___1000lb_GP_Bombs_LD,
        )
        MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD = (
            9,
            Weapons.MER2_with_2_x_Mk_82___500lb_GP_Bombs_LD,
        )
        AASM_250_RIGHT = (9, Weapons.AASM_250_RIGHT)
        AASMx3R = (9, Weapons.AASMx3R)
        MICA_IR_ = (9, Weapons.MICA_IR_)
        _2_Mk_83_ = (9, Weapons._2_Mk_83_)

    class Pylon10:
        MICA_IR_ = (10, Weapons.MICA_IR_)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (10, Weapons.Smokewinder___orange)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
        task.Reconnaissance,
        task.Intercept,
    ]
    task_default = task.GroundAttack
