import dcs

money = 2000
aircraft = []
armor = []
control_points = []

def add_aircraft(plane: dcs.planes.PlaneType):
    aircraft.append(plane)

def add_armor(vehicle: dcs.vehicles.Armor):
    armor.append(vehicle)

def add_control_point(cp):
    control_points.append(cp)
