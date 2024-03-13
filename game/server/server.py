import time
from collections.abc import Iterator
from contextlib import contextmanager
from threading import Thread

import uvicorn
from uvicorn import Config

from game.server import EventStream
from game.server.app import app
from game.server.settings import ServerSettings
from game.sim import GameUpdateEvents


class Server(uvicorn.Server):
    def __init__(self) -> None:
        super().__init__(
            Config(
                app=app,
                host=ServerSettings.get().server_bind_address,
                port=ServerSettings.get().server_port,
                # Configured explicitly with default_logging.yaml or logging.yaml.
                log_config=None,
            )
        )

    @contextmanager
    def run_in_thread(self) -> Iterator[None]:
        # This relies on undocumented behavior, but it is what the developer recommends:
        # https://github.com/encode/uvicorn/issues/742
        thread = Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            EventStream.put_nowait(GameUpdateEvents().shut_down())
            thread.join()
