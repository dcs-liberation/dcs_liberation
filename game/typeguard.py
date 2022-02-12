from __future__ import annotations

from typing import Callable, TypeGuard, TypeVar

SelfT = TypeVar("SelfT")
BaseT = TypeVar("BaseT")
GuardT = TypeVar("GuardT")


def self_type_guard(
    f: Callable[[SelfT, BaseT], TypeGuard[GuardT]]
) -> Callable[[SelfT, BaseT], TypeGuard[GuardT]]:
    def decorator(s: SelfT, arg: BaseT) -> TypeGuard[GuardT]:
        if id(s) != id(arg):
            raise ValueError(
                "self type guards must be called with self as the argument"
            )
        return f(s, arg)

    return decorator
