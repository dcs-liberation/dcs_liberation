import itertools
import logging
from typing import Callable

from PySide6.QtWidgets import QGridLayout, QLabel, QWidget
from dcs.unitpropertydescription import UnitPropertyDescription

from game.ato import Flight
from game.ato.flightmember import FlightMember
from .missingpropertydataerror import MissingPropertyDataError
from .propertycheckbox import PropertyCheckBox
from .propertycombobox import PropertyComboBox
from .propertyspinbox import PropertySpinBox


class UnhandledControlTypeError(RuntimeError):
    def __init__(self, control: str) -> None:
        super().__init__(f"Unhandled control type {control}")


class PropertyEditor(QGridLayout):
    def __init__(self, flight: Flight, flight_member: FlightMember) -> None:
        super().__init__()
        self.flight_member = flight_member
        self.flight_member_update_listeners: list[Callable[[FlightMember], None]] = []

        last_label: QWidget | None = None
        row = itertools.count()
        for prop in flight.unit_type.iter_props():
            if prop.label is None:
                if prop.control != "label":
                    logging.error(
                        "Found non-label aircraft property with no display name."
                    )
                continue

            if prop.player_only and not flight.client_count:
                continue

            if not flight.unit_type.should_show_prop(prop.identifier):
                continue

            try:
                widget = self.control_for_property(prop)
            except (MissingPropertyDataError, UnhandledControlTypeError):
                logging.exception(
                    f"Cannot create property control for property %s of %s",
                    prop.identifier,
                    flight.unit_type,
                )
                continue

            # Draw any deferred label if this is a real control.
            if last_label is not None and widget is not None:
                self.addWidget(last_label, next(row), 0)
                last_label = None

            label = prop.label
            if widget is None:
                label = f"<strong>{label}</label>"

            label = QLabel(label)
            if widget is None:
                # The "control" is only a section label. Defer adding it to the layout
                # so that we can skip empty sections.
                last_label = label
            else:
                # Else the label is for the control itself and should be drawn
                # immediately.
                this_row = next(row)
                self.addWidget(label, this_row, 0)
                self.addWidget(widget, this_row, 1)

    def control_for_property(self, prop: UnitPropertyDescription) -> QWidget | None:
        # Valid values are:
        # "checkbox", "comboList", "groupbox", "label", "slider", "spinbox"
        match prop.control:
            case "checkbox":
                widget = PropertyCheckBox(self.flight_member, prop)
                self.flight_member_update_listeners.append(widget.set_flight_member)
                return widget
            case "comboList":
                widget = PropertyComboBox(self.flight_member, prop)
                self.flight_member_update_listeners.append(widget.set_flight_member)
                return widget
            case "groupbox" | "label":
                return None
            case "slider" | "spinbox":
                widget = PropertySpinBox(self.flight_member, prop)
                self.flight_member_update_listeners.append(widget.set_flight_member)
                return widget
            case _:
                raise UnhandledControlTypeError(prop.control)

    def set_flight_member(self, flight_member: FlightMember) -> None:
        self.flight_member = flight_member
        for listener in self.flight_member_update_listeners:
            listener(self.flight_member)
