"""Unit conversions."""


def meters_to_feet(meters: float) -> float:
    """Converts meters to feet."""
    return meters * 3.28084

def inches_hg_to_mm_hg(inches_hg: float) -> float:
    """Converts inches mercury to millimeters mercury."""
    return inches_hg * 25.400002776728

def inches_hg_to_hpa(inches_hg: float) -> float:
    """Converts inches mercury to hectopascal."""
    return inches_hg * 33.86389