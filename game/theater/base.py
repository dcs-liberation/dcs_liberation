from game.dcs.groundunittype import GroundUnitType

BASE_MAX_STRENGTH = 1.0
BASE_MIN_STRENGTH = 0.0


class Base:
    def __init__(self) -> None:
        self.armor: dict[GroundUnitType, int] = {}
        self.strength = 1.0

    @property
    def total_armor(self) -> int:
        return sum(self.armor.values())

    @property
    def total_armor_value(self) -> int:
        total = 0
        for unit_type, count in self.armor.items():
            total += unit_type.price * count
        return total

    def total_units_of_type(self, unit_type: GroundUnitType) -> int:
        return sum([c for t, c in self.armor.items() if t == unit_type])

    def commission_units(self, units: dict[GroundUnitType, int]) -> None:
        for unit_type, unit_count in units.items():
            if unit_count <= 0:
                continue
            self.armor[unit_type] = self.armor.get(unit_type, 0) + unit_count

    def commit_losses(self, units_lost: dict[GroundUnitType, int]) -> None:
        for unit_type, count in units_lost.items():
            if unit_type not in self.armor:
                print("Base didn't find unit type {}".format(unit_type))
                continue

            self.armor[unit_type] = max(self.armor[unit_type] - count, 0)
            if self.armor[unit_type] == 0:
                del self.armor[unit_type]

    def affect_strength(self, amount: float) -> None:
        self.strength += amount
        if self.strength > BASE_MAX_STRENGTH:
            self.strength = BASE_MAX_STRENGTH
        elif self.strength <= 0:
            self.strength = BASE_MIN_STRENGTH

    def set_strength_to_minimum(self) -> None:
        self.strength = BASE_MIN_STRENGTH
