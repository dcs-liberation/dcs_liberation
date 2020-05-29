from dcs.terrain import nevada
from dcs import mapping

from .landmap import *
from .conflicttheater import *
from .base import *


class NevadaTheater(ConflictTheater):
    terrain = dcs.terrain.Nevada()
    overview_image = "nevada.gif"
    reference_points = {(nevada.Mina_Airport_3Q0.position.x, nevada.Mina_Airport_3Q0.position.y): (45*2, -360*2),
                        (nevada.Laughlin_Airport.position.x, nevada.Laughlin_Airport.position.y): (440*2, 80*2), }
    landmap = load_landmap("resources\\nev_landmap.p")
    daytime_map = {
        "dawn": (4, 6),
        "day": (6, 17),
        "dusk": (17, 18),
        "night": (0, 5),
    }

    def __init__(self):
        super(NevadaTheater, self).__init__()

        self.tonopah = ControlPoint.from_airport(nevada.Tonopah_Airport, LAND, SIZE_SMALL, IMPORTANCE_LOW)
        self.tonopah_test_range = ControlPoint.from_airport(nevada.Tonopah_Test_Range_Airfield, LAND, SIZE_SMALL,IMPORTANCE_LOW)
        self.lincoln_conty = ControlPoint.from_airport(nevada.Lincoln_County, LAND, SIZE_SMALL, 1.2)
        self.pahute_mesa = ControlPoint.from_airport(nevada.Pahute_Mesa_Airstrip, LAND, SIZE_SMALL, 1.1)
        self.groom_lake = ControlPoint.from_airport(nevada.Groom_Lake_AFB, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.mesquite = ControlPoint.from_airport(nevada.Mesquite, LAND, SIZE_REGULAR, 1.3)
        self.beatty = ControlPoint.from_airport(nevada.Beatty_Airport, LAND, SIZE_REGULAR, 1.1)
        self.creech = ControlPoint.from_airport(nevada.Creech_AFB, LAND, SIZE_BIG, IMPORTANCE_HIGH)
        #self.las_vegas = ControlPoint.from_airport(nevada.North_Las_Vegas, LAND, SIZE_LARGE, IMPORTANCE_HIGH)
        #self.jean = ControlPoint.from_airport(nevada.Jean_Airport, LAND, SIZE_REGULAR, 1.2)
        #self.laughlin = ControlPoint.from_airport(nevada.Laughlin_Airport, LAND, SIZE_LARGE, IMPORTANCE_HIGH)

        self.add_controlpoint(self.tonopah, connected_to=[self.tonopah_test_range])

        self.add_controlpoint(self.tonopah_test_range, connected_to=[self.tonopah, self.lincoln_conty, self.pahute_mesa])
        self.add_controlpoint(self.lincoln_conty, connected_to=[self.tonopah_test_range, self.mesquite, self.groom_lake])
        self.add_controlpoint(self.pahute_mesa, connected_to=[self.groom_lake, self.tonopah_test_range, self.beatty, self.creech])
        self.add_controlpoint(self.groom_lake, connected_to=[self.pahute_mesa, self.lincoln_conty, self.mesquite])

        self.add_controlpoint(self.beatty, connected_to=[self.pahute_mesa])
        self.add_controlpoint(self.creech, connected_to=[self.mesquite, self.pahute_mesa])
        self.add_controlpoint(self.mesquite, connected_to=[self.lincoln_conty, self.groom_lake, self.creech])

        self.tonopah.captured = True

