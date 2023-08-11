from typing import TypeAlias, TypeVar, Callable

T = TypeVar("T")
Provider: TypeAlias = Callable[[], T]
