from abc import ABC, abstractmethod


class MissionTarget(ABC):
    # TODO: These should just be required objects to the constructor
    # The TheatherGroundObject class is difficult to modify because it's
    # generated data that's pickled ahead of time.
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the mission target."""
