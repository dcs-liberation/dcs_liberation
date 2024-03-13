from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TaskContext:
    mission_start_time: datetime
