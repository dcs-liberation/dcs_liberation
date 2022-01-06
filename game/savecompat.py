"""Tools for aiding in save compat removal after compatibility breaks."""
from collections.abc import Callable
from typing import TypeVar

from game.version import MAJOR_VERSION

ReturnT = TypeVar("ReturnT")


class DeprecatedSaveCompatError(RuntimeError):
    def __init__(self, function_name: str) -> None:
        super().__init__(
            f"{function_name} has save compat code for a different major version."
        )


def has_save_compat_for(
    major: int,
) -> Callable[[Callable[..., ReturnT]], Callable[..., ReturnT]]:
    """Declares a function or method as having save compat code for a given version.

    If the function has save compatibility for the current major version, there is no
    change in behavior.

    If the function has save compatibility for a *different* (future or past) major
    version, DeprecatedSaveCompatError will be raised during startup. Since a break in
    save compatibility is the definition of a major version break, there's no need to
    keep around old save compat code; it only serves to mask initialization bugs.

    Args:
        major: The major version for which the decorated function has save
        compatibility.

    Returns:
        The decorated function or method.

    Raises:
        DeprecatedSaveCompatError: The decorated function has save compat code for
        another version of liberation, and that code (and the decorator declaring it)
        should be removed from this branch.
    """

    def decorator(func: Callable[..., ReturnT]) -> Callable[..., ReturnT]:
        if major != MAJOR_VERSION:
            raise DeprecatedSaveCompatError(func.__name__)
        return func

    return decorator
