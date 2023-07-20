import logging

from PySide6.QtWidgets import QGridLayout, QLabel, QWidget
from dcs.unitpropertydescription import UnitPropertyDescription

from game.ato import Flight
from .missingpropertydataerror import MissingPropertyDataError
from .propertycheckbox import PropertyCheckBox
from .propertycombobox import PropertyComboBox
from .propertyspinbox import PropertySpinBox


class UnhandledControlTypeError(RuntimeError):
    def __init__(self, control: str) -> None:
        super().__init__(f"Unhandled control type {control}")


class PropertyEditor(QGridLayout):
    def __init__(self, flight: Flight) -> None:
        super().__init__()
        self.flight = flight

        for row, prop in enumerate(flight.unit_type.iter_props()):
            if prop.label is None:
                if prop.control != "label":
                    logging.error(
                        "Found non-label aircraft property with no display name."
                    )
                continue

            if prop.player_only and not flight.client_count:
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

            label = prop.label
            if widget is None:
                label = f"<strong>{label}</label>"
            self.addWidget(QLabel(label), row, 0)

            # If prop.control is "label", widget will be None. We only need to add the
            # label, not the control.
            if widget is not None:
                self.addWidget(widget, row, 1)

    def control_for_property(self, prop: UnitPropertyDescription) -> QWidget | None:
        # Valid values are:
        # "checkbox", "comboList", "groupbox", "label", "slider", "spinbox"
        match prop.control:
            case "checkbox":
                return PropertyCheckBox(self.flight, prop)
            case "comboList":
                return PropertyComboBox(self.flight, prop)
            case "groupbox" | "label":
                return None
            case "slider" | "spinbox":
                return PropertySpinBox(self.flight, prop)
            case _:
                raise UnhandledControlTypeError(prop.control)
