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

        self.tonopah_test_range = ControlPoint.from_airport(nevada.Tonopah_Test_Range_Airfield, LAND, SIZE_SMALL,IMPORTANCE_LOW)
        self.lincoln_conty = ControlPoint.from_airport(nevada.Lincoln_County, LAND, SIZE_SMALL, 1.2)
        self.groom_lake = ControlPoint.from_airport(nevada.Groom_Lake_AFB, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.mesquite = ControlPoint.from_airport(nevada.Mesquite, LAND, SIZE_REGULAR, 1.3)
        self.creech = ControlPoint.from_airport(nevada.Creech_AFB, LAND, SIZE_BIG, IMPORTANCE_HIGH)
        self.nellis = ControlPoint.from_airport(nevada.Nellis_AFB, LAND, SIZE_BIG, IMPORTANCE_HIGH)

        self.add_controlpoint(self.tonopah_test_range, connected_to=[self.lincoln_conty, self.groom_lake])
        self.add_controlpoint(self.lincoln_conty, connected_to=[self.tonopah_test_range, self.mesquite])
        self.add_controlpoint(self.groom_lake, connected_to=[self.mesquite, self.creech, self.tonopah_test_range])

        self.add_controlpoint(self.creech, connected_to=[self.groom_lake, self.nellis])
        self.add_controlpoint(self.mesquite, connected_to=[self.lincoln_conty, self.groom_lake])
        self.add_controlpoint(self.nellis, connected_to=[self.creech])

        self.nellis.captured = True
        self.tonopah_test_range.captured_invert = True

