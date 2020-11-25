def meter_to_feet(value_in_meter: float) -> int:
    """Converts meters to feets

    :arg value_in_meter Value in meters
    """
    return int(3.28084 * value_in_meter)


def feet_to_meter(value_in_feet: float) -> int:
    """Converts feets to meters

    :arg value_in_feet Value in feets
    """
    return int(value_in_feet / 3.28084)


def meter_to_nm(value_in_meter: float) -> int:
    """Converts meters to nautic miles

    :arg value_in_meter Value in meters
    """
    return int(value_in_meter / 1852)


def nm_to_meter(value_in_nm: float) -> int:
    """Converts nautic miles to meters

    :arg value_in_nm Value in nautic miles
    """
    return int(value_in_nm * 1852)


def knots_to_kph(value_in_knots: float) -> int:
    """Converts Knots to Kilometer Per Hour

    :arg value_in_knots Knots 
    """
    return int(value_in_knots * 1.852)

def mps_to_knots(value_in_mps: float) -> int:
    """Converts Meters Per Second To Knots

    :arg value_in_mps Meters Per Second
    """
    return int(value_in_mps * 1.943)