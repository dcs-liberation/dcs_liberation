from __future__ import annotations

import logging
import timeit
from collections import defaultdict
from contextlib import contextmanager
from datetime import timedelta
from typing import Iterator


@contextmanager
def logged_duration(event: str) -> Iterator[None]:
    start = timeit.default_timer()
    yield
    end = timeit.default_timer()
    logging.debug("%s took %s", event, timedelta(seconds=end - start))


class MultiEventTracer:
    def __init__(self) -> None:
        self.events: dict[str, timedelta] = defaultdict(timedelta)

    def __enter__(self) -> MultiEventTracer:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        for event, duration in self.events.items():
            logging.debug("%s took %s", event, duration)

    @contextmanager
    def trace(self, event: str) -> Iterator[None]:
        start = timeit.default_timer()
        yield
        end = timeit.default_timer()
        self.events[event] += timedelta(seconds=end - start)
