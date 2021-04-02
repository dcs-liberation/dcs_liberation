from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons


class F22AWeapons:
    AIM_9XX = {"clsid": "{AIM-9XX}", "name": "AIM-9XX", "weight": 85}
    AIM_120D = {"clsid": "{AIM-120D}", "name": "AIM-120D", "weight": 152}


class F_22A(PlaneType):
    id = "F-22A"
    flyable = True
    height = 4.88
    width = 13.05
    length = 19.1
    fuel_max = 6103
    max_speed = 2649.996
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    property_defaults = {
        "BAY_DOOR_OPTION": False,
    }

    class Properties:
        class BAY_DOOR_OPTION:
            id = "BAY_DOOR_OPTION"

    class Liveries:
        class USSR(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Georgia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Venezuela(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Australia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Israel(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Combined_Joint_Task_Forces_Blue(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Sudan(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Norway(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Romania(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Iran(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Ukraine(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Libya(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Belgium(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Slovakia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Greece(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class UK(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Third_Reich(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Hungary(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Abkhazia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Morocco(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class United_Nations_Peacekeepers(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Switzerland(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class SouthOssetia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Vietnam(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class China(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Yemen(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Kuwait(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Serbia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Oman(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class India(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Egypt(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class TheNetherlands(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Poland(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Syria(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Finland(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Kazakhstan(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Denmark(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Sweden(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Croatia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class CzechRepublic(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class GDR(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Yugoslavia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Bulgaria(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class SouthKorea(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Tunisia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Combined_Joint_Task_Forces_Red(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Lebanon(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Portugal(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Cuba(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Insurgents(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class SaudiArabia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class France(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class USA(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Honduras(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Qatar(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Russia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class United_Arab_Emirates(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Italian_Social_Republi(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Austria(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Bahrain(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Italy(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Chile(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Turkey(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Philippines(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Algeria(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Pakistan(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Malaysia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Indonesia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Iraq(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Germany(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class South_Africa(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Jordan(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Mexico(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class USAFAggressors(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Brazil(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Spain(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Belarus(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Canada(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class NorthKorea(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Ethiopia(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Japan(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

        class Thailand(Enum):
            default = "default"
            _154_wg = "154 wg"
            _18th_aggressor_sq_blue_foxes_red_23 = "18th aggressor sq blue foxes red 23"
            _18th_aggressor_sq_blue_foxes_red_43 = "18th aggressor sq blue foxes red 43"
            af045 = "af045"
            af172 = "af172"
            _302nd_tactical_fighter_squadron__jasdf = (
                "302nd tactical fighter squadron (jasdf)"
            )
            af188 = "af188"
            af116 = "af116"
            _53rd_fighter_sq_haveglass = "53rd fighter sq haveglass"
            _69_thunder_squadron_iaf_2_0 = "69 thunder squadron iaf 2.0"
            cripes_a_mighty = "cripes'a mighty"
            no_markings = "no markings"
            sea_fictional_raptor = "sea fictional raptor"
            starscream = "starscream"
            tigermeet = "tigermeet"
            yf_22_livery = "yf-22 livery"

    class Pylon1:
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_9XX = (1, F22AWeapons.AIM_9XX)

    class Pylon2:
        Fuel_tank_610_gal = (2, Weapons.Fuel_tank_610_gal)

    class Pylon3:
        AIM_120C = (3, Weapons.AIM_120C)
        AIM_120D = (3, F22AWeapons.AIM_120D)

    class Pylon4:
        AIM_120C = (4, Weapons.AIM_120C)
        AIM_120D = (4, F22AWeapons.AIM_120D)

    class Pylon5:
        AIM_120C = (5, Weapons.AIM_120C)
        AIM_120D = (5, F22AWeapons.AIM_120D)

    class Pylon6:
        Smokewinder___red = (6, Weapons.Smokewinder___red)
        Smokewinder___green = (6, Weapons.Smokewinder___green)
        Smokewinder___blue = (6, Weapons.Smokewinder___blue)
        Smokewinder___white = (6, Weapons.Smokewinder___white)
        Smokewinder___yellow = (6, Weapons.Smokewinder___yellow)

    class Pylon7:
        AIM_120C = (7, Weapons.AIM_120C)
        AIM_120D = (7, F22AWeapons.AIM_120D)

    class Pylon8:
        AIM_120C = (8, Weapons.AIM_120C)
        AIM_120D = (8, F22AWeapons.AIM_120D)

    class Pylon9:
        AIM_120C = (9, Weapons.AIM_120C)
        AIM_120D = (9, F22AWeapons.AIM_120D)

    class Pylon10:
        Fuel_tank_610_gal = (10, Weapons.Fuel_tank_610_gal)

    class Pylon11:
        AIM_9X_Sidewinder_IR_AAM = (11, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_9XX = (11, F22AWeapons.AIM_9XX)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP
