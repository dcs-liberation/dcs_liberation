from threading import Lock, Timer
from typing import Callable, Optional

from .simspeedsetting import SimSpeedSetting


class GameLoopTimer:
    def __init__(self, callback: Callable[[], None]) -> None:
        self.callback = callback
        self.simulation_speed = SimSpeedSetting.PAUSED
        self._timer: Optional[Timer] = None
        self._timer_lock = Lock()

    def set_speed(self, simulation_speed: SimSpeedSetting) -> None:
        with self._timer_lock:
            self._stop()
            self.simulation_speed = simulation_speed
            self._recreate_timer()

    def stop(self) -> None:
        with self._timer_lock:
            self._stop()

    def _stop(self) -> None:
        if self._timer is not None:
            self._timer.cancel()

    def _recreate_timer(self) -> None:
        self._stop()
        factor = self.simulation_speed.speed_factor
        if not factor:
            self._timer = None
            return None
        self._timer = Timer(1 / factor, self._tick)
        self._timer.start()

    def _tick(self) -> None:
        self.callback()
        with self._timer_lock:
            self._recreate_timer()
