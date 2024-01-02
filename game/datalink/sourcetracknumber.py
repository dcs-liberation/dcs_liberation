from dataclasses import dataclass

from game.datalink.sourcetracknumberprefix import SourceTrackNumberPrefix


@dataclass(frozen=True)
class SourceTrackNumber:
    """Source track number (STN) for a flight member."""

    prefix: SourceTrackNumberPrefix
    index: int

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError("STN indexes cannot be negative")
        if self.index >= 8:
            raise ValueError("STN indexes must be < 8")

    def __str__(self) -> str:
        return f"{self.prefix}{self.index}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.prefix!r}, {self.index})"
