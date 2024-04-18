"""Support for working with DCS group callsigns."""
import logging
import re
from typing import Any

from dcs.unitgroup import FlyingGroup
from dcs.flyingunit import FlyingUnit


def callsign_for_support_unit(group: FlyingGroup[Any]) -> str:
    # Either something like Overlord11 for Western AWACS, or else just a number.
    # Convert to either "Overlord" or "Flight 123".
    lead = group.units[0]
    raw_callsign = lead.callsign_as_str()
    try:
        return f"Flight {int(raw_callsign)}"
    except ValueError:
        return raw_callsign.rstrip("1234567890")


def create_group_callsign_from_unit(lead: FlyingUnit) -> str:
    raw_callsign = lead.callsign_as_str()
    if not lead.callsign_is_western:
        # Callsigns for non-Western countries are just a number per flight,
        # similar to tail numbers.
        return f"Flight {raw_callsign}"

    # Callsign from pydcs is in the format `<name><group ID><unit ID>`,
    # where unit ID is guaranteed to be a single digit but the group ID may
    # be more.
    match = re.search(r"^(\D+)(\d+)(\d)$", raw_callsign)
    if match is None:
        logging.error(f"Could not parse unit callsign: {raw_callsign}")
        return f"Flight {raw_callsign}"
    return f"{match.group(1)} {match.group(2)}"
