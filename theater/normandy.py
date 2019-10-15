from dcs.terrain import normandy

from .conflicttheater import *
from .landmap import *


class NormandyTheater(ConflictTheater):
    terrain = dcs.terrain.Normandy()
    overview_image = "normandy.gif"
    reference_points = {(normandy.Needs_Oar_Point.position.x, normandy.Needs_Oar_Point.position.y): (-170, -1000),
                        (normandy.Evreux.position.x, normandy.Evreux.position.y): (2020, 500)}
    landmap = load_landmap("resources\\normandylandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (10, 17),
        "dusk": (17, 18),
        "night": (0, 5),
    }

    st_pierre = ControlPoint.from_airport(normandy.Saint_Pierre_du_Mont, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)
    maupertus = ControlPoint.from_airport(normandy.Maupertus, LAND, SIZE_SMALL, IMPORTANCE_LOW)
    azeville = ControlPoint.from_airport(normandy.Azeville, LAND, SIZE_SMALL, IMPORTANCE_LOW)
    lessay = ControlPoint.from_airport(normandy.Lessay, LAND, SIZE_SMALL, IMPORTANCE_LOW)
    meautis = ControlPoint.from_airport(normandy.Meautis, LAND, SIZE_SMALL, IMPORTANCE_LOW)
    chippelle = ControlPoint.from_airport(normandy.Chippelle, LAND, SIZE_SMALL, IMPORTANCE_LOW)

    def __init__(self):
        super(NormandyTheater, self).__init__()

        self.add_controlpoint(self.st_pierre, connected_to=[self.chippelle])
        self.add_controlpoint(self.maupertus, connected_to=[self.azeville])
        self.add_controlpoint(self.azeville, connected_to=[self.meautis, self.maupertus])
        self.add_controlpoint(self.lessay, connected_to=[self.meautis])
        self.add_controlpoint(self.meautis, connected_to=[self.chippelle, self.lessay, self.azeville])
        self.add_controlpoint(self.chippelle, connected_to=[self.st_pierre, self.meautis])

        self.st_pierre.captured = True
