from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons

from pydcs_extensions.weapon_injector import inject_weapons


class ProwlerWeapons:
    EA6B_AN_ALQ_99 = {
        "clsid": "{EA6B_ANALQ991}",
        "name": "EA6B AN-ALQ-99",
        "weight": 435,
    }
    EA6B_AN_ALQ_99_ = {
        "clsid": "{EA6B_ANALQ992}",
        "name": "EA6B AN-ALQ-99",
        "weight": 435,
    }


inject_weapons(ProwlerWeapons)


class EA_6B(PlaneType):
    id = "EA_6B"
    height = 4.57
    width = 10.15
    length = 17.98
    fuel_max = 6994
    max_speed = 1047.96
    chaff = 30
    flare = 30
    charge_total = 60
    chaff_charge_size = 1
    flare_charge_size = 1
    eplrs = True
    radio_frequency = 250.5

    class Liveries:
        class USSR(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Georgia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Venezuela(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Australia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Israel(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Combined_Joint_Task_Forces_Blue(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Sudan(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Norway(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Romania(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Iran(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Ukraine(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Libya(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Belgium(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Slovakia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Greece(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class UK(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Third_Reich(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Hungary(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Abkhazia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Morocco(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class United_Nations_Peacekeepers(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Switzerland(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class SouthOssetia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Vietnam(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class China(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Yemen(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Kuwait(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Serbia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Oman(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class India(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Egypt(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class TheNetherlands(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Poland(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Syria(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Finland(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Kazakhstan(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Denmark(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Sweden(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Croatia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class CzechRepublic(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class GDR(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Yugoslavia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Bulgaria(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class SouthKorea(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Tunisia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Combined_Joint_Task_Forces_Red(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Lebanon(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Portugal(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Cuba(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Insurgents(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class SaudiArabia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class France(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class USA(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Honduras(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Qatar(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Russia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class United_Arab_Emirates(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Italian_Social_Republi(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Austria(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Bahrain(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Italy(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Chile(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Turkey(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Philippines(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Algeria(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Pakistan(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Malaysia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Indonesia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Iraq(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Germany(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class South_Africa(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Jordan(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Mexico(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class USAFAggressors(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Brazil(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Spain(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Belarus(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Canada(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class NorthKorea(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Ethiopia(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Japan(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

        class Thailand(Enum):
            AMERICA_621_AB_159485 = "AMERICA 621 AB 159485"
            MARINES_06_CB_161352 = "MARINES 06 CB 161352"
            S_TRUMAN_500_AC_162938 = "S.TRUMAN 500 AC 162938"
            STENNIS_500_NK_159907 = "STENNIS 500 NK 159907"
            VAQ_132_Scorpion_Enterprice = "VAQ-132 Scorpion Enterprice"
            VMAQ_2_CY_159909 = "VMAQ-2 CY 159909"
            VMAQ_2_CY_160432 = "VMAQ-2 CY 160432"

    class Pylon1:
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            1,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            1,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        F_5_275Gal_Fuel_tank = (1, Weapons.F_5_275Gal_Fuel_tank)
        EA6B_AN_ALQ_99 = (1, Weapons.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    class Pylon2:
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            2,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            2,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        F_5_275Gal_Fuel_tank = (2, Weapons.F_5_275Gal_Fuel_tank)
        EA6B_AN_ALQ_99 = (2, Weapons.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    class Pylon3:
        F_5_275Gal_Fuel_tank = (3, Weapons.F_5_275Gal_Fuel_tank)
        EA6B_AN_ALQ_99_ = (3, Weapons.EA6B_AN_ALQ_99_)

    # ERRR <CLEAN>

    class Pylon4:
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            4,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            4,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        F_5_275Gal_Fuel_tank = (4, Weapons.F_5_275Gal_Fuel_tank)
        EA6B_AN_ALQ_99 = (4, Weapons.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    class Pylon5:
        LAU_118a_with_AGM_45B_Shrike_ARM__Imp_ = (
            5,
            Weapons.LAU_118a_with_AGM_45B_Shrike_ARM__Imp_,
        )
        AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_ = (
            5,
            Weapons.AGM_88C_HARM___High_Speed_Anti_Radiation_Missile_,
        )
        F_5_275Gal_Fuel_tank = (5, Weapons.F_5_275Gal_Fuel_tank)
        EA6B_AN_ALQ_99 = (5, Weapons.EA6B_AN_ALQ_99)

    # ERRR <CLEAN>

    pylons = {1, 2, 3, 4, 5}

    tasks = [
        task.Escort,
        task.Reconnaissance,
        task.GroundAttack,
        task.CAS,
        task.AFAC,
        task.RunwayAttack,
        task.AntishipStrike,
        task.SEAD,
    ]
    task_default = task.GroundAttack
