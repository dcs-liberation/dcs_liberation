from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

class RafaleWeapons:
    SCALP = {"clsid": "{SCALP}", "name": "SCALP", "weight": None}
    AS_30L = {"clsid": "{AS_30L}", "name": "AS_30L", "weight": 292}
    Exocet = {"clsid": "{Exocet}", "name": "Exocet", "weight": 640}
    Thales_RBE2 = {"clsid": "{Thales_RBE2}", "name": "Thales_RBE2", "weight": 1.4789}
    DAMOCLES = {"clsid": "{DAMOCLES}", "name": "DAMOCLES", "weight": 265}
    DAMOCLES_ = {"clsid": "{DAMOCLES}", "name": "DAMOCLES", "weight": 265}
    _2300_PTB_RAF = {"clsid": "{2300-PTB RAF}", "name": "2300-PTB RAF", "weight": 70}
    _2300_PTB_RAF_ = {"clsid": "{2300-PTB RAF}", "name": "2300-PTB RAF", "weight": 70}
    PTB_1500 = {"clsid": "{PTB-1500}", "name": "PTB-1500", "weight": 70}


class Rafale_A_S(PlaneType):
    id = "Rafale_A_S"
    flyable = False
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

        class Georgia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Syria(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Finland(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Australia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Germany(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class SaudiArabia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Israel(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Croatia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class CzechRepublic(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Norway(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Romania(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Spain(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Ukraine(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Belgium(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Slovakia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Greece(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class UK(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Insurgents(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Hungary(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class France(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Abkhazia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Russia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Sweden(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Austria(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Switzerland(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Italy(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class SouthOssetia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class SouthKorea(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Iran(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class China(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Pakistan(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Belarus(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class NorthKorea(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Iraq(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Kazakhstan(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Bulgaria(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Serbia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class India(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class USAFAggressors(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class USA(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Denmark(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Egypt(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Canada(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class TheNetherlands(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Turkey(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Japan(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Poland(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

    class Pylon1:
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        MICA_IR = (1, Weapons.MICA_IR)
        AIM_9M_Sidewinder_IR_AAM = (1, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (1, Weapons.AIM_9P_Sidewinder_IR_AAM)
#ERRR {BRU-42_3*GBU-12}

    class Pylon2:
        _2xGBU_12 = (2, Weapons._2xGBU_12)
        MER_2_MK_82 = (2, Weapons.MER_2_MK_82)
        _3_Mk_82 = (2, Weapons._3_Mk_82)
        GBU_10 = (2, Weapons.GBU_10)
        GBU_12 = (2, Weapons.GBU_12)
        Mk_20 = (2, Weapons.Mk_20)
        _3_Mk_20_Rockeye = (2, Weapons._3_Mk_20_Rockeye)
        Mk_84 = (2, Weapons.Mk_84)
        GBU_24 = (2, Weapons.GBU_24)
        AGM_88C_ = (2, Weapons.AGM_88C_)
        LAU_131___7_2_75__rockets_M151__HE_ = (2, Weapons.LAU_131___7_2_75__rockets_M151__HE_)
        LAU3_HE151 = (2, Weapons.LAU3_HE151)
        LAU3_WP156 = (2, Weapons.LAU3_WP156)
        LAU3_HE5 = (2, Weapons.LAU3_HE5)
        SCALP = (2, RafaleWeapons.SCALP)
        AS_30L = (2, RafaleWeapons.AS_30L)

    class Pylon3:
        GBU_10 = (3, Weapons.GBU_10)
        GBU_24 = (3, Weapons.GBU_24)
#ERRR {BRU-42_3*GBU-12}
        _2xGBU_12 = (3, Weapons._2xGBU_12)
        GBU_12 = (3, Weapons.GBU_12)
        MER_2_MK_82 = (3, Weapons.MER_2_MK_82)
        _3_Mk_82 = (3, Weapons._3_Mk_82)
        AGM_88C_ = (3, Weapons.AGM_88C_)
        LAU3_HE151 = (3, Weapons.LAU3_HE151)
        LAU3_WP156 = (3, Weapons.LAU3_WP156)
        LAU_131x3_HYDRA_70_M151 = (3, Weapons.LAU_131x3_HYDRA_70_M151)
        SCALP = (3, RafaleWeapons.SCALP)
        AS_30L = (3, RafaleWeapons.AS_30L)
        PTB_1500 = (3, RafaleWeapons.PTB_1500)
        _2300_PTB_RAF_ = (3, RafaleWeapons._2300_PTB_RAF)

    class Pylon4:
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (4, Weapons.AIM_9P_Sidewinder_IR_AAM)
        MICA_IR = (4, Weapons.MICA_IR)
        LAU3_WP156 = (4, Weapons.LAU3_WP156)

    class Pylon5:
        Mk_84 = (5, Weapons.Mk_84)
        PTB_1500 = (5, RafaleWeapons.PTB_1500)
        _2300_PTB_RAF_ = (5, RafaleWeapons._2300_PTB_RAF)
        Mercury_LLTV_Pod = (5, Weapons.Mercury_LLTV_Pod)
        Exocet = (5, RafaleWeapons.Exocet)

    class Pylon6:
        AIM_9M_Sidewinder_IR_AAM = (6, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (6, Weapons.AIM_9P_Sidewinder_IR_AAM)
        MICA_IR = (6, Weapons.MICA_IR)
        LAU3_WP156 = (6, Weapons.LAU3_WP156)

    class Pylon7:
        AN_AAQ_28_LITENING = (7, Weapons.AN_AAQ_28_LITENING)
        DAMOCLES_ = (7, RafaleWeapons.DAMOCLES_)
        Thales_RBE2 = (7, RafaleWeapons.Thales_RBE2)

    class Pylon8:
        GBU_10 = (8, Weapons.GBU_10)
        GBU_24 = (8, Weapons.GBU_24)
#ERRR {BRU-42_3*GBU-12}
        _2xGBU_12 = (8, Weapons._2xGBU_12)
        GBU_12 = (8, Weapons.GBU_12)
        MER_2_MK_82 = (8, Weapons.MER_2_MK_82)
        _3_Mk_20_Rockeye = (8, Weapons._3_Mk_20_Rockeye)
        _3_Mk_82 = (8, Weapons._3_Mk_82)
        AGM_88C_ = (8, Weapons.AGM_88C_)
        LAU3_HE151 = (8, Weapons.LAU3_HE151)
        LAU3_WP156 = (8, Weapons.LAU3_WP156)
        LAU_131x3_HYDRA_70_M151 = (8, Weapons.LAU_131x3_HYDRA_70_M151)
        SCALP = (8, RafaleWeapons.SCALP)
        AS_30L = (8, RafaleWeapons.AS_30L)
        PTB_1500 = (8, RafaleWeapons.PTB_1500)
        _2300_PTB_RAF_ = (8, RafaleWeapons._2300_PTB_RAF)

    class Pylon9:
        GBU_24 = (9, Weapons.GBU_24)
#ERRR {BRU-42_3*GBU-12}
        MER_2_MK_82 = (9, Weapons.MER_2_MK_82)
        _2xGBU_12 = (9, Weapons._2xGBU_12)
        GBU_10 = (9, Weapons.GBU_10)
        GBU_12 = (9, Weapons.GBU_12)
        Mk_20 = (9, Weapons.Mk_20)
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
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        MICA_IR = (10, Weapons.MICA_IR)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (10, Weapons.Smokewinder___orange)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [task.CAP, task.Escort, task.FighterSweep, task.GroundAttack, task.CAS, task.AFAC, task.RunwayAttack, task.AntishipStrike]
    task_default = task.CAP


class Rafale_M(PlaneType):
    id = "Rafale_M"
    flyable = False
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

        class Georgia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Syria(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Finland(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Australia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Germany(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class SaudiArabia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Israel(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Croatia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class CzechRepublic(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Norway(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Romania(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Spain(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Ukraine(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Belgium(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Slovakia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Greece(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class UK(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Insurgents(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Hungary(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class France(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Abkhazia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Russia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Sweden(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Austria(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Switzerland(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Italy(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class SouthOssetia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class SouthKorea(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Iran(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class China(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Pakistan(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Belarus(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class NorthKorea(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Iraq(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Kazakhstan(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Bulgaria(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Serbia(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class India(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class USAFAggressors(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class USA(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Denmark(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Egypt(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Canada(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class TheNetherlands(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Turkey(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Japan(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

        class Poland(Enum):
            _01_MARINE_12_F = "01 MARINE 12 F"
            _02_MARINE_MAT_17F = "02 MARINE MAT 17F"
            _03_BLACK_DERIVE_11F = "03 BLACK DERIVE 11F"
            _04_MARINE_OLD = "04 MARINE OLD"
            _05_BRAZIL = "05 BRAZIL"
            _06_NEUTRE = "06 NEUTRE"

    class Pylon1:
        Smokewinder___red = (1, Weapons.Smokewinder___red)
        Smokewinder___green = (1, Weapons.Smokewinder___green)
        Smokewinder___blue = (1, Weapons.Smokewinder___blue)
        Smokewinder___white = (1, Weapons.Smokewinder___white)
        Smokewinder___yellow = (1, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (1, Weapons.Smokewinder___orange)
        MICA_IR = (1, Weapons.MICA_IR)
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
        PTB_1500 = (3, RafaleWeapons.PTB_1500)
        _2300_PTB_RAF_ = (3, RafaleWeapons._2300_PTB_RAF)

    class Pylon4:
        MICA_IR = (4, Weapons.MICA_IR)
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (4, Weapons.AIM_9P_Sidewinder_IR_AAM)
        LAU3_WP156 = (4, Weapons.LAU3_WP156)

    class Pylon5:
        PTB_1500 = (5, RafaleWeapons.PTB_1500)
        _2300_PTB_RAF_ = (5, RafaleWeapons._2300_PTB_RAF)
        MICA_IR = (5, Weapons.MICA_IR)
        AIM_7M = (5, Weapons.AIM_7M)
        AIM_120B = (5, Weapons.AIM_120B)
        AIM_120C = (5, Weapons.AIM_120C)
        Super_530D = (5, Weapons.Super_530D)

    class Pylon6:
        MICA_IR = (6, Weapons.MICA_IR)
        AIM_9M_Sidewinder_IR_AAM = (6, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (6, Weapons.AIM_9P_Sidewinder_IR_AAM)
        LAU3_WP156 = (6, Weapons.LAU3_WP156)

    class Pylon7:
        AN_AAQ_28_LITENING = (7, Weapons.AN_AAQ_28_LITENING)
        DAMOCLES_ = (7, RafaleWeapons.DAMOCLES_)

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
        PTB_1500 = (8, RafaleWeapons.PTB_1500)
        _2300_PTB_RAF_ = (8, RafaleWeapons._2300_PTB_RAF)

    class Pylon9:
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

    class Pylon10:
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9P_Sidewinder_IR_AAM = (10, Weapons.AIM_9P_Sidewinder_IR_AAM)
        MICA_IR = (10, Weapons.MICA_IR)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        Smokewinder___orange = (10, Weapons.Smokewinder___orange)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    tasks = [task.CAP, task.Escort, task.FighterSweep, task.GroundAttack, task.CAS, task.AFAC, task.RunwayAttack, task.AntishipStrike, task.Reconnaissance, task.Intercept]
    task_default = task.CAP
