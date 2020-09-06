"""Extra airfield data that is not exposed by pydcs.

Remove once https://github.com/pydcs/dcs/issues/69 tracks getting the missing
data added to pydcs. Until then, missing data can be manually filled in here.
"""
from dataclasses import dataclass, field
import logging
from typing import Dict, Optional, Tuple

from dcs.terrain.terrain import Airport
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
            "13": ("ILU", MHz(110, 30)),
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
            "07": ("IKB", MHz(111, 50)),
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
            "09": ("ITS", MHz(108, 90)),
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
            "08": ("IKS", MHz(109, 75)),
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
            "06": ("ISO", MHz(111, 10)),
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
            "22": ("AP", MHz(443, 0)), "4": "443.00 (AN)"
        },
        inner_ndb={
            "22": ("P", MHz(215, 0)), "4": "215.00 (N)"
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
            "30": ("IMW", MHz(109, 30)),
            "12": ("IMD", MHz(111, 70)),
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
            "24": ("INL", MHz(110, 50)),
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
        }
    ),

    "Beslan": AirfieldData(
        theater="Caucasus",
        icao="URMO",
        elevation=1719,
        runway_length=9327,
        atc=AtcData(MHz(4, 750), MHz(141, 0), MHz(42, 400), MHz(270, 0)),
        ils={
            "10": ("ICH", MHz(110, 50)),
        },
        outer_ndb={
            "10": ("CX", MHz(1, 5)),
        },
        inner_ndb={
            "10": ("C", MHz(250, 0)),
        }
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
            "13": ("INA", MHz(110, 30)),
            "30": ("INA", MHz(108, 90)),
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
            "13": ("IVZ", MHz(108, 75)),
            "31": ("IVZ", MHz(108, 75)),
        },
    ),

    # TODO : PERSIAN GULF MAP
    # TODO : SYRIA MAP

    "Incirlik": AirfieldData(
        theater="Syria",
        icao="LTAG",
        elevation=156,
        runway_length=9662,
        tacan=TacanChannel(21, TacanBand.X),
        tacan_callsign="DAN",
        vor=("DAN", MHz(108, 400)),
        atc=AtcData(MHz(3, 850), MHz(38, 600), MHz(129, 400), MHz(360, 100)),
        ils={
            "50": ("IDAN", MHz(109, 300)),
            "23": ("DANM", MHz(111, 700)),
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
            "32": ("I-UVV", MHz(111, 70)),
            "14": ("I-RVP", MHz(108, 30)),
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
            "32": ("GLRI", MHz(109, 30)),
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
            "8": ("ICRR", MHz(108, 70)),
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
            "21": ("IDIQ", MHz(109, 10)),
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
            "25": ("I-LAS", MHz(110, 30)),
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

    # TODO : NORMANDY MAP

    # Channel Map
    "Detling": AirfieldData(
        theater="Channel",
        elevation=623,
        runway_length=2557,
        atc=AtcData(MHz(3, 950), MHz(118, 400), MHz(38, 800), MHz(250, 400)),
    ),

    "High Halden": AirfieldData(
        theater="Channel",
        elevation=104,
        runway_length=3296,
        atc=AtcData(MHz(3, 750), MHz(118, 800), MHz(38, 400), MHz(250, 0)),
    ),

    "Lympne": AirfieldData(
        theater="Channel",
        elevation=351,
        runway_length=2548,
        atc=AtcData(MHz(3, 925), MHz(118, 350), MHz(38, 750), MHz(250, 350)),
    ),

    "Hawkinge": AirfieldData(
        theater="Channel",
        elevation=524,
        runway_length=3013,
        atc=AtcData(MHz(3, 900), MHz(118, 300), MHz(38, 700), MHz(250, 300)),
    ),

    "Manston": AirfieldData(
        theater="Channel",
        elevation=160,
        runway_length=8626,
        atc=AtcData(MHz(3, 875), MHz(118, 250), MHz(38, 650), MHz(250, 250)),
    ),

    "Dunkirk Mardyck": AirfieldData(
        theater="Channel",
        elevation=16,
        runway_length=1737,
        atc=AtcData(MHz(3, 850), MHz(118, 200), MHz(38, 600), MHz(250, 200)),
    ),

    "Saint Omer Longuenesse": AirfieldData(
        theater="Channel",
        elevation=219,
        runway_length=1929,
        atc=AtcData(MHz(3, 825), MHz(118, 150), MHz(38, 550), MHz(250, 150)),
    ),

    "Merville Calonne": AirfieldData(
        theater="Channel",
        elevation=52,
        runway_length=7580,
        atc=AtcData(MHz(3, 800), MHz(118, 100), MHz(38, 500), MHz(250, 100)),
    ),

    "Abbeville Drucat": AirfieldData(
        theater="Channel",
        elevation=183,
        runway_length=4726,
        atc=AtcData(MHz(3, 775), MHz(118, 50), MHz(38, 450), MHz(250, 50)),
    ),
}


@dataclass(frozen=True)
class RunwayData:
    airfield_name: str
    runway_name: str
    atc: Optional[RadioFrequency] = None
    tacan: Optional[TacanChannel] = None
    tacan_callsign: Optional[str] = None
    ils: Optional[RadioFrequency] = None
    icls: Optional[int] = None

    @classmethod
    def for_airfield(cls, airport: Airport, runway: str) -> "RunwayData":
        """Creates RunwayData for the given runway of an airfield.

        Args:
            airport: The airfield the runway belongs to.
            runway: Identifier of the runway to use. e.g. "03" or "20L".
        """
        atc: Optional[RadioFrequency] = None
        tacan: Optional[TacanChannel] = None
        ils: Optional[RadioFrequency] = None
        try:
            airfield = AIRFIELD_DATA[airport.name]
            atc = airfield.atc.uhf
            tacan = airfield.tacan
            tacan = airfield.tacan_callsign
            ils = airfield.ils_freq(runway)
        except KeyError:
            logging.warning(f"No airfield data for {airport.name}")
        return cls(
            airport.name,
            runway,
            atc,
            tacan,
            ils
        )
