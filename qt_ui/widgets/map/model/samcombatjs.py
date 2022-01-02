from PySide2.QtCore import Property, QObject, Signal

from game.sim.combat.defendingsam import DefendingSam
from qt_ui.models import GameModel
from .flightjs import FlightJs
from .groundobjectjs import GroundObjectJs


class SamCombatJs(QObject):
    flightChanged = Signal()
    airDefensesChanged = Signal()

    def __init__(self, combat: DefendingSam, game_model: GameModel) -> None:
        super().__init__()
        assert game_model.game is not None
        self.combat = combat
        self.theater = game_model.game.theater
        self._flight = FlightJs(
            combat.flight,
            selected=False,
            theater=game_model.game.theater,
            ato_model=game_model.ato_model_for(combat.flight.squadron.player),
        )
        self._air_defenses = [
            GroundObjectJs(tgo, game_model.game) for tgo in self.combat.air_defenses
        ]

    @Property(FlightJs, notify=flightChanged)
    def flight(self) -> FlightJs:
        return self._flight

    @Property(list, notify=airDefensesChanged)
    def airDefenses(self) -> list[GroundObjectJs]:
        return self._air_defenses

    def refresh(self) -> None:
        pass
