import time
from collections.abc import Iterator
from contextlib import contextmanager
from threading import Thread

import uvicorn
from uvicorn import Config

from game.server.settings import ServerSettings


class Server(uvicorn.Server):
    def __init__(self) -> None:
        super().__init__(
            Config(
                "game.server.app:app",
                host=ServerSettings.get().server_bind_address,
                port=ServerSettings.get().server_port,
                log_level="info",
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
            thread.join()
