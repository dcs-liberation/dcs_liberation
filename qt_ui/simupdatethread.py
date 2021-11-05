from threading import Event, Thread, Timer
from typing import Callable


class SimUpdateThread(Thread):
    def __init__(self, update_callback: Callable[[], None]) -> None:
        super().__init__()
        self.update_callback = update_callback
        self.running = False
        self.should_shutdown = False
        self._interrupt = Event()
        self._timer = self._make_timer()

    def run(self) -> None:
        while True:
            self._interrupt.wait()
            self._interrupt.clear()
            if self.should_shutdown:
                return
            if self.running:
                self.update_callback()
            self._timer = self._make_timer()
            self._timer.start()

    def on_sim_pause(self) -> None:
        self._timer.cancel()
        self._timer = self._make_timer()
        self.running = False

    def on_sim_unpause(self) -> None:
        if not self.running:
            self.running = True
            self._timer.start()

    def stop(self) -> None:
        self.should_shutdown = True
        self._interrupt.set()

    def on_timer_elapsed(self) -> None:
        self._timer = self._make_timer()
        self._timer.start()
        self._interrupt.set()

    def _make_timer(self) -> Timer:
        return Timer(1 / 60, lambda: self._interrupt.set())
