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

    def __init__(self):
        super(NormandyTheater, self).__init__()

        self.needOarPoint = ControlPoint.from_airport(normandy.Needs_Oar_Point, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.chailey = ControlPoint.from_airport(normandy.Chailey, LAND, SIZE_SMALL, IMPORTANCE_LOW)

        self.deuxjumeaux = ControlPoint.from_airport(normandy.Deux_Jumeaux, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.lignerolles = ControlPoint.from_airport(normandy.Lignerolles, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.carpiquet = ControlPoint.from_airport(normandy.Carpiquet, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.lessay = ControlPoint.from_airport(normandy.Lessay, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.maupertus = ControlPoint.from_airport(normandy.Maupertus, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.evreux = ControlPoint.from_airport(normandy.Evreux, LAND, SIZE_SMALL, IMPORTANCE_LOW)

        self.add_controlpoint(self.chailey, connected_to=[self.needOarPoint])
        self.add_controlpoint(self.needOarPoint, connected_to=[self.chailey])

        self.add_controlpoint(self.deuxjumeaux, connected_to=[self.lignerolles])
        self.add_controlpoint(self.lignerolles, connected_to=[self.deuxjumeaux, self.lessay, self.carpiquet])
        self.add_controlpoint(self.lessay, connected_to=[self.lignerolles, self.maupertus])
        self.add_controlpoint(self.carpiquet, connected_to=[self.lignerolles, self.evreux])
        self.add_controlpoint(self.maupertus, connected_to=[self.lessay])
        self.add_controlpoint(self.evreux, connected_to=[self.carpiquet])

        self.deuxjumeaux.captured = True
        self.chailey.captured = True
        self.needOarPoint.captured = True


class NormandySmall(ConflictTheater):
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

    def __init__(self):
        super(NormandySmall, self).__init__()

        self.needOarPoint = ControlPoint.from_airport(normandy.Needs_Oar_Point, LAND, SIZE_SMALL, IMPORTANCE_LOW)

        self.deuxjumeaux = ControlPoint.from_airport(normandy.Deux_Jumeaux, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.lignerolles = ControlPoint.from_airport(normandy.Lignerolles, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.carpiquet = ControlPoint.from_airport(normandy.Carpiquet, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.evreux = ControlPoint.from_airport(normandy.Evreux, LAND, SIZE_SMALL, IMPORTANCE_LOW)

        self.add_controlpoint(self.needOarPoint, connected_to=[self.needOarPoint])

        self.add_controlpoint(self.deuxjumeaux, connected_to=[self.lignerolles])
        self.add_controlpoint(self.lignerolles, connected_to=[self.deuxjumeaux, self.carpiquet])
        self.add_controlpoint(self.carpiquet, connected_to=[self.lignerolles, self.evreux])
        self.add_controlpoint(self.evreux, connected_to=[self.carpiquet])

        self.deuxjumeaux.captured = True
        self.needOarPoint.captured = True
