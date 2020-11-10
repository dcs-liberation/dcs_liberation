from dataclasses import dataclass, field

from typing import List

from gen.locations.preset_locations import PresetLocation


@dataclass
class PresetControlPointLocations:
    """A repository of preset locations for a given control point"""

    # List of possible ashore locations to generate objects (Represented in miz file by an APC_AAV_7)
    ashore_locations: List[PresetLocation] = field(default_factory=list)

    # List of possible offshore locations to generate ship groups (Represented in miz file by an Oliver Hazard Perry)
    offshore_locations: List[PresetLocation] = field(default_factory=list)

    # Possible antiship missiles sites locations (Represented in miz file by Iranian Silkworm missiles)
    antiship_locations: List[PresetLocation] = field(default_factory=list)

    # List of possible powerplants locations (Represented in miz file by static Workshop A object, USA)
    powerplant_locations: List[PresetLocation] = field(default_factory=list)
