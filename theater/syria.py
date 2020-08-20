from dcs.terrain import normandy, syria

from .conflicttheater import *
from .landmap import *


class GolanHeights(ConflictTheater):
    terrain = dcs.terrain.Syria()
    overview_image = "syria.gif"
    reference_points = {(syria.Eyn_Shemer.position.x, syria.Eyn_Shemer.position.y): (1300, 1380),
                        (syria.Tabqa.position.x, syria.Tabqa.position.y): (2060, 570)}
    landmap = load_landmap("resources\\syrialandmap.p")
    daytime_map = {
        "dawn": (6, 8),
        "day": (8, 16),
        "dusk": (16, 18),
        "night": (0, 5),
    }

    def __init__(self):
        super(GolanHeights, self).__init__()

        self.ramatDavid = ControlPoint.from_airport(syria.Ramat_David, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.kinghussein = ControlPoint.from_airport(syria.King_Hussein_Air_College, LAND, SIZE_REGULAR, IMPORTANCE_HIGH)
        self.khalkhala = ControlPoint.from_airport(syria.Khalkhalah, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)

        self.khalkhala.allow_sea_units = False
        self.ramatDavid.allow_sea_units = False
        self.kinghussein.allow_sea_units = False

        self.marjruhayyil = ControlPoint.from_airport(syria.Marj_Ruhayyil, LAND, SIZE_REGULAR, IMPORTANCE_LOW)
        self.mezzeh = ControlPoint.from_airport(syria.Mezzeh, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)
        self.aldumayr = ControlPoint.from_airport(syria.Al_Dumayr, LAND, SIZE_REGULAR, IMPORTANCE_MEDIUM)

        self.carrier = ControlPoint.carrier("Carrier", Point(-280000, -238000), 1001)
        self.lha = ControlPoint.lha("LHA Carrier", Point(-237000, -89800), 1002)

        self.add_controlpoint(self.ramatDavid, connected_to=[self.khalkhala, self.kinghussein])
        self.add_controlpoint(self.khalkhala, connected_to=[self.ramatDavid, self.kinghussein, self.marjruhayyil])
        self.add_controlpoint(self.kinghussein, connected_to=[self.khalkhala, self.ramatDavid])
        self.add_controlpoint(self.marjruhayyil, connected_to=[self.khalkhala, self.mezzeh, self.aldumayr])
        self.add_controlpoint(self.mezzeh, connected_to=[self.marjruhayyil])
        self.add_controlpoint(self.aldumayr, connected_to=[self.marjruhayyil])

        self.add_controlpoint(self.carrier)
        self.add_controlpoint(self.lha)

        self.ramatDavid.captured = True
        self.carrier.captured = True
        self.lha.captured = True

        self.aldumayr.captured_invert = True
        self.carrier.captured_invert = True
        self.lha.captured_invert = True
