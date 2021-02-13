from enum import Enum

from dcs import task
from dcs.planes import PlaneType
from dcs.weapons_data import Weapons


class F_22A(PlaneType):
    id = "F-22A"
    flyable = True
    height = 4.88
    width = 13.05
    length = 19.1
    fuel_max = 6103
    max_speed = 2649.996
    chaff = 120
    flare = 120
    charge_total = 240
    chaff_charge_size = 1
    flare_charge_size = 2
    eplrs = True
    category = "Interceptor"  # {78EFB7A2-FD52-4b57-A6A6-3BF0E1D6555F}
    radio_frequency = 127.5

    class Liveries:
        class USSR(Enum):
            default = "default"

        class Georgia(Enum):
            default = "default"

        class Venezuela(Enum):
            default = "default"

        class Australia(Enum):
            default = "default"

        class Israel(Enum):
            default = "default"

        class Combined_Joint_Task_Forces_Blue(Enum):
            default = "default"

        class Sudan(Enum):
            default = "default"

        class Norway(Enum):
            default = "default"

        class Romania(Enum):
            default = "default"

        class Iran(Enum):
            default = "default"

        class Ukraine(Enum):
            default = "default"

        class Libya(Enum):
            default = "default"

        class Belgium(Enum):
            default = "default"

        class Slovakia(Enum):
            default = "default"

        class Greece(Enum):
            default = "default"

        class UK(Enum):
            default = "default"

        class Third_Reich(Enum):
            default = "default"

        class Hungary(Enum):
            default = "default"

        class Abkhazia(Enum):
            default = "default"

        class Morocco(Enum):
            default = "default"

        class United_Nations_Peacekeepers(Enum):
            default = "default"

        class Switzerland(Enum):
            default = "default"

        class SouthOssetia(Enum):
            default = "default"

        class Vietnam(Enum):
            default = "default"

        class China(Enum):
            default = "default"

        class Yemen(Enum):
            default = "default"

        class Kuwait(Enum):
            default = "default"

        class Serbia(Enum):
            default = "default"

        class Oman(Enum):
            default = "default"

        class India(Enum):
            default = "default"

        class Egypt(Enum):
            default = "default"

        class TheNetherlands(Enum):
            default = "default"

        class Poland(Enum):
            default = "default"

        class Syria(Enum):
            default = "default"

        class Finland(Enum):
            default = "default"

        class Kazakhstan(Enum):
            default = "default"

        class Denmark(Enum):
            default = "default"

        class Sweden(Enum):
            default = "default"

        class Croatia(Enum):
            default = "default"

        class CzechRepublic(Enum):
            default = "default"

        class GDR(Enum):
            default = "default"

        class Yugoslavia(Enum):
            default = "default"

        class Bulgaria(Enum):
            default = "default"

        class SouthKorea(Enum):
            default = "default"

        class Tunisia(Enum):
            default = "default"

        class Combined_Joint_Task_Forces_Red(Enum):
            default = "default"

        class Lebanon(Enum):
            default = "default"

        class Portugal(Enum):
            default = "default"

        class Cuba(Enum):
            default = "default"

        class Insurgents(Enum):
            default = "default"

        class SaudiArabia(Enum):
            default = "default"

        class France(Enum):
            default = "default"

        class USA(Enum):
            default = "default"

        class Honduras(Enum):
            default = "default"

        class Qatar(Enum):
            default = "default"

        class Russia(Enum):
            default = "default"

        class United_Arab_Emirates(Enum):
            default = "default"

        class Italian_Social_Republi(Enum):
            default = "default"

        class Austria(Enum):
            default = "default"

        class Bahrain(Enum):
            default = "default"

        class Italy(Enum):
            default = "default"

        class Chile(Enum):
            default = "default"

        class Turkey(Enum):
            default = "default"

        class Philippines(Enum):
            default = "default"

        class Algeria(Enum):
            default = "default"

        class Pakistan(Enum):
            default = "default"

        class Malaysia(Enum):
            default = "default"

        class Indonesia(Enum):
            default = "default"

        class Iraq(Enum):
            default = "default"

        class Germany(Enum):
            default = "default"

        class South_Africa(Enum):
            default = "default"

        class Jordan(Enum):
            default = "default"

        class Mexico(Enum):
            default = "default"

        class USAFAggressors(Enum):
            default = "default"

        class Brazil(Enum):
            default = "default"

        class Spain(Enum):
            default = "default"

        class Belarus(Enum):
            default = "default"

        class Canada(Enum):
            default = "default"

        class NorthKorea(Enum):
            default = "default"

        class Ethiopia(Enum):
            default = "default"

        class Japan(Enum):
            default = "default"

        class Thailand(Enum):
            default = "default"

    class Pylon1:
        AIM_9X_Sidewinder_IR_AAM = (1, Weapons.AIM_9X_Sidewinder_IR_AAM)

    class Pylon2:
        Fuel_tank_610_gal = (2, Weapons.Fuel_tank_610_gal)
        AIM_9X_Sidewinder_IR_AAM = (2, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (2, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_120C = (2, Weapons.AIM_120C)
        Smokewinder___red = (2, Weapons.Smokewinder___red)
        Smokewinder___green = (2, Weapons.Smokewinder___green)
        Smokewinder___blue = (2, Weapons.Smokewinder___blue)
        Smokewinder___white = (2, Weapons.Smokewinder___white)
        Smokewinder___yellow = (2, Weapons.Smokewinder___yellow)
        CBU_97 = (2, Weapons.CBU_97)
        Fuel_tank_370_gal = (2, Weapons.Fuel_tank_370_gal)
        LAU_115_2_LAU_127_AIM_9M = (2, Weapons.LAU_115_2_LAU_127_AIM_9M)
        LAU_115_2_LAU_127_AIM_9X = (2, Weapons.LAU_115_2_LAU_127_AIM_9X)
        LAU_115_2_LAU_127_AIM_120C = (2, Weapons.LAU_115_2_LAU_127_AIM_120C)

    class Pylon3:
        AIM_9M_Sidewinder_IR_AAM = (3, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (3, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C = (3, Weapons.AIM_120C)
        CBU_97 = (3, Weapons.CBU_97)

    class Pylon4:
        AIM_9M_Sidewinder_IR_AAM = (4, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (4, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C = (4, Weapons.AIM_120C)
        CBU_97 = (4, Weapons.CBU_97)

    class Pylon5:
        AIM_9M_Sidewinder_IR_AAM = (5, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (5, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C = (5, Weapons.AIM_120C)
        CBU_97 = (5, Weapons.CBU_97)

    class Pylon6:
        Smokewinder___red = (6, Weapons.Smokewinder___red)
        Smokewinder___green = (6, Weapons.Smokewinder___green)
        Smokewinder___blue = (6, Weapons.Smokewinder___blue)
        Smokewinder___white = (6, Weapons.Smokewinder___white)
        Smokewinder___yellow = (6, Weapons.Smokewinder___yellow)

    class Pylon7:
        AIM_9M_Sidewinder_IR_AAM = (7, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (7, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C = (7, Weapons.AIM_120C)
        CBU_97 = (7, Weapons.CBU_97)

    class Pylon8:
        AIM_9M_Sidewinder_IR_AAM = (8, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (8, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C = (8, Weapons.AIM_120C)
        CBU_97 = (8, Weapons.CBU_97)

    class Pylon9:
        AIM_9M_Sidewinder_IR_AAM = (9, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_9X_Sidewinder_IR_AAM = (9, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_120C = (9, Weapons.AIM_120C)
        CBU_97 = (9, Weapons.CBU_97)

    class Pylon10:
        Fuel_tank_610_gal = (10, Weapons.Fuel_tank_610_gal)
        AIM_9X_Sidewinder_IR_AAM = (10, Weapons.AIM_9X_Sidewinder_IR_AAM)
        AIM_9M_Sidewinder_IR_AAM = (10, Weapons.AIM_9M_Sidewinder_IR_AAM)
        AIM_120C = (10, Weapons.AIM_120C)
        Smokewinder___red = (10, Weapons.Smokewinder___red)
        Smokewinder___green = (10, Weapons.Smokewinder___green)
        Smokewinder___blue = (10, Weapons.Smokewinder___blue)
        Smokewinder___white = (10, Weapons.Smokewinder___white)
        Smokewinder___yellow = (10, Weapons.Smokewinder___yellow)
        CBU_97 = (10, Weapons.CBU_97)
        Fuel_tank_370_gal = (10, Weapons.Fuel_tank_370_gal)
        LAU_115_2_LAU_127_AIM_9M = (10, Weapons.LAU_115_2_LAU_127_AIM_9M)
        LAU_115_2_LAU_127_AIM_9X = (10, Weapons.LAU_115_2_LAU_127_AIM_9X)
        LAU_115_2_LAU_127_AIM_120C = (10, Weapons.LAU_115_2_LAU_127_AIM_120C)

    class Pylon11:
        AIM_9X_Sidewinder_IR_AAM = (11, Weapons.AIM_9X_Sidewinder_IR_AAM)

    pylons = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}

    tasks = [
        task.CAP,
        task.Escort,
        task.FighterSweep,
        task.Intercept,
        task.Reconnaissance,
    ]
    task_default = task.CAP
