from game import db


class NameGenerator:
    number = 0

    def next_unit_name(self, country, unit_type):
        self.number += 1
        return "{}|{}|{}".format(country.id, self.number, db.unit_type_name(unit_type))

    def next_basedefense_name(self):
        return "basedefense_aa"


namegen = NameGenerator()

