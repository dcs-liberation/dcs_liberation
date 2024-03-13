from collections.abc import Iterable, Iterator
from typing import Generic, Optional, TypeVar

ValueT = TypeVar("ValueT")


class OrderedSet(Generic[ValueT]):
    def __init__(self, initial_data: Optional[Iterable[ValueT]] = None) -> None:
        if initial_data is None:
            initial_data = []
        self._data: dict[ValueT, None] = {v: None for v in initial_data}

    def __iter__(self) -> Iterator[ValueT]:
        yield from self._data

    def __contains__(self, item: ValueT) -> bool:
        return item in self._data

    def add(self, item: ValueT) -> None:
        self._data[item] = None

    def clear(self) -> None:
        self._data.clear()
