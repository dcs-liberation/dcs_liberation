from __future__ import annotations

from dataclasses import dataclass, field
from enum import unique, Enum

from faker import Faker


@dataclass
class PilotRecord:
    missions_flown: int = field(default=0)


@unique
class PilotStatus(Enum):
    Active = "Active"
    OnLeave = "On leave"
    Dead = "Dead"


@dataclass
class Pilot:
    name: str
    player: bool = field(default=False)
    status: PilotStatus = field(default=PilotStatus.Active)
    record: PilotRecord = field(default_factory=PilotRecord)

    @property
    def alive(self) -> bool:
        return self.status is not PilotStatus.Dead

    @property
    def on_leave(self) -> bool:
        return self.status is PilotStatus.OnLeave

    def send_on_leave(self) -> None:
        if self.status is not PilotStatus.Active:
            raise RuntimeError("Only active pilots may be sent on leave")
        self.status = PilotStatus.OnLeave

    def return_from_leave(self) -> None:
        if self.status is not PilotStatus.OnLeave:
            raise RuntimeError("Only pilots on leave may be returned from leave")
        self.status = PilotStatus.Active

    def kill(self) -> None:
        self.status = PilotStatus.Dead

    @classmethod
    def random(cls, faker: Faker) -> Pilot:
        return Pilot(faker.name())
