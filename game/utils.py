def meter_to_feet(value_in_meter):
    return int(3.28084 * value_in_meter)


def feet_to_meter(value_in_feet):
    return int(float(value_in_feet)/3.048)


def meter_to_nm(value_in_meter):
    return int(float(value_in_meter)*0.000539957)


def nm_to_meter(value_in_nm):
    return int(float(value_in_nm)*1852)