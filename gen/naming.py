class NameGenerator:
    number = 0

    def next_armor_group_name(self):
        self.number += 1
        return "Armor Unit {}".format(self.number)

    def next_cas_group_name(self):
        self.number += 1
        return "CAS Unit {}".format(self.number)

    def next_escort_group_name(self):
        self.number += 1
        return "Escort Unit {}".format(self.number)

    def next_intercept_group_name(self):
        self.number += 1
        return "Intercept Unit {}".format(self.number)
    
    def next_ground_group_name(self):
        self.number += 1
        return "AA Unit {}".format(self.number)

    def next_transport_group_name(self):
        self.number += 1
        return "Transport Unit {}".format(self.number)

    def next_awacs_group_name(self):
        self.number += 1
        return "AWACS Unit {}".format(self.number)

    def next_passenger_group_name(self):
        self.number += 1
        return "Infantry Unit {}".format(self.number)


namegen = NameGenerator()

