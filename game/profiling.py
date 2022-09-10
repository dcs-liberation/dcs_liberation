from __future__ import annotations

import logging
import timeit
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import timedelta
from types import TracebackType
from typing import Iterator, Optional, Type


@contextmanager
def logged_duration(event: str) -> Iterator[None]:
    timer = Timer()
    with timer:
        yield
    logging.debug("%s took %s", event, timer.duration)


@dataclass
class CountedEvent:
    count: int = 0
    duration: timedelta = timedelta()

    def increment(self, duration: timedelta) -> None:
        self.count += 1
        self.duration += duration

    @property
    def average(self) -> timedelta:
        return self.duration / self.count


class MultiEventTracer:
    def __init__(self) -> None:
        self.events: dict[str, CountedEvent] = defaultdict(CountedEvent)

    def __enter__(self) -> MultiEventTracer:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        for event, counter in self.events.items():
            logging.debug(
                "%s %d times took %s (%s average)",
                event,
                counter.count,
                counter.duration,
                counter.average,
            )

    @contextmanager
    def trace(self, event: str) -> Iterator[None]:
        timer = Timer()
        with timer:
            yield
        self.events[event].increment(timer.duration)


class Timer:
    def __init__(self) -> None:
        self._start_time: float | None = None
        self._end_time: float | None = None
        self._duration: timedelta | None = None

    @property
    def duration(self) -> timedelta:
        if self._duration is None:
            raise RuntimeError(
                "Cannot query the duration of the timer before it has elapsed"
            )
        return self._duration

    def __enter__(self) -> None:
        self._start_time = timeit.default_timer()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        assert self._start_time is not None
        self._end_time = timeit.default_timer()
        self._duration = timedelta(seconds=self._end_time - self._start_time)
