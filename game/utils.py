def meter_to_feet(value_in_meter: float) -> int:
    return int(3.28084 * value_in_meter)


def feet_to_meter(value_in_feet: float) -> int:
    return int(value_in_feet / 3.28084)


def meter_to_nm(value_in_meter: float) -> int:
    return int(value_in_meter / 1852)


def nm_to_meter(value_in_nm: float) -> int:
    return int(value_in_nm * 1852)
