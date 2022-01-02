from __future__ import annotations

import inspect
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Generic, Type, TypeVar

from dcs.unittype import FlyingType

from .propertyvalue import PropertyValue

ValueT = TypeVar("ValueT", bool, int)


@dataclass(frozen=True)
class UnitProperty(Generic[ValueT]):
    id: str
    default: ValueT
    values: list[PropertyValue[Any]]

    @classmethod
    def for_aircraft(
        cls, unit_type: Type[FlyingType]
    ) -> Iterator[UnitProperty[ValueT]]:
        try:
            props = unit_type.Properties  # type: ignore
        except AttributeError:
            return

        if unit_type.property_defaults is None:
            raise RuntimeError(f"{unit_type} has Properties but no defaults")

        for name, attr in inspect.getmembers(props, inspect.isclass):
            if name.startswith("__"):
                continue
            yield cls.property_from(attr, unit_type.property_defaults[name])

    @classmethod
    def property_from(cls, attr: Type[ValueT], default: ValueT) -> UnitProperty[ValueT]:
        prop_id = attr.id  # type: ignore
        values = getattr(attr, "Values", None)
        if values is None:
            prop_values = list(cls.default_values_for(prop_id, default))
        else:
            prop_values = []
            for name, value in inspect.getmembers(values):
                if name.startswith("__"):
                    continue
                prop_values.append(PropertyValue(name, value))
        return UnitProperty(prop_id, default, prop_values)

    @classmethod
    def default_values_for(
        cls, prop_id: str, default: ValueT
    ) -> Iterator[PropertyValue[ValueT]]:
        if isinstance(default, bool):
            yield PropertyValue("True", True)
            yield PropertyValue("False", False)
        elif isinstance(default, int):
            for i in range(10):
                yield PropertyValue(str(i), i)
        else:
            raise TypeError(
                f"Unexpected property type for {prop_id}: {default.__class__}"
            )
