"""Extra airfield data that is not exposed by pydcs.

Remove once https://github.com/pydcs/dcs/issues/69 tracks getting the missing
data added to pydcs. Until then, missing data can be manually filled in here.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


RadioFrequency = str


@dataclass
class AtcData:
    hf: RadioFrequency
    vhf_fm: RadioFrequency
    vhf_am: RadioFrequency
    uhf: RadioFrequency


@dataclass
class AirfieldData:
    """Additional airfield data not included in pydcs."""

    #: ICAO airport code
    icao: Optional[str] = None

    #: Elevation (in ft).
    elevation: int = 0

    #: Runway length (in ft).
    runway_length: int = 0

    #: TACAN channel as a string, i.e. "74X".
    tacan: Optional[str] = None

    #: TACAN callsign
    tacan_callsign: Optional[str] = None

    #: VOR channel as a string, i.e. "114.90 (MA)".
    vor: Optional[str] = None

    #: RSBN channel as a string, i.e. "ch 28 (KW)".
    rsbn: Optional[str] = None

    #: Radio channels used by the airfield's ATC.
    atc: AtcData = AtcData("", "", "", "")

    #: Dict of runway heading -> ILS frequency.
    ils: Dict[str, RadioFrequency] = field(default_factory=dict)

    #: Dict of runway heading -> PRMG info, i.e "ch 26 (KW)"
    prmg: Dict[str, str] = field(default_factory=dict)

    #: Dict of runway heading -> outer ndb, i.e "408.00 (KW)"
    outer_ndb: Dict[str, str] = field(default_factory=dict)

    #: Dict of runway heading -> inner ndb, i.e "803.00 (K)
    inner_ndb: Dict[str, str] = field(default_factory=dict)

    def ils_freq(self, runway: str) -> Optional[RadioFrequency]:
        return self.ils.get(runway)


# TODO: Add more airfields.
AIRFIELD_DATA = {

    # TODO : CAUCASUS MAP
    "Batumi": AirfieldData(
        "UGSB",
        32, 6792,
        "16X", "BTM",
        "", "",
        AtcData("4.250", "131.000", "40.400", "260.000"),
        {"13": "110.30 (ILU)"},
        {},
        {},
        {}
    ),

    "Kobuleti": AirfieldData(
        "UG5X",
        59, 7406,
        "67X", "KBL",
        "", "",
        AtcData("4.350", "133.000", "40.800", "262.000"),
        {"7": "111.50 (IKB)"},
        {},
        {"7": "870.00 (KT)"},
        {"7": "490.00 (T)"},
    ),

    "Senaki-Kolkhi": AirfieldData(
        "UGKS",
        43, 7256,
        "31X", "TSK",
        "", "",
        AtcData("4.300", "132.000", "40.600", "261.000"),
        {"9": "108.90 (ITS)"},
        {},
        {"9": "335.00 (BI)"},
        {"9": "688.00 (I)"},
    ),

    "Kutaisi": AirfieldData(
        "UGKO",
        147, 7937,
        "44X", "KTS",
        "113.60 (KT)", "",
        AtcData("4.400", "134.000", "41.000", "263.000"),
        {"8": "109.75 (IKS)"},
        {},
        {},
        {},
    ),

    "Sukhumi-Babushara": AirfieldData(
        "UGSS",
        43, 11217,
        "", "",
        "", "",
        AtcData("4.150", "129.000", "40.000", "258.000"),
        {},
        {},
        {"30": "489.00 (AV)"},
        {"30": "995.00 (A)"},
    ),

    "Gudauta": AirfieldData(
        "UG23",
        68, 7839,
        "", "",
        "", "",
        AtcData("4.200", "120.000", "40.200", "259.000"),
        {},
        {},
        {},
        {},
    ),

    "Sochi-Adler": AirfieldData(
        "URSS",
        98, 9686,
        "", "",
        "", "",
        AtcData("4.050", "127.000", "39.600", "256.000"),
        {"6": "111.10 (ISO)"},
        {},
        {},
        {},
    ),

    "Gelendzhik": AirfieldData(
        "URKG",
        72, 5452,
        "", "",
        "114.30 (GN)", "",
        AtcData("4.000", "126.000", "39.400", "255.000"),
        {},
        {},
        {},
        {},
    ),

    "Novorossiysk": AirfieldData(
        "URKN",
        131, 5639,
        "", "",
        "", "",
        AtcData("3.850", "123.000", "38.800", "252.000"),
        {},
        {},
        {},
        {},
    ),

    "Anapa-Vityazevo": AirfieldData(
        "URKA",
        141, 8623,
        "", "",
        "", "",
        AtcData("3.750", "121.000", "38.400", "250.000"),
        {},
        {},
        {"22": "443.00 (AP)", "4": "443.00 (AN)"},
        {"22": "215.00 (P)", "4": "215.00 (N)"},
    ),

    "Krymsk": AirfieldData(
        "URKW",
        65, 6733,
        "", "",
        "", "ch 28 (KW)",
        AtcData("3.900", "124.000", "39.000", "253.000"),
        {},
        {"4": "ch 26 (OX)", "22": "ch 26 (KW)"},
        {"4": "408.00 (OX)", "22": "408.00 (KW)"},
        {"4": "803.00 (O)", "22": "803.00 (K)"},
    ),

    "Krasnodar-Center": AirfieldData(
        "URKL",
        98, 7659,
        "", "",
        "", "ch 40 (MB)",
        AtcData("3.800", "122.000", "38.600", "251.000"),
        {},
        {"9": "ch 38 (MB)"},
        {"9": "625.00 (MB)", "27": "625.00 (OC)"},
        {"9": "303.00 (M)", "27": "303.00 (C)"},
    ),

    "Krasnodar-Pashkovsky": AirfieldData(
        "URKK",
        111, 9738,
        "", "",
        "115.80 (KN)", "",
        AtcData("4.100", "128.000", "39.800", "257.000"),
        {},
        {},
        {"23": "493.00 (LD)", "5": "493.00 (KR)"},
        {"23": "240.00 (L)", "5": "240.00 (K)"},
    ),

    "Maykop-Khanskaya": AirfieldData(
        "URKH",
        590, 10195,
        "", "",
        "", "ch 34 (DG)",
        AtcData("3.950", "125.000", "39.200", "254.000"),
        {},
        {"4": "ch 36 (DG)"},
        {"4": "289.00 (DG)", "22": "289.00 (RK)"},
        {"4": "591.00 (D)", "22": "591.00 (R)"},
    ),

    "Mineralnye Vody": AirfieldData(
        "URMM",
        1049, 12316,
        "", "",
        "117.10 (MN)", "",
        AtcData("4.450", "135.000", "41.200", "264.000"),
        {"30": "109.30 (IMW)", "12": "111.70 (IMD)"},
        {},
        {"30": "583.00 (NR)", "12": "583.00 (MD)"},
        {"30": "283.00 (N)", "12": "283.00 (D)"},
    ),

    "Nalchik": AirfieldData(
        "URMN",
        1410, 7082,
        "", "",
        "", "",
        AtcData("4.500", "136.000", "41.400", "265.000"),
        {"24": "110.50 (INL)"},
        {},
        {"24": "718.00 (NL)"},
        {"24": "350.00 (N)"},
    ),

    "Mozdok": AirfieldData(
        "XRMF",
        507, 7734,
        "", "",
        "", "ch 20 (MZ)",
        AtcData("4.550", "137.000", "41.600", "266.000"),
        {},
        {"26": "ch 22 (MZ)", "8": "ch 22 (MZ)"},
        {"26": "525.00 (RM)", "8": "525.00 (DO)"},
        {"26": "1.06 (R)", "8": "1.06 (D)"}
    ),

    "Beslan": AirfieldData(
        "URMO",
        1719, 9327,
        "", "",
        "", "",
        AtcData("4.750", "141.000", "42.400", "270.000"),
        {"10": "110.50 (ICH)"},
        {},
        {"10": "1.05 (CX)"},
        {"10": "250.00 (C)"}
    ),

    "Tbilisi-Lochini": AirfieldData(
        "UGTB",
        1573, 7692,
        "25X", "GTB",
        "113.70 (INA)", "",
        AtcData("4.600", "138.000", "41.800", "267.000"),
        {"13": "110.30 (INA)", "30": "108.90 (INA)"},
        {},
        {"13": "342.00 (BP)", "30": "211.00 (NA)"},
        {"13": "923.00 (B)", "30": "435.00 (N)"},
    ),

    "Soganlung": AirfieldData(
        "UG24",
        1474, 7871,
        "25X", "GTB",
        "113.70 (INA)", "",
        AtcData("4.650", "139.000", "42.000", "268.000"),
        {},
        {},
        {},
        {},
    ),

    "Vaziani": AirfieldData(
        "UG27",
        1523, 7842,
        "22X", "VAS",
        "", "",
        AtcData("4.700", "140.000", "42.200", "269.000"),
        {"13": "108.75 (IVZ)", "31": "108.75 (IVZ)"},
        {},
        {},
        {},
    ),

    # TODO : PERSIAN GULF MAP
    # TODO : SYRIA MAP
    # "Incirlik": AirfieldData(
    #     AtcData("3.85", "38.6", "129.4", "360.1"),
    #     "21X",
    #     {"050": "109.3", "230": "111.7"}
    # ),
    # TODO : NEVADA MAP
    "Mina Airport 3Q0": AirfieldData(
        "",
        4562, 4222,
        "", "",
        "", "",
        AtcData("", "", "", ""),
        {},
        {},
        {},
        {},
    ),

    "Tonopah Airport": AirfieldData(
        "KTPH",
        5394, 6715,
        "", "",
        "", "",
        AtcData("", "", "", ""),
        {},
        {},
        {},
        {},
    ),

    "Tonopah Test Range Airfield": AirfieldData(
        "KTNX",
        5534, 11633,
        "77X", "TQQ",
        "113.00 (TQQ)", "",
        AtcData("3.800", "124.750", "38.500", "257.950"),
        {"32": "111.70 (I-UVV)", "14": "108.30 (I-RVP)"},
        {},
        {},
        {},
    ),

    "Beatty Airport": AirfieldData(
        "KBTY",
        3173, 5380,
        "", "",
        "", "",
        AtcData("", "", "", ""),
        {},
        {},
        {},
        {},
    ),

    "Pahute Mesa Airstrip": AirfieldData(
        "",
        5056, 5420,
        "", "",
        "", "",
        AtcData("", "", "", ""),
        {},
        {},
        {},
        {},
    ),

    "Groom Lake AFB": AirfieldData(
        "KXTA",
        4494, 11008,
        "18X", "GRL",
        "", "",
        AtcData("3.850", "118.000", "38.600", "250.050"),
        {"32": "109.30 (GLRI)"},
        {},
        {},
        {},
    ),

    "Lincoln County": AirfieldData(
        "",
        4815, 4408,
        "", "",
        "", "",
        AtcData("", "", "", ""),
        {},
        {},
        {},
        {},
    ),

    "Mesquite": AirfieldData(
        "67L",
        1858, 4937,
        "", "",
        "", "",
        AtcData("", "", "", ""),
        {},
        {},
        {},
        {},
    ),

    "Creech AFB": AirfieldData(
        "KINS",
        3126, 6100,
        "87X", "INS",
        "", "",
        AtcData("3.825", "118.300", "38.550", "360.600"),
        {"8": "108.70 (ICRR)"},
        {},
        {},
        {},
    ),

    "Echo Bay": AirfieldData(
        "OL9",
        3126, 6100,
        "87X", "INS",
        "", "",
        AtcData("3.825", "118.300", "38.550", "360.600"),
        {},
        {},
        {},
        {},
    ),

    "Nellis AFB": AirfieldData(
        "KLSV",
        1841, 9454,
        "12X", "LSV",
        "", "",
        AtcData("3.900", "132.550", "38.700", "327.000"),
        {"21": "109.10 (IDIQ)"},
        {},
        {},
        {},
    ),

    "North Las Vegas": AirfieldData(
        "KVGT",
        2228, 4734,
        "", "",
        "", "",
        AtcData("3.775", "125.700", "38.450", "360.750"),
        {},
        {},
        {},
        {},
    ),

    "McCarran International Airport": AirfieldData(
        "KLAS",
        2169, 10377,
        "116X", "LAS",
        "116.90 (LAS)", "",
        AtcData("3.875", "119.900", "38.650", "257.800"),
        {"25": "110.30 (I-LAS)"},
        {},
        {},
        {},
    ),

    "Henderson Executive Airport": AirfieldData(
        "KHND",
        2491, 5999,
        "", "",
        "", "",
        AtcData("3.925", "125.100", "38.750", "250.100"),
        {},
        {},
        {},
        {},
    ),

    "Boulder City Airport": AirfieldData(
        "KBVU",
        2121, 4612,
        "", "",
        "", "",
        AtcData("", "", "", ""),
        {},
        {},
        {},
        {},
    ),

    "Jean Airport": AirfieldData(
        "",
        2824, 4053,
        "", "",
        "", "",
        AtcData("", "", "", ""),
        {},
        {},
        {},
        {},
    ),

    "Laughlin Airport": AirfieldData(
        "KIFP",
        656, 7139,
        "", "",
        "", "",
        AtcData("3.750", "123.900", "38.400", "250.000"),
        {},
        {},
        {},
        {},
    ),

    # TODO : NORMANDY MAP

    # Channel Map
    "Detling": AirfieldData(
        "",
        623, 2557,
        "", "",
        "", "",
        AtcData("3.950", "118.400", "38.800", "250.400"),
        {},
        {},
        {},
        {},
    ),

    "High Halden": AirfieldData(
        "",
        104, 3296,
        "", "",
        "", "",
        AtcData("3.750", "118.800", "38.400", "250.000"),
        {},
        {},
        {},
        {},
    ),

    "Lympne": AirfieldData(
        "",
        351, 2548,
        "", "",
        "", "",
        AtcData("3.925", "118.350", "38.750", "250.350"),
        {},
        {},
        {},
        {},
    ),

    "Hawkinge": AirfieldData(
        "",
        524, 3013,
        "", "",
        "", "",
        AtcData("3.900", "118.300", "38.700", "250.300"),
        {},
        {},
        {},
        {},
    ),

    "Manston": AirfieldData(
        "",
        160, 8626,
        "", "",
        "", "",
        AtcData("3.875", "118.250", "38.650", "250.250"),
        {},
        {},
        {},
        {},
    ),

    "Dunkirk Mardyck": AirfieldData(
        "",
        16, 1737,
        "", "",
        "", "",
        AtcData("3.850", "118.200", "38.600", "250.200"),
        {},
        {},
        {},
        {},
    ),

    "Saint Omer Longuenesse": AirfieldData(
        "",
        219, 1929,
        "", "",
        "", "",
        AtcData("3.825", "118.150", "38.550" "250.150"),
        {},
        {},
        {},
        {},
    ),

    "Merville Calonne": AirfieldData(
        "",
        52, 7580,
        "", "",
        "", "",
        AtcData("3.800", "118.100", "38.500", "250.100"),
        {},
        {},
        {},
        {},
    ),

    "Abbeville Drucat": AirfieldData(
        "",
        183, 4726,
        "", "",
        "", "",
        AtcData("3.775", "118.050", "38.450", "250.050"),
        {},
        {},
        {},
        {},
    )

}
