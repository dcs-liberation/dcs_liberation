def meter_to_feet(value_in_meter: float) -> int:
    return int(3.28084 * value_in_meter)


def feet_to_meter(value_in_feet: float) -> int:
    return int(value_in_feet / 3.28084)


def meter_to_nm(value_in_meter: float) -> int:
    return int(value_in_meter / 1852)


def nm_to_meter(value_in_nm: float) -> int:
    return int(value_in_nm * 1852)


def knots_to_kph(knots: float) -> int:
    return int(knots * 1.852)

def mps_to_knots(mps: float) -> int:
    """Converts Meters Per Second To Knots

    :arg mps Meters Per Second
    """
    return int(mps * 1.943)