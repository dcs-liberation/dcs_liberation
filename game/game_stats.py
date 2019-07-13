class FactionTurnMetadata:
    """
    Store metadata about a faction
    """

    aircraft_count: int = 0
    vehicles_count: int = 0
    sam_count: int = 0

    def __init__(self):
        self.aircraft_count = 0
        self.vehicles_count = 0
        self.sam_count = 0


class GameTurnMetadata:
    """
    Store metadata about a game turn
    """

    allied_units:FactionTurnMetadata
    enemy_units:FactionTurnMetadata

    def __init__(self):
        self.allied_units = FactionTurnMetadata()
        self.enemy_units = FactionTurnMetadata()


class GameStats:
    """
    Store statistics for the current game
    """

    data_per_turn: [GameTurnMetadata] = []

    def __init__(self):
        self.data_per_turn = []

    def update(self, game):
        """
        Save data for current turn
        :param game: Game we want to save the data about
        """

        turn_data = GameTurnMetadata()

        for cp in game.theater.controlpoints:
            if cp.captured:
                turn_data.allied_units.aircraft_count += sum(cp.base.aircraft.values())
                turn_data.allied_units.sam_count += sum(cp.base.aa.values())
                turn_data.allied_units.vehicles_count += sum(cp.base.armor.values())
            else:
                turn_data.enemy_units.aircraft_count += sum(cp.base.aircraft.values())
                turn_data.enemy_units.sam_count += sum(cp.base.aa.values())
                turn_data.enemy_units.vehicles_count += sum(cp.base.armor.values())

        self.data_per_turn.append(turn_data)

