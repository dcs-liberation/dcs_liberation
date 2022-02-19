from typing import Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


class Database(Generic[T]):
    def __init__(self) -> None:
        self.objects: dict[UUID, T] = {}

    def add(self, uuid: UUID, obj: T) -> None:
        if uuid in self.objects:
            raise KeyError(f"Object with UUID {uuid} already exists")
        self.objects[uuid] = obj

    def get(self, uuid: UUID) -> T:
        return self.objects[uuid]

    def remove(self, uuid: UUID) -> None:
        del self.objects[uuid]
