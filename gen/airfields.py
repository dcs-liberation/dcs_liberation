"""Extra airfield data that is not exposed by pydcs.

Remove once https://github.com/pydcs/dcs/issues/69 tracks getting the missing
data added to pydcs. Until then, missing data can be manually filled in here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from .radios import MHz, RadioFrequency
from .tacan import TacanBand, TacanChannel


@dataclass
class AtcData:
    hf: RadioFrequency
    vhf_fm: RadioFrequency
    vhf_am: RadioFrequency
    uhf: RadioFrequency


@dataclass
class AirfieldData:
    """Additional airfield data not included in pydcs."""

    #: Name of the theater the airport is in.
    theater: str

    #: ICAO airport code
    icao: Optional[str] = None

    #: Elevation (in ft).
    elevation: int = 0

    #: Runway length (in ft).
    runway_length: int = 0

    #: TACAN channel for the airfield.
    tacan: Optional[TacanChannel] = None

    #: TACAN callsign
    tacan_callsign: Optional[str] = None

    #: VOR as a tuple of (callsign, frequency).
    vor: Optional[Tuple[str, RadioFrequency]] = None

    #: RSBN channel as a tuple of (callsign, channel).
    rsbn: Optional[Tuple[str, int]] = None

    #: Radio channels used by the airfield's ATC. Note that not all airfields
    #: have ATCs.
    atc: Optional[AtcData] = None

    #: Dict of runway heading -> ILS tuple of (callsign, frequency).
    ils: Dict[str, Tuple[str, RadioFrequency]] = field(default_factory=dict)

    #: Dict of runway heading -> PRMG tuple of (callsign, channel).
    prmg: Dict[str, Tuple[str, int]] = field(default_factory=dict)

    #: Dict of runway heading -> outer NDB tuple of (callsign, frequency).
    outer_ndb: Dict[str, Tuple[str, RadioFrequency]] = field(default_factory=dict)

    #: Dict of runway heading -> inner NDB tuple of (callsign, frequency).
    inner_ndb: Dict[str, Tuple[str, RadioFrequency]] = field(default_factory=dict)

    def ils_freq(self, runway: str) -> Optional[RadioFrequency]:
        ils = self.ils.get(runway)
        if ils is not None:
            return ils[1]
        return None


# TODO: Add more airfields.
AIRFIELD_DATA = {
    # Caucasus
    "Batumi": AirfieldData(
        theater="Caucasus",
        icao="UGSB",
        elevation=32,
        runway_length=6792,
        tacan=TacanChannel(16, TacanBand.X),
        tacan_callsign="BTM",
        atc=AtcData(MHz(4, 250), MHz(131, 0), MHz(40, 400), MHz(260, 0)),
        ils={
            "13": ("ILU", MHz(110, 300)),
        },
    ),
    "Kobuleti": AirfieldData(
        theater="Caucasus",
        icao="UG5X",
        elevation=59,
        runway_length=7406,
        tacan=TacanChannel(67, TacanBand.X),
        tacan_callsign="KBL",
        atc=AtcData(MHz(4, 350), MHz(133, 0), MHz(40, 800), MHz(262, 0)),
        ils={
            "07": ("IKB", MHz(111, 500)),
        },
        outer_ndb={
            "07": ("KT", MHz(870, 0)),
        },
        inner_ndb={
            "07": ("T", MHz(490, 0)),
        },
    ),
    "Senaki-Kolkhi": AirfieldData(
        theater="Caucasus",
        icao="UGKS",
        elevation=43,
        runway_length=7256,
        tacan=TacanChannel(31, TacanBand.X),
        tacan_callsign="TSK",
        atc=AtcData(MHz(4, 300), MHz(132, 0), MHz(40, 600), MHz(261, 0)),
        ils={
            "09": ("ITS", MHz(108, 900)),
        },
        outer_ndb={
            "09": ("BI", MHz(335, 0)),
        },
        inner_ndb={
            "09": ("I", MHz(688, 0)),
        },
    ),
    "Kutaisi": AirfieldData(
        theater="Caucasus",
        icao="UGKO",
        elevation=147,
        runway_length=7937,
        tacan=TacanChannel(44, TacanBand.X),
        tacan_callsign="KTS",
        atc=AtcData(MHz(4, 400), MHz(134, 0), MHz(41, 0), MHz(263, 0)),
        ils={
            "08": ("IKS", MHz(109, 750)),
        },
    ),
    "Sukhumi-Babushara": AirfieldData(
        theater="Caucasus",
        icao="UGSS",
        elevation=43,
        runway_length=11217,
        atc=AtcData(MHz(4, 150), MHz(129, 0), MHz(40, 0), MHz(258, 0)),
        outer_ndb={
            "30": ("AV", MHz(489, 0)),
        },
        inner_ndb={
            "30": ("A", MHz(995, 0)),
        },
    ),
    "Gudauta": AirfieldData(
        theater="Caucasus",
        icao="UG23",
        elevation=68,
        runway_length=7839,
        atc=AtcData(MHz(4, 200), MHz(120, 0), MHz(40, 200), MHz(259, 0)),
    ),
    "Sochi-Adler": AirfieldData(
        theater="Caucasus",
        icao="URSS",
        elevation=98,
        runway_length=9686,
        atc=AtcData(MHz(4, 50), MHz(127, 0), MHz(39, 600), MHz(256, 0)),
        ils={
            "06": ("ISO", MHz(111, 100)),
        },
    ),
    "Gelendzhik": AirfieldData(
        theater="Caucasus",
        icao="URKG",
        elevation=72,
        runway_length=5452,
        vor=("GN", MHz(114, 30)),
        atc=AtcData(MHz(4, 0), MHz(126, 0), MHz(39, 400), MHz(255, 0)),
    ),
    "Novorossiysk": AirfieldData(
        theater="Caucasus",
        icao="URKN",
        elevation=131,
        runway_length=5639,
        atc=AtcData(MHz(3, 850), MHz(123, 0), MHz(38, 800), MHz(252, 0)),
    ),
    "Anapa-Vityazevo": AirfieldData(
        theater="Caucasus",
        icao="URKA",
        elevation=141,
        runway_length=8623,
        atc=AtcData(MHz(3, 750), MHz(121, 0), MHz(38, 400), MHz(250, 0)),
        outer_ndb={
            "22": ("AP", MHz(443, 0)),
            "04": ("AN", MHz(443)),
        },
        inner_ndb={
            "22": ("P", MHz(215, 0)),
            "04": ("N", MHz(215)),
        },
    ),
    "Krymsk": AirfieldData(
        theater="Caucasus",
        icao="URKW",
        elevation=65,
        runway_length=6733,
        rsbn=("KW", 28),
        atc=AtcData(MHz(3, 900), MHz(124, 0), MHz(39, 0), MHz(253, 0)),
        prmg={
            "04": ("OX", 26),
            "22": ("KW", 26),
        },
        outer_ndb={
            "04": ("OX", MHz(408, 0)),
            "22": ("KW", MHz(408, 0)),
        },
        inner_ndb={
            "04": ("O", MHz(803, 0)),
            "22": ("K", MHz(803, 0)),
        },
    ),
    "Krasnodar-Center": AirfieldData(
        theater="Caucasus",
        icao="URKL",
        elevation=98,
        runway_length=7659,
        rsbn=("MB", 40),
        atc=AtcData(MHz(3, 800), MHz(122, 0), MHz(38, 600), MHz(251, 0)),
        prmg={
            "09": ("MB", 38),
        },
        outer_ndb={
            "09": ("MB", MHz(625, 0)),
            "27": ("OC", MHz(625, 0)),
        },
        inner_ndb={
            "09": ("M", MHz(303, 0)),
            "27": ("C", MHz(303, 0)),
        },
    ),
    "Krasnodar-Pashkovsky": AirfieldData(
        theater="Caucasus",
        icao="URKK",
        elevation=111,
        runway_length=9738,
        vor=("KN", MHz(115, 80)),
        atc=AtcData(MHz(4, 100), MHz(128, 0), MHz(39, 800), MHz(257, 0)),
        outer_ndb={
            "23": ("LD", MHz(493, 0)),
            "05": ("KR", MHz(493, 0)),
        },
        inner_ndb={
            "23": ("L", MHz(240, 0)),
            "05": ("K", MHz(240, 0)),
        },
    ),
    "Maykop-Khanskaya": AirfieldData(
        theater="Caucasus",
        icao="URKH",
        elevation=590,
        runway_length=10195,
        rsbn=("DG", 34),
        atc=AtcData(MHz(3, 950), MHz(125, 0), MHz(39, 200), MHz(254, 0)),
        prmg={
            "04": ("DG", 36),
        },
        outer_ndb={
            "04": ("DG", MHz(289, 0)),
            "22": ("RK", MHz(289, 0)),
        },
        inner_ndb={
            "4": ("D", MHz(591, 0)),
            "22": ("R", MHz(591, 0)),
        },
    ),
    "Mineralnye Vody": AirfieldData(
        theater="Caucasus",
        icao="URMM",
        elevation=1049,
        runway_length=12316,
        vor=("MN", MHz(117, 10)),
        atc=AtcData(MHz(4, 450), MHz(135, 0), MHz(41, 200), MHz(264, 0)),
        ils={
            "30": ("IMW", MHz(109, 300)),
            "12": ("IMD", MHz(111, 700)),
        },
        outer_ndb={
            "30": ("NR", MHz(583, 0)),
            "12": ("MD", MHz(583, 0)),
        },
        inner_ndb={
            "30": ("N", MHz(283, 0)),
            "12": ("D", MHz(283, 0)),
        },
    ),
    "Nalchik": AirfieldData(
        theater="Caucasus",
        icao="URMN",
        elevation=1410,
        runway_length=7082,
        atc=AtcData(MHz(4, 500), MHz(136, 0), MHz(41, 400), MHz(265, 0)),
        ils={
            "24": ("INL", MHz(110, 500)),
        },
        outer_ndb={
            "24": ("NL", MHz(718, 0)),
        },
        inner_ndb={
            "24": ("N", MHz(350, 0)),
        },
    ),
    "Mozdok": AirfieldData(
        theater="Caucasus",
        icao="XRMF",
        elevation=507,
        runway_length=7734,
        rsbn=("MZ", 20),
        atc=AtcData(MHz(4, 550), MHz(137, 0), MHz(41, 600), MHz(266, 0)),
        prmg={
            "26": ("MZ", 22),
            "8": ("MZ", 22),
        },
        outer_ndb={
            "26": ("RM", MHz(525, 0)),
            "8": ("DO", MHz(525, 0)),
        },
        inner_ndb={
            "26": ("R", MHz(1, 6)),
            "8": ("D", MHz(1, 6)),
        },
    ),
    "Beslan": AirfieldData(
        theater="Caucasus",
        icao="URMO",
        elevation=1719,
        runway_length=9327,
        atc=AtcData(MHz(4, 750), MHz(141, 0), MHz(42, 400), MHz(270, 0)),
        ils={
            "10": ("ICH", MHz(110, 500)),
        },
        outer_ndb={
            "10": ("CX", MHz(1, 5)),
        },
        inner_ndb={
            "10": ("C", MHz(250, 0)),
        },
    ),
    "Tbilisi-Lochini": AirfieldData(
        theater="Caucasus",
        icao="UGTB",
        elevation=1573,
        runway_length=7692,
        tacan=TacanChannel(25, TacanBand.X),
        tacan_callsign="GTB",
        atc=AtcData(MHz(4, 600), MHz(138, 0), MHz(41, 800), MHz(267, 0)),
        ils={
            "13": ("INA", MHz(110, 300)),
            "30": ("INA", MHz(108, 900)),
        },
        outer_ndb={
            "13": ("BP", MHz(342, 0)),
            "30": ("NA", MHz(211, 0)),
        },
        inner_ndb={
            "13": ("B", MHz(923, 0)),
            "30": ("N", MHz(435, 0)),
        },
    ),
    "Soganlung": AirfieldData(
        theater="Caucasus",
        icao="UG24",
        elevation=1474,
        runway_length=7871,
        tacan=TacanChannel(25, TacanBand.X),
        tacan_callsign="GTB",
        atc=AtcData(MHz(4, 650), MHz(139, 0), MHz(42, 0), MHz(268, 0)),
    ),
    "Vaziani": AirfieldData(
        theater="Caucasus",
        icao="UG27",
        elevation=1523,
        runway_length=7842,
        tacan=TacanChannel(22, TacanBand.X),
        tacan_callsign="VAS",
        atc=AtcData(MHz(4, 700), MHz(140, 0), MHz(42, 200), MHz(269, 0)),
        ils={
            "13": ("IVZ", MHz(108, 750)),
            "31": ("IVZ", MHz(108, 750)),
        },
    ),
    # PERSIAN GULF MAP
    "Liwa AFB": AirfieldData(
        theater="Persian Gulf",
        icao="OMLW",
        elevation=400,
        runway_length=10768,
        tacan=TacanChannel(121, TacanBand.X),
        tacan_callsign="OMLW",
        vor=("OMLW", MHz(117, 400)),
        atc=AtcData(MHz(4, 225), MHz(39, 350), MHz(119, 300), MHz(250, 950)),
    ),
    "Al Dhafra AFB": AirfieldData(
        theater="Persian Gulf",
        icao="OMAM",
        elevation=52,
        runway_length=11530,
        tacan=TacanChannel(96, TacanBand.X),
        tacan_callsign="MA",
        vor=("MA", MHz(114, 900)),
        atc=AtcData(MHz(4, 300), MHz(39, 500), MHz(126, 500), MHz(251, 100)),
        ils={
            "13": ("MMA", MHz(111, 100)),
            "31": ("IMA", MHz(109, 100)),
        },
    ),
    "Al-Bateen": AirfieldData(
        theater="Persian Gulf",
        icao="OMAD",
        elevation=11,
        runway_length=6808,
        vor=("ALB", MHz(114, 0)),
        atc=AtcData(MHz(4, 75), MHz(39, 50), MHz(119, 900), MHz(250, 600)),
    ),
    "Sas Al Nakheel": AirfieldData(
        theater="Persian Gulf",
        icao="OMNK",
        elevation=9,
        runway_length=5387,
        vor=("SAS", MHz(128, 930)),
        atc=AtcData(MHz(4, 0), MHz(38, 900), MHz(128, 900), MHz(250, 450)),
    ),
    "Abu Dhabi Intl": AirfieldData(
        theater="Persian Gulf",
        icao="OMAA",
        elevation=91,
        runway_length=12817,
        vor=("ADV", MHz(114, 250)),
        atc=AtcData(MHz(4, 50), MHz(39, 0), MHz(119, 200), MHz(250, 550)),
    ),
    "Al Ain Intl": AirfieldData(
        theater="Persian Gulf",
        icao="OMAL",
        elevation=813,
        runway_length=11267,
        vor=("ALN", MHz(112, 600)),
        atc=AtcData(MHz(4, 125), MHz(39, 150), MHz(119, 850), MHz(250, 700)),
    ),
    "Al Maktoum Intl": AirfieldData(
        theater="Persian Gulf",
        icao="OMDW",
        elevation=123,
        runway_length=11500,
        atc=AtcData(MHz(4, 350), MHz(39, 600), MHz(118, 600), MHz(251, 200)),
        ils={
            "30": ("IJWA", MHz(109, 750)),
            "12": ("IMA", MHz(111, 750)),
        },
    ),
    "Al Minhad AFB": AirfieldData(
        theater="Persian Gulf",
        icao="OMDM",
        elevation=190,
        runway_length=11865,
        tacan=TacanChannel(99, TacanBand.X),
        tacan_callsign="MIN",
        atc=AtcData(MHz(3, 800), MHz(38, 500), MHz(118, 550), MHz(250, 100)),
        ils={
            "27": ("IMNR", MHz(110, 750)),
            "9": ("IMNW", MHz(110, 700)),
        },
    ),
    "Dubai Intl": AirfieldData(
        theater="Persian Gulf",
        icao="OMDB",
        elevation=16,
        runway_length=11018,
        atc=AtcData(MHz(4, 325), MHz(39, 550), MHz(118, 750), MHz(251, 150)),
        ils={
            "30": ("IDBL", MHz(110, 900)),
            "12": ("IDBR", MHz(110, 100)),
        },
    ),
    "Sharjah Intl": AirfieldData(
        theater="Persian Gulf",
        icao="OMSJ",
        elevation=98,
        runway_length=10535,
        atc=AtcData(MHz(3, 850), MHz(38, 600), MHz(118, 600), MHz(250, 200)),
        ils={
            "30": ("ISHW", MHz(111, 950)),
            "12": ("ISRE", MHz(108, 550)),
        },
    ),
    "Fujairah Intl": AirfieldData(
        theater="Persian Gulf",
        icao="OMFJ",
        elevation=60,
        runway_length=9437,
        vor=("FJV", MHz(113, 800)),
        atc=AtcData(MHz(4, 375), MHz(39, 650), MHz(124, 600), MHz(251, 250)),
        ils={
            "29": ("IFJR", MHz(111, 500)),
        },
    ),
    "Ras Al Khaimah Intl": AirfieldData(
        theater="Persian Gulf",
        icao="OMRK",
        elevation=70,
        runway_length=8406,
        vor=("OMRK", MHz(113, 600)),
        atc=AtcData(MHz(4, 200), MHz(39, 300), MHz(121, 600), MHz(250, 900)),
    ),
    "Khasab": AirfieldData(
        theater="Persian Gulf",
        icao="OOKB",
        elevation=47,
        runway_length=7513,
        atc=AtcData(MHz(3, 750), MHz(38, 400), MHz(124, 350), MHz(250, 000)),
        ils={
            "19": ("IBKS", MHz(110, 300)),
        },
    ),
    "Sir Abu Nuayr": AirfieldData(
        theater="Persian Gulf",
        icao="OMSN",
        elevation=25,
        runway_length=2229,
        atc=AtcData(MHz(3, 900), MHz(38, 700), MHz(118, 0), MHz(250, 800)),
    ),
    "Sirri Island": AirfieldData(
        theater="Persian Gulf",
        icao="OIBS",
        elevation=17,
        runway_length=7443,
        vor=("SIR", MHz(113, 750)),
        atc=AtcData(MHz(3, 875), MHz(38, 650), MHz(135, 50), MHz(250, 250)),
    ),
    "Abu Musa Island": AirfieldData(
        theater="Persian Gulf",
        icao="OIBA",
        elevation=16,
        runway_length=7616,
        atc=AtcData(MHz(3, 950), MHz(38, 800), MHz(122, 900), MHz(250, 400)),
    ),
    "Tunb Kochak": AirfieldData(
        theater="Persian Gulf",
        icao="OITK",
        elevation=15,
        runway_length=1481,
        tacan=TacanChannel(89, TacanBand.X),
        tacan_callsign="KCK",
    ),
    "Tunb Island AFB": AirfieldData(
        theater="Persian Gulf",
        icao="OIGI",
        elevation=42,
        runway_length=6099,
    ),
    "Qeshm Island": AirfieldData(
        theater="Persian Gulf",
        icao="OIKQ",
        elevation=26,
        runway_length=13287,
        vor=("KHM", MHz(117, 100)),
        atc=AtcData(MHz(3, 825), MHz(38, 550), MHz(118, 50), MHz(250, 150)),
    ),
    "Bandar-e-Jask": AirfieldData(
        theater="Persian Gulf",
        icao="OIZJ",
        elevation=26,
        runway_length=6842,
        vor=("KHM", MHz(116, 300)),
        atc=AtcData(MHz(4, 25), MHz(38, 950), MHz(118, 150), MHz(250, 500)),
    ),
    "Bandar Lengeh": AirfieldData(
        theater="Persian Gulf",
        icao="OIBL",
        elevation=80,
        runway_length=7625,
        vor=("LEN", MHz(114, 800)),
        atc=AtcData(MHz(4, 275), MHz(39, 450), MHz(121, 700), MHz(251, 50)),
    ),
    "Kish Intl": AirfieldData(
        theater="Persian Gulf",
        icao="OIBK",
        elevation=114,
        runway_length=10617,
        tacan=TacanChannel(112, TacanBand.X),
        tacan_callsign="KIH",
        atc=AtcData(MHz(4, 100), MHz(39, 100), MHz(121, 650), MHz(250, 650)),
    ),
    "Lavan Island": AirfieldData(
        theater="Persian Gulf",
        icao="OIBV",
        elevation=75,
        runway_length=8234,
        vor=("LVA", MHz(116, 850)),
        atc=AtcData(MHz(4, 150), MHz(39, 200), MHz(128, 550), MHz(250, 750)),
    ),
    "Lar": AirfieldData(
        theater="Persian Gulf",
        icao="OISL",
        elevation=2635,
        runway_length=9600,
        vor=("LAR", MHz(117, 900)),
        atc=AtcData(MHz(3, 775), MHz(38, 450), MHz(127, 350), MHz(250, 50)),
    ),
    "Havadarya": AirfieldData(
        theater="Persian Gulf",
        icao="OIKP",
        elevation=50,
        runway_length=7300,
        tacan=TacanChannel(47, TacanBand.X),
        tacan_callsign="HDR",
        atc=AtcData(MHz(4, 400), MHz(39, 700), MHz(123, 150), MHz(251, 300)),
        ils={
            "8": ("IBHD", MHz(108, 900)),
        },
    ),
    "Bandar Abbas Intl": AirfieldData(
        theater="Persian Gulf",
        icao="OIKB",
        elevation=18,
        runway_length=11640,
        tacan=TacanChannel(78, TacanBand.X),
        tacan_callsign="BND",
        vor=("BND", MHz(117, 200)),
        atc=AtcData(MHz(4, 250), MHz(39, 400), MHz(118, 100), MHz(251, 0)),
        ils={
            "21": ("IBND", MHz(109, 900)),
        },
    ),
    "Jiroft": AirfieldData(
        theater="Persian Gulf",
        icao="OIKJ",
        elevation=2664,
        runway_length=9160,
        atc=AtcData(MHz(4, 125), MHz(39, 120), MHz(136, 0), MHz(250, 750)),
    ),
    "Kerman": AirfieldData(
        theater="Persian Gulf",
        icao="OIKK",
        elevation=5746,
        runway_length=11981,
        tacan=TacanChannel(97, TacanBand.X),
        tacan_callsign="KER",
        vor=("KER", MHz(112, 0)),
        atc=AtcData(MHz(3, 925), MHz(38, 750), MHz(118, 250), MHz(250, 300)),
    ),
    "Shiraz Intl": AirfieldData(
        theater="Persian Gulf",
        icao="OISS",
        elevation=4878,
        runway_length=13271,
        tacan=TacanChannel(94, TacanBand.X),
        tacan_callsign="SYZ1",
        vor=("SYZ", MHz(112, 0)),
        atc=AtcData(MHz(3, 950), MHz(38, 800), MHz(121, 900), MHz(250, 350)),
    ),
    # Syria Map
    "Adana Sakirpasa": AirfieldData(
        theater="Syria",
        icao="LTAF",
        elevation=55,
        runway_length=8115,
        vor=("ADA", MHz(112, 700)),
        atc=AtcData(MHz(4, 275), MHz(39, 450), MHz(121, 100), MHz(251, 0)),
        ils={
            "05": ("IADA", MHz(108, 700)),
        },
    ),
    "Incirlik": AirfieldData(
        theater="Syria",
        icao="LTAG",
        elevation=156,
        runway_length=9662,
        tacan=TacanChannel(21, TacanBand.X),
        tacan_callsign="DAN",
        vor=("DAN", MHz(108, 400)),
        atc=AtcData(MHz(3, 900), MHz(38, 700), MHz(122, 100), MHz(360, 100)),
        ils={
            "05": ("IDAN", MHz(109, 300)),
            "23": ("DANM", MHz(111, 700)),
        },
    ),
    "Minakh": AirfieldData(
        theater="Syria",
        icao="OS71",
        elevation=1614,
        runway_length=4648,
        atc=AtcData(MHz(4, 175), MHz(39, 250), MHz(120, 600), MHz(250, 800)),
    ),
    "Hatay": AirfieldData(
        theater="Syria",
        icao="LTDA",
        elevation=253,
        runway_length=9052,
        vor=("HTY", MHz(112, 500)),
        atc=AtcData(MHz(3, 875), MHz(38, 650), MHz(128, 500), MHz(250, 250)),
        ils={
            "22": ("IHTY", MHz(108, 150)),
            "04": ("IHAT", MHz(108, 900)),
        },
    ),
    "Kuweires": AirfieldData(
        theater="Syria",
        icao="OS66",
        elevation=1200,
        runway_length=6662,
        atc=AtcData(MHz(4, 325), MHz(39, 550), MHz(120, 500), MHz(251, 100)),
    ),
    "Aleppo": AirfieldData(
        theater="Syria",
        icao="OSAP",
        elevation=1253,
        runway_length=8332,
        atc=AtcData(MHz(4, 200), MHz(39, 300), MHz(119, 100), MHz(250, 850)),
    ),
    "Jirah": AirfieldData(
        theater="Syria",
        icao="OS62",
        elevation=1170,
        runway_length=9090,
        atc=AtcData(MHz(3, 925), MHz(38, 750), MHz(118, 100), MHz(250, 300)),
    ),
    "Taftanaz": AirfieldData(
        theater="Syria",
        elevation=1020,
        runway_length=2705,
        atc=AtcData(MHz(4, 375), MHz(39, 650), MHz(122, 800), MHz(251, 200)),
    ),
    "Tabqa": AirfieldData(
        theater="Syria",
        icao="OS59",
        elevation=1083,
        runway_length=9036,
        atc=AtcData(MHz(4, 500), MHz(39, 900), MHz(122, 800), MHz(251, 450)),
    ),
    "Abu al-Dahur": AirfieldData(
        theater="Syria",
        icao="OS57",
        elevation=820,
        runway_length=8728,
        atc=AtcData(MHz(4, 0), MHz(38, 900), MHz(122, 200), MHz(250, 450)),
    ),
    "Bassel Al-Assad": AirfieldData(
        theater="Syria",
        icao="OSLK",
        elevation=93,
        runway_length=7305,
        vor=("LTK", MHz(114, 800)),
        atc=AtcData(MHz(4, 50), MHz(39, 0), MHz(118, 100), MHz(250, 550)),
        ils={
            "17": ("IBA", MHz(109, 100)),
        },
    ),
    "Hama": AirfieldData(
        theater="Syria",
        icao="OS58",
        elevation=983,
        runway_length=7957,
        atc=AtcData(MHz(3, 850), MHz(38, 600), MHz(118, 50), MHz(250, 200)),
    ),
    "Rene Mouawad": AirfieldData(
        theater="Syria",
        icao="OLKA",
        elevation=14,
        runway_length=8614,
        atc=AtcData(MHz(4, 375), MHz(39, 650), MHz(121, 0), MHz(251, 200)),
    ),
    "Al Quasayr": AirfieldData(
        theater="Syria",
        icao="OS70",
        elevation=1729,
        runway_length=8585,
        atc=AtcData(MHz(4, 550), MHz(40, 0), MHz(119, 200), MHz(251, 550)),
    ),
    "Palmyra": AirfieldData(
        theater="Syria",
        icao="OSPR",
        elevation=1267,
        runway_length=8704,
        atc=AtcData(MHz(4, 225), MHz(39, 350), MHz(121, 900), MHz(250, 900)),
    ),
    "Wujah Al Hajar": AirfieldData(
        theater="Syria",
        icao="Z19O",
        elevation=619,
        runway_length=4717,
        vor=("CAK", MHz(116, 200)),
        atc=AtcData(MHz(4, 575), MHz(40, 50), MHz(121, 500), MHz(251, 600)),
    ),
    "An Nasiriyah": AirfieldData(
        theater="Syria",
        icao="OS64",
        elevation=2746,
        runway_length=8172,
        atc=AtcData(MHz(4, 600), MHz(40, 100), MHz(122, 300), MHz(251, 650)),
    ),
    "Rayak": AirfieldData(
        theater="Syria",
        icao="OLRA",
        elevation=2934,
        runway_length=8699,
        vor=("HTY", MHz(124, 400)),
        atc=AtcData(MHz(4, 350), MHz(39, 600), MHz(124, 400), MHz(251, 150)),
    ),
    "Beirut-Rafic Hariri": AirfieldData(
        theater="Syria",
        icao="OLBA",
        elevation=39,
        runway_length=9463,
        vor=("KAD", MHz(112, 600)),
        atc=AtcData(MHz(4, 675), MHz(40, 250), MHz(118, 900), MHz(251, 800)),
        ils={
            "17": ("BIL", MHz(109, 500)),
        },
    ),
    "Al-Dumayr": AirfieldData(
        theater="Syria",
        icao="OS61",
        elevation=2066,
        runway_length=8902,
        atc=AtcData(MHz(4, 750), MHz(40, 400), MHz(120, 300), MHz(251, 950)),
    ),
    "Marj as Sultan North": AirfieldData(
        theater="Syria",
        elevation=2007,
        runway_length=268,
        atc=AtcData(MHz(4, 75), MHz(38, 50), MHz(122, 700), MHz(250, 600)),
    ),
    "Marj as Sultan South": AirfieldData(
        theater="Syria",
        elevation=2007,
        runway_length=166,
        atc=AtcData(MHz(4, 725), MHz(40, 350), MHz(122, 900), MHz(251, 900)),
    ),
    "Mezzeh": AirfieldData(
        theater="Syria",
        icao="OS67",
        elevation=2355,
        runway_length=7522,
        atc=AtcData(MHz(4, 150), MHz(39, 200), MHz(120, 700), MHz(250, 750)),
    ),
    "Qabr as Sitt": AirfieldData(
        theater="Syria",
        elevation=2134,
        runway_length=489,
        atc=AtcData(MHz(4, 250), MHz(39, 400), MHz(122, 600), MHz(250, 950)),
    ),
    "Damascus": AirfieldData(
        theater="Syria",
        icao="OSDI",
        elevation=2007,
        runway_length=11423,
        vor=("DAM", MHz(116)),
        atc=AtcData(MHz(4, 700), MHz(40, 300), MHz(118, 500), MHz(251, 850)),
        ils={
            "24": ("IDA", MHz(109, 900)),
        },
    ),
    "Marj Ruhayyil": AirfieldData(
        theater="Syria",
        icao="OS63",
        elevation=2160,
        runway_length=7576,
        atc=AtcData(MHz(4, 100), MHz(39, 100), MHz(120, 800), MHz(250, 6550)),
    ),
    "Kiryat Shmona": AirfieldData(
        theater="Syria",
        icao="LLKS",
        elevation=328,
        runway_length=3258,
        atc=AtcData(MHz(4, 25), MHz(38, 950), MHz(118, 400), MHz(250, 500)),
    ),
    "Khalkhalah": AirfieldData(
        theater="Syria",
        icao="OS69",
        elevation=2337,
        runway_length=8248,
        atc=AtcData(MHz(3, 950), MHz(38, 800), MHz(122, 500), MHz(250, 350)),
    ),
    "Haifa": AirfieldData(
        theater="Syria",
        icao="LLHA",
        elevation=19,
        runway_length=3253,
        atc=AtcData(MHz(3, 825), MHz(38, 550), MHz(127, 800), MHz(250, 150)),
    ),
    "Ramat David": AirfieldData(
        theater="Syria",
        icao="LLRD",
        elevation=105,
        runway_length=7037,
        atc=AtcData(MHz(4, 300), MHz(39, 500), MHz(118, 600), MHz(251, 50)),
    ),
    "Megiddo": AirfieldData(
        theater="Syria",
        icao="LLMG",
        elevation=180,
        runway_length=6098,
        atc=AtcData(MHz(4, 125), MHz(39, 150), MHz(119, 900), MHz(250, 700)),
    ),
    "Eyn Shemer": AirfieldData(
        theater="Syria",
        icao="LLES",
        elevation=93,
        runway_length=3562,
        atc=AtcData(MHz(3, 750), MHz(38, 400), MHz(123, 400), MHz(250)),
    ),
    "King Hussein Air College": AirfieldData(
        theater="Syria",
        icao="OJMF",
        elevation=2204,
        runway_length=8595,
        atc=AtcData(MHz(3, 975), MHz(38, 850), MHz(118, 300), MHz(250, 400)),
    ),
    "Tha'lah": AirfieldData(
        theater="Syria",
        icao="OS60",
        elevation=2381,
        runway_length=8025,
        atc=AtcData(MHz(4, 650), MHz(40, 200), MHz(122, 400), MHz(251, 750)),
    ),
    "Shayrat": AirfieldData(
        theater="Syria",
        icao="OS60",
        elevation=2637,
        runway_length=8553,
        atc=AtcData(MHz(4, 450), MHz(39, 800), MHz(122, 200), MHz(251, 350)),
    ),
    "Tiyas": AirfieldData(
        theater="Syria",
        icao="OS72",
        elevation=1797,
        runway_length=9420,
        atc=AtcData(MHz(4, 525), MHz(39, 950), MHz(120, 500), MHz(251, 500)),
    ),
    "Rosh Pina": AirfieldData(
        theater="Syria",
        icao="LLIB",
        elevation=865,
        runway_length=2711,
        atc=AtcData(MHz(4, 400), MHz(39, 700), MHz(118, 450), MHz(251, 250)),
    ),
    "Sayqal": AirfieldData(
        theater="Syria",
        icao="OS68",
        elevation=2273,
        runway_length=8536,
        atc=AtcData(MHz(4, 425), MHz(39, 750), MHz(120, 400), MHz(251, 300)),
    ),
    "H4": AirfieldData(
        theater="Syria",
        icao="OJHR",
        elevation=2257,
        runway_length=7179,
        atc=AtcData(MHz(3, 800), MHz(38, 500), MHz(120, 400), MHz(250, 100)),
    ),
    "Naqoura": AirfieldData(
        theater="Syria",
        icao="",
        elevation=378,
        runway_length=0,
        atc=AtcData(MHz(4, 625), MHz(40, 150), MHz(122, 000), MHz(251, 700)),
    ),
    "Gaziantep": AirfieldData(
        theater="Syria",
        icao="LTAJ",
        elevation=2287,
        runway_length=8871,
        atc=AtcData(MHz(3, 775), MHz(38, 450), MHz(120, 100), MHz(250, 50)),
        ils={
            "28": ("IGNP", MHz(109, 10)),
        },
    ),
    "Gecitkale": AirfieldData(
        theater="Syria",
        icao="LCGK",
        elevation=147,
        runway_length=8156,
        vor=("GKE", MHz(114, 30)),
        atc=AtcData(MHz(3, 775), MHz(4, 800), MHz(40, 500), MHz(252, 50)),
    ),
    "Kingsfield": AirfieldData(
        theater="Syria",
        icao="CY-0004",
        elevation=270,
        runway_length=3069,
        atc=AtcData(MHz(121, 0), MHz(4, 650), MHz(40, 200), MHz(251, 750)),
    ),
    "Larnaca": AirfieldData(
        theater="Syria",
        icao="LCRE",
        elevation=16,
        runway_length=8009,
        vor=("LCA", MHz(112, 80)),
        atc=AtcData(MHz(121, 200), MHz(4, 700), MHz(40, 300), MHz(251, 850)),
        ils={
            "22": ("ILC", MHz(110, 30)),
        },
    ),
    "Ercan": AirfieldData(
        theater="Syria",
        icao="LCEN",
        elevation=383,
        runway_length=7559,
        vor=("GKE", MHz(114, 30)),
        atc=AtcData(MHz(120, 200), MHz(4, 750), MHz(40, 400), MHz(241, 950)),
    ),
    "Lakatamia": AirfieldData(
        theater="Syria",
        icao="CY-0001",
        elevation=757,
        runway_length=1230,
        atc=AtcData(MHz(120, 200), MHz(4, 725), MHz(40, 350), MHz(251, 900)),
    ),
    "Nicosia": AirfieldData(
        theater="Syria",
        icao="LCNC",
        elevation=716,
        runway_length=0,
    ),
    "Pinarbashi": AirfieldData(
        theater="Syria",
        icao="CY-0003",
        elevation=770,
        runway_length=3364,
        atc=AtcData(MHz(121, 000), MHz(4, 825), MHz(40, 550), MHz(252, 100)),
    ),
    "Akrotiri": AirfieldData(
        theater="Syria",
        icao="LCRA",
        elevation=62,
        runway_length=8276,
        tacan=TacanChannel(107, TacanBand.X),
        tacan_callsign="AKR",
        vor=("AKR", MHz(116, 0)),
        atc=AtcData(MHz(128, 0), MHz(4, 625), MHz(40, 150), MHz(251, 700)),
        ils={
            "28": ("IAK", MHz(109, 70)),
        },
    ),
    "Paphos": AirfieldData(
        theater="Syria",
        icao="LCPH",
        elevation=40,
        runway_length=8425,
        vor=("PHA", MHz(117, 90)),
        atc=AtcData(MHz(119, 900), MHz(4, 675), MHz(40, 250), MHz(251, 800)),
        ils={
            "29": ("IPA", MHz(108, 90)),
        },
    ),
    "Gazipasa": AirfieldData(
        theater="Syria",
        icao="LTFG",
        elevation=36,
        runway_length=6885,
        vor=("GZP", MHz(114, 20)),
        atc=AtcData(MHz(119, 250), MHz(4, 600), MHz(40, 100), MHz(251, 650)),
        ils={
            "8": ("IGZP", MHz(108, 50)),
        },
    ),
    # NTTR
    "Mina Airport 3Q0": AirfieldData(
        theater="NTTR",
        elevation=4562,
        runway_length=4222,
    ),
    "Tonopah Airport": AirfieldData(
        theater="NTTR",
        icao="KTPH",
        elevation=5394,
        runway_length=6715,
    ),
    "Tonopah Test Range Airfield": AirfieldData(
        theater="NTTR",
        icao="KTNX",
        elevation=5534,
        runway_length=11633,
        tacan=TacanChannel(77, TacanBand.X),
        tacan_callsign="TQQ",
        atc=AtcData(MHz(3, 800), MHz(124, 750), MHz(38, 500), MHz(257, 950)),
        ils={
            "32": ("I-UVV", MHz(111, 700)),
            "14": ("I-RVP", MHz(108, 300)),
        },
    ),
    "Beatty Airport": AirfieldData(
        theater="NTTR",
        icao="KBTY",
        elevation=3173,
        runway_length=5380,
    ),
    "Pahute Mesa Airstrip": AirfieldData(
        theater="NTTR",
        elevation=5056,
        runway_length=5420,
    ),
    "Groom Lake AFB": AirfieldData(
        theater="NTTR",
        icao="KXTA",
        elevation=4494,
        runway_length=11008,
        tacan=TacanChannel(18, TacanBand.X),
        tacan_callsign="GRL",
        atc=AtcData(MHz(3, 850), MHz(118, 0), MHz(38, 600), MHz(250, 50)),
        ils={
            "32": ("GLRI", MHz(109, 300)),
        },
    ),
    "Lincoln County": AirfieldData(
        theater="NTTR",
        elevation=4815,
        runway_length=4408,
    ),
    "Mesquite": AirfieldData(
        theater="NTTR",
        icao="67L",
        elevation=1858,
        runway_length=4937,
    ),
    "Creech AFB": AirfieldData(
        theater="NTTR",
        icao="KINS",
        elevation=3126,
        runway_length=6100,
        tacan=TacanChannel(87, TacanBand.X),
        tacan_callsign="INS",
        atc=AtcData(MHz(3, 825), MHz(118, 300), MHz(38, 550), MHz(360, 600)),
        ils={
            "8": ("ICRR", MHz(108, 700)),
        },
    ),
    "Echo Bay": AirfieldData(
        theater="NTTR",
        icao="OL9",
        elevation=3126,
        runway_length=6100,
        tacan=TacanChannel(87, TacanBand.X),
        tacan_callsign="INS",
        atc=AtcData(MHz(3, 825), MHz(118, 300), MHz(38, 550), MHz(360, 600)),
    ),
    "Nellis AFB": AirfieldData(
        theater="NTTR",
        icao="KLSV",
        elevation=1841,
        runway_length=9454,
        tacan=TacanChannel(12, TacanBand.X),
        tacan_callsign="LSV",
        atc=AtcData(MHz(3, 900), MHz(132, 550), MHz(38, 700), MHz(327, 0)),
        ils={
            "21": ("IDIQ", MHz(109, 100)),
        },
    ),
    "North Las Vegas": AirfieldData(
        theater="NTTR",
        icao="KVGT",
        elevation=2228,
        runway_length=4734,
        atc=AtcData(MHz(3, 775), MHz(125, 700), MHz(38, 450), MHz(360, 750)),
    ),
    "McCarran International Airport": AirfieldData(
        theater="NTTR",
        icao="KLAS",
        elevation=2169,
        runway_length=10377,
        tacan=TacanChannel(116, TacanBand.X),
        tacan_callsign="LAS",
        atc=AtcData(MHz(3, 875), MHz(119, 900), MHz(38, 650), MHz(257, 800)),
        ils={
            "25": ("I-LAS", MHz(110, 300)),
        },
    ),
    "Henderson Executive Airport": AirfieldData(
        theater="NTTR",
        icao="KHND",
        elevation=2491,
        runway_length=5999,
        atc=AtcData(MHz(3, 925), MHz(125, 100), MHz(38, 750), MHz(250, 100)),
    ),
    "Boulder City Airport": AirfieldData(
        theater="NTTR",
        icao="KBVU",
        elevation=2121,
        runway_length=4612,
    ),
    "Jean Airport": AirfieldData(
        theater="NTTR",
        elevation=2824,
        runway_length=4053,
    ),
    "Laughlin Airport": AirfieldData(
        theater="NTTR",
        icao="KIFP",
        elevation=656,
        runway_length=7139,
        atc=AtcData(MHz(3, 750), MHz(123, 900), MHz(38, 400), MHz(250, 0)),
    ),
    # Normandy
    "Needs Oar Point": AirfieldData(
        theater="Normandy",
        elevation=30,
        runway_length=5259,
        atc=AtcData(MHz(4, 225), MHz(118, 950), MHz(39, 350), MHz(250, 950)),
    ),
    "Funtington": AirfieldData(
        theater="Normandy",
        elevation=164,
        runway_length=5080,
        atc=AtcData(MHz(4, 250), MHz(119, 000), MHz(39, 400), MHz(251, 000)),
    ),
    "Tangmere": AirfieldData(
        theater="Normandy",
        elevation=47,
        runway_length=4296,
        atc=AtcData(MHz(4, 300), MHz(119, 100), MHz(39, 500), MHz(251, 100)),
    ),
    "Ford_AF": AirfieldData(
        theater="Normandy",
        elevation=29,
        runway_length=4296,
        atc=AtcData(MHz(4, 325), MHz(119, 150), MHz(39, 550), MHz(251, 150)),
    ),
    "Chailey": AirfieldData(
        theater="Normandy",
        elevation=134,
        runway_length=5080,
        atc=AtcData(MHz(4, 200), MHz(118, 900), MHz(39, 300), MHz(250, 900)),
    ),
    "Maupertus": AirfieldData(
        theater="Normandy",
        icao="A-15",
        elevation=441,
        runway_length=4666,
        atc=AtcData(MHz(4, 550), MHz(119, 600), MHz(40, 000), MHz(251, 600)),
    ),
    "Azeville": AirfieldData(
        theater="Normandy",
        icao="A-7",
        elevation=74,
        runway_length=3357,
        atc=AtcData(MHz(3, 875), MHz(118, 250), MHz(38, 650), MHz(250, 250)),
    ),
    "Biniville": AirfieldData(
        theater="Normandy",
        icao="A-24",
        elevation=106,
        runway_length=3283,
        atc=AtcData(MHz(3, 750), MHz(118, 000), MHz(38, 400), MHz(250, 000)),
    ),
    "Beuzeville": AirfieldData(
        theater="Normandy",
        icao="A-6",
        elevation=114,
        runway_length=3840,
        atc=AtcData(MHz(3, 850), MHz(118, 200), MHz(38, 600), MHz(250, 200)),
    ),
    "Picauville": AirfieldData(
        theater="Normandy",
        icao="A-8",
        elevation=72,
        runway_length=3840,
        atc=AtcData(MHz(3, 900), MHz(118, 300), MHz(38, 700), MHz(250, 300)),
    ),
    "Brucheville": AirfieldData(
        theater="Normandy",
        icao="A-16",
        elevation=45,
        runway_length=3413,
        atc=AtcData(MHz(4, 575), MHz(119, 650), MHz(40, 50), MHz(251, 650)),
    ),
    "Cretteville": AirfieldData(
        theater="Normandy",
        icao="A-14",
        elevation=95,
        runway_length=4594,
        atc=AtcData(MHz(4, 500), MHz(119, 500), MHz(39, 900), MHz(251, 500)),
    ),
    "Meautis": AirfieldData(
        theater="Normandy",
        icao="A-17",
        elevation=83,
        runway_length=3840,
        atc=AtcData(MHz(4, 600), MHz(119, 700), MHz(40, 100), MHz(251, 700)),
    ),
    "Lessay": AirfieldData(
        theater="Normandy",
        icao="A-20",
        elevation=65,
        runway_length=5080,
        atc=AtcData(MHz(4, 650), MHz(119, 800), MHz(40, 200), MHz(251, 800)),
    ),
    "Cardonville": AirfieldData(
        theater="Normandy",
        icao="A-3",
        elevation=101,
        runway_length=4541,
        atc=AtcData(MHz(3, 775), MHz(118, 50), MHz(38, 450), MHz(250, 50)),
    ),
    "Cricqueville-en-Bessin": AirfieldData(
        theater="Normandy",
        icao="A-2",
        elevation=81,
        runway_length=3459,
        atc=AtcData(MHz(4, 625), MHz(119, 750), MHz(40, 150), MHz(251, 750)),
    ),
    "Deux Jumeaux": AirfieldData(
        theater="Normandy",
        icao="A-4",
        elevation=123,
        runway_length=4628,
        atc=AtcData(MHz(3, 800), MHz(118, 100), MHz(38, 500), MHz(250, 100)),
    ),
    "Saint Pierre du Mont": AirfieldData(
        theater="Normandy",
        icao="A-1",
        elevation=103,
        runway_length=4737,
        atc=AtcData(MHz(4, 000), MHz(118, 500), MHz(38, 900), MHz(250, 500)),
    ),
    "Sainte-Laurent-sur-Mer": AirfieldData(
        theater="Normandy",
        icao="A-21",
        elevation=145,
        runway_length=4561,
        atc=AtcData(MHz(4, 675), MHz(119, 850), MHz(40, 250), MHz(251, 850)),
    ),
    "Longues-sur-Mer": AirfieldData(
        theater="Normandy",
        icao="B-11",
        elevation=225,
        runway_length=3155,
        atc=AtcData(MHz(3, 950), MHz(118, 400), MHz(38, 800), MHz(250, 400)),
    ),
    "Chippelle": AirfieldData(
        theater="Normandy",
        icao="A-5",
        elevation=124,
        runway_length=4643,
        atc=AtcData(MHz(3, 825), MHz(118, 150), MHz(38, 550), MHz(250, 150)),
    ),
    "Le Molay": AirfieldData(
        theater="Normandy",
        icao="A-9",
        elevation=104,
        runway_length=3840,
        atc=AtcData(MHz(3, 925), MHz(118, 350), MHz(38, 750), MHz(250, 350)),
    ),
    "Lignerolles": AirfieldData(
        theater="Normandy",
        icao="A-12",
        elevation=404,
        runway_length=3436,
        atc=AtcData(MHz(4, 275), MHz(119, 50), MHz(39, 450), MHz(251, 50)),
    ),
    "Sommervieu": AirfieldData(
        theater="Normandy",
        icao="B-8",
        elevation=186,
        runway_length=3840,
        atc=AtcData(MHz(4, 125), MHz(118, 750), MHz(39, 150), MHz(250, 750)),
    ),
    "Bazenville": AirfieldData(
        theater="Normandy",
        icao="B-2",
        elevation=199,
        runway_length=3800,
        atc=AtcData(MHz(4, 25), MHz(118, 550), MHz(38, 950), MHz(250, 550)),
    ),
    "Rucqueville": AirfieldData(
        theater="Normandy",
        icao="B-7",
        elevation=192,
        runway_length=4561,
        atc=AtcData(MHz(4, 100), MHz(118, 700), MHz(39, 100), MHz(250, 700)),
    ),
    "Lantheuil": AirfieldData(
        theater="Normandy",
        icao="B-9",
        elevation=174,
        runway_length=3597,
        atc=AtcData(MHz(4, 150), MHz(118, 800), MHz(39, 200), MHz(250, 800)),
    ),
    "Sainte-Croix-sur-Mer": AirfieldData(
        theater="Normandy",
        icao="B-3",
        elevation=160,
        runway_length=3840,
        atc=AtcData(MHz(4, 50), MHz(118, 600), MHz(39, 000), MHz(250, 600)),
    ),
    "Beny-sur-Mer": AirfieldData(
        theater="Normandy",
        icao="B-4",
        elevation=199,
        runway_length=3155,
        atc=AtcData(MHz(4, 75), MHz(118, 650), MHz(39, 50), MHz(250, 650)),
    ),
    "Carpiquet": AirfieldData(
        theater="Normandy",
        icao="B-17",
        elevation=187,
        runway_length=3799,
        atc=AtcData(MHz(3, 975), MHz(118, 450), MHz(38, 850), MHz(250, 450)),
    ),
    "Goulet": AirfieldData(
        theater="Normandy",
        elevation=616,
        runway_length=3283,
        atc=AtcData(MHz(4, 375), MHz(119, 250), MHz(39, 650), MHz(251, 250)),
    ),
    "Argentan": AirfieldData(
        theater="Normandy",
        elevation=639,
        runway_length=3283,
        atc=AtcData(MHz(4, 350), MHz(119, 200), MHz(39, 600), MHz(251, 200)),
    ),
    "Vrigny": AirfieldData(
        theater="Normandy",
        elevation=590,
        runway_length=3283,
        atc=AtcData(MHz(4, 475), MHz(119, 450), MHz(39, 850), MHz(251, 450)),
    ),
    "Hauterive": AirfieldData(
        theater="Normandy",
        elevation=476,
        runway_length=3283,
        atc=AtcData(MHz(4, 450), MHz(119, 400), MHz(39, 800), MHz(251, 400)),
    ),
    "Essay": AirfieldData(
        theater="Normandy",
        elevation=507,
        runway_length=3283,
        atc=AtcData(MHz(4, 425), MHz(119, 350), MHz(39, 750), MHz(251, 350)),
    ),
    "Barville": AirfieldData(
        theater="Normandy",
        elevation=462,
        runway_length=3493,
        atc=AtcData(MHz(4, 400), MHz(119, 300), MHz(39, 700), MHz(251, 300)),
    ),
    "Conches": AirfieldData(
        theater="Normandy",
        elevation=541,
        runway_length=4199,
        atc=AtcData(MHz(4, 525), MHz(119, 550), MHz(39, 950), MHz(251, 550)),
    ),
    "Evreux": AirfieldData(
        theater="Normandy",
        elevation=423,
        runway_length=4296,
        atc=AtcData(MHz(4, 175), MHz(118, 850), MHz(39, 250), MHz(250, 850)),
    ),
    # Channel Map
    "Detling": AirfieldData(
        theater="Channel",
        elevation=623,
        runway_length=3482,
        atc=AtcData(MHz(4, 50), MHz(118, 600), MHz(39, 0), MHz(250, 600)),
    ),
    "High Halden": AirfieldData(
        theater="Channel",
        elevation=104,
        runway_length=3296,
        atc=AtcData(MHz(3, 800), MHz(118, 100), MHz(38, 500), MHz(250, 100)),
    ),
    "Lympne": AirfieldData(
        theater="Channel",
        elevation=351,
        runway_length=3054,
        atc=AtcData(MHz(4, 25), MHz(118, 550), MHz(38, 950), MHz(250, 550)),
    ),
    "Hawkinge": AirfieldData(
        theater="Channel",
        elevation=524,
        runway_length=3013,
        atc=AtcData(MHz(4, 0), MHz(118, 500), MHz(38, 900), MHz(250, 500)),
    ),
    "Manston": AirfieldData(
        theater="Channel",
        elevation=160,
        runway_length=8626,
        atc=AtcData(MHz(3, 975), MHz(118, 250), MHz(38, 650), MHz(250, 250)),
    ),
    "Dunkirk Mardyck": AirfieldData(
        theater="Channel",
        elevation=16,
        runway_length=1737,
        atc=AtcData(MHz(3, 950), MHz(118, 450), MHz(38, 850), MHz(250, 450)),
    ),
    "Saint Omer Longuenesse": AirfieldData(
        theater="Channel",
        elevation=219,
        runway_length=1929,
        atc=AtcData(MHz(3, 925), MHz(118, 350), MHz(38, 750), MHz(250, 350)),
    ),
    "Merville Calonne": AirfieldData(
        theater="Channel",
        elevation=52,
        runway_length=7580,
        atc=AtcData(MHz(3, 900), MHz(118, 300), MHz(38, 700), MHz(250, 300)),
    ),
    "Abbeville Drucat": AirfieldData(
        theater="Channel",
        elevation=183,
        runway_length=4726,
        atc=AtcData(MHz(3, 875), MHz(118, 250), MHz(38, 650), MHz(250, 250)),
    ),
    "Eastchurch": AirfieldData(
        theater="Channel",
        elevation=30,
        runway_length=2983,
        atc=AtcData(MHz(3, 775), MHz(118, 50), MHz(38, 450), MHz(250, 50)),
    ),
    "Headcorn": AirfieldData(
        theater="Channel",
        elevation=114,
        runway_length=3680,
        atc=AtcData(MHz(3, 825), MHz(118, 150), MHz(38, 550), MHz(250, 150)),
    ),
    "Biggin Hill": AirfieldData(
        theater="Channel",
        elevation=552,
        runway_length=3953,
        atc=AtcData(MHz(3, 850), MHz(118, 200), MHz(38, 600), MHz(250, 200)),
    ),
}
