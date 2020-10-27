import random

from dcs.vehicles import AirDefence
from game import db
from gen.sam.group_generator import GroupGenerator


class GenericSamGroupGenerator(GroupGenerator):
    """
    This is the base for all SAM group generators
    """
    
    def __init__(self, game, ground_object, faction):
        self.faction = faction
        super(GenericSamGroupGenerator, self).__init__(game, ground_object)

    @property
    def groupNamePrefix(self) -> str:
        # prefix the SAM site for use with the Skynet IADS plugin
        if self.faction == self.game.player_name: # this is the player faction
            return "BLUE SAM " 
        else:
            return "RED SAM " 
