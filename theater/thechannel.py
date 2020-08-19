from dcs.terrain import thechannel

from .conflicttheater import *
from .landmap import *


class Dunkirk(ConflictTheater):
    terrain = dcs.terrain.TheChannel()
    overview_image = "thechannel.gif"
    reference_points = {(thechannel.Abbeville_Drucat.position.x, thechannel.Abbeville_Drucat.position.y): (2400, 4100),
                        (thechannel.Detling.position.x, thechannel.Detling.position.y): (1100, 2000)}
    landmap = load_landmap("resources\\channellandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (10, 17),
        "dusk": (17, 18),
        "night": (0, 5),
    }

    def __init__(self):
        super(Dunkirk, self).__init__()

        self.abeville = ControlPoint.from_airport(thechannel.Abbeville_Drucat, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        #self.detling = ControlPoint.from_airport(thechannel.Detling, LAND, SIZE_SMALL, IMPORTANCE_LOW)

        self.stomer = ControlPoint.from_airport(thechannel.Saint_Omer_Longuenesse, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.dunkirk = ControlPoint.from_airport(thechannel.Dunkirk_Mardyck, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.hawkinge = ControlPoint.from_airport(thechannel.Hawkinge, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        #self.highhalden = ControlPoint.from_airport(thechannel.High_Halden, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.lympne = ControlPoint.from_airport(thechannel.Lympne, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.manston = ControlPoint.from_airport(thechannel.Manston, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.merville = ControlPoint.from_airport(thechannel.Merville_Calonne, LAND, SIZE_SMALL, IMPORTANCE_LOW)


        # England
        self.add_controlpoint(self.hawkinge, connected_to=[self.lympne, self.manston])
        self.add_controlpoint(self.lympne, connected_to=[self.hawkinge])
        self.add_controlpoint(self.manston, connected_to=[self.hawkinge])

        # France
        self.add_controlpoint(self.dunkirk, connected_to=[self.stomer])
        self.add_controlpoint(self.stomer, connected_to=[self.dunkirk, self.merville, self.abeville])
        self.add_controlpoint(self.merville, connected_to=[self.stomer])
        self.add_controlpoint(self.abeville, connected_to=[self.stomer])

        #self.detling.captured = True
        self.hawkinge.captured = True
        self.dunkirk.captured = True
        #self.highhalden.captured = True
        self.lympne.captured = True
        self.manston.captured = True

        self.manston.captured_invert = True
        self.dunkirk.captured_invert = True
        self.stomer.captured_invert = True
        self.merville.captured_invert = True
        self.abeville.captured_invert = True


class BattleOfBritain(ConflictTheater):
    terrain = dcs.terrain.TheChannel()
    overview_image = "thechannel.gif"
    reference_points = {(thechannel.Abbeville_Drucat.position.x, thechannel.Abbeville_Drucat.position.y): (2400, 4100),
                        (thechannel.Detling.position.x, thechannel.Detling.position.y): (1100, 2000)}
    landmap = load_landmap("resources\\channellandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (10, 17),
        "dusk": (17, 18),
        "night": (0, 5),
    }

    def __init__(self):
        super(BattleOfBritain, self).__init__()

        self.abeville = ControlPoint.from_airport(thechannel.Abbeville_Drucat, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        #self.detling = ControlPoint.from_airport(thechannel.Detling, LAND, SIZE_SMALL, IMPORTANCE_LOW)

        self.stomer = ControlPoint.from_airport(thechannel.Saint_Omer_Longuenesse, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.dunkirk = ControlPoint.from_airport(thechannel.Dunkirk_Mardyck, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.hawkinge = ControlPoint.from_airport(thechannel.Hawkinge, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.highhalden = ControlPoint.from_airport(thechannel.High_Halden, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.lympne = ControlPoint.from_airport(thechannel.Lympne, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.manston = ControlPoint.from_airport(thechannel.Manston, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.merville = ControlPoint.from_airport(thechannel.Merville_Calonne, LAND, SIZE_SMALL, IMPORTANCE_LOW)

        # England
        self.add_controlpoint(self.hawkinge, connected_to=[self.lympne, self.manston])
        self.add_controlpoint(self.lympne, connected_to=[self.hawkinge, self.highhalden])
        self.add_controlpoint(self.manston, connected_to=[self.hawkinge])
        self.add_controlpoint(self.highhalden, connected_to=[self.lympne])

        # France
        self.add_controlpoint(self.dunkirk, connected_to=[self.stomer])
        self.add_controlpoint(self.stomer, connected_to=[self.dunkirk, self.merville, self.abeville])
        self.add_controlpoint(self.merville, connected_to=[self.stomer])
        self.add_controlpoint(self.abeville, connected_to=[self.stomer])

        #self.detling.captured = True
        self.hawkinge.captured = True
        #self.dunkirk.captured = True
        self.highhalden.captured = True
        self.lympne.captured = True
        self.manston.captured = True

        self.dunkirk.captured_invert = True
        self.stomer.captured_invert = True
        self.merville.captured_invert = True
        self.abeville.captured_invert = True
