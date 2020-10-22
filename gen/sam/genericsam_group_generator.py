import random

from dcs.vehicles import AirDefence
from game import db
from gen.sam.group_generator import GroupGenerator


class GenericSamGroupGenerator(GroupGenerator):
    """
    This is the base for all SAM group generators
    """

    def getGroupNamePrefix(self, faction):
        if not faction:
            return ""

        # prefix the SAM site for use with the Skynet IADS plugin
        prefix = "BLUE SAM " 
        if db.FACTIONS[faction]["side"] == "red":
            prefix = "RED SAM " 
        return prefix        
