from game.utils import nm_to_meter, feet_to_meter

MODERN_DOCTRINE = {

    "GENERATORS": {
        "CAS": True,
        "CAP": True,
        "SEAD": True,
        "STRIKE": True,
        "ANTISHIP": True,
    },

    "STRIKE_MAX_RANGE": 1500000,
    "SEAD_MAX_RANGE": 1500000,

    "CAP_EVERY_X_MINUTES": 20,
    "CAS_EVERY_X_MINUTES": 30,
    "SEAD_EVERY_X_MINUTES": 40,
    "STRIKE_EVERY_X_MINUTES": 40,

    "INGRESS_EGRESS_DISTANCE": nm_to_meter(45),
    "INGRESS_ALT": feet_to_meter(20000),
    "EGRESS_ALT": feet_to_meter(20000),
    "PATROL_ALT_RANGE": (feet_to_meter(15000), feet_to_meter(33000)),
    "PATTERN_ALTITUDE": feet_to_meter(5000),

    "CAP_PATTERN_LENGTH": (nm_to_meter(15), nm_to_meter(40)),
    "FRONTLINE_CAP_DISTANCE_FROM_FRONTLINE": (nm_to_meter(6), nm_to_meter(15)),
    "CAP_DISTANCE_FROM_CP": (nm_to_meter(10), nm_to_meter(40)),

    "MAX_NUMBER_OF_INTERCEPTION_GROUP": 3,
}

COLDWAR_DOCTRINE = {

    "GENERATORS": {
        "CAS": True,
        "CAP": True,
        "SEAD": True,
        "STRIKE": True,
        "ANTISHIP": True,
    },

    "STRIKE_MAX_RANGE": 1500000,
    "SEAD_MAX_RANGE": 1500000,

    "CAP_EVERY_X_MINUTES": 20,
    "CAS_EVERY_X_MINUTES": 30,
    "SEAD_EVERY_X_MINUTES": 40,
    "STRIKE_EVERY_X_MINUTES": 40,

    "INGRESS_EGRESS_DISTANCE": nm_to_meter(30),
    "INGRESS_ALT": feet_to_meter(18000),
    "EGRESS_ALT": feet_to_meter(18000),
    "PATROL_ALT_RANGE": (feet_to_meter(10000), feet_to_meter(24000)),
    "PATTERN_ALTITUDE": feet_to_meter(5000),

    "CAP_PATTERN_LENGTH": (nm_to_meter(12), nm_to_meter(24)),
    "FRONTLINE_CAP_DISTANCE_FROM_FRONTLINE": (nm_to_meter(2), nm_to_meter(8)),
    "CAP_DISTANCE_FROM_CP": (nm_to_meter(8), nm_to_meter(25)),

    "MAX_NUMBER_OF_INTERCEPTION_GROUP": 3,
}

WWII_DOCTRINE = {

    "GENERATORS": {
        "CAS": True,
        "CAP": True,
        "SEAD": False,
        "STRIKE": True,
        "ANTISHIP": True,
    },

    "STRIKE_MAX_RANGE": 1500000,
    "SEAD_MAX_RANGE": 1500000,

    "CAP_EVERY_X_MINUTES": 20,
    "CAS_EVERY_X_MINUTES": 30,
    "SEAD_EVERY_X_MINUTES": 40,
    "STRIKE_EVERY_X_MINUTES": 40,

    "INGRESS_EGRESS_DISTANCE": nm_to_meter(7),
    "INGRESS_ALT": feet_to_meter(8000),
    "EGRESS_ALT": feet_to_meter(8000),
    "PATROL_ALT_RANGE": (feet_to_meter(4000), feet_to_meter(15000)),
    "PATTERN_ALTITUDE": feet_to_meter(5000),

    "CAP_PATTERN_LENGTH": (nm_to_meter(8), nm_to_meter(18)),
    "FRONTLINE_CAP_DISTANCE_FROM_FRONTLINE": (nm_to_meter(1), nm_to_meter(6)),
    "CAP_DISTANCE_FROM_CP": (nm_to_meter(5), nm_to_meter(15)),

    "MAX_NUMBER_OF_INTERCEPTION_GROUP": 3,

}
