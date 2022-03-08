from __future__ import annotations

from asyncio import Queue
from collections.abc import Iterator
from contextlib import contextmanager

from game.sim import GameUpdateEvents


class EventStream:
    _queue: Queue[GameUpdateEvents] = Queue()

    @classmethod
    def drain(cls) -> None:
        while not cls._queue.empty():
            cls._queue.get_nowait()
            cls._queue.task_done()

    @classmethod
    async def put(cls, events: GameUpdateEvents) -> None:
        await cls._queue.put(events)

    @classmethod
    def put_nowait(cls, events: GameUpdateEvents) -> None:
        # The queue has infinite size so this should never need to block anyway. If for
        # some reason the queue is full this will throw QueueFull.
        cls._queue.put_nowait(events)

    @classmethod
    async def get(cls) -> GameUpdateEvents:
        events = await cls._queue.get()
        cls._queue.task_done()
        return events

    @staticmethod
    @contextmanager
    def event_context() -> Iterator[GameUpdateEvents]:
        events = GameUpdateEvents()
        yield events
        EventStream.put_nowait(events)
