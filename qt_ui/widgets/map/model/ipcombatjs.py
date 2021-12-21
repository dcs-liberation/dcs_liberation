from PySide2.QtCore import Property, QObject, Signal

from game.sim.combat.atip import AtIp
from qt_ui.models import GameModel
from .flightjs import FlightJs


class IpCombatJs(QObject):
    flightChanged = Signal()

    def __init__(self, combat: AtIp, game_model: GameModel) -> None:
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

    @Property(FlightJs, notify=flightChanged)
    def flight(self) -> FlightJs:
        return self._flight

    def refresh(self) -> None:
        pass
