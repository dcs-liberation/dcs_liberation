from __future__ import annotations

from typing import List, Optional

from PySide2.QtCore import Property, QObject, Signal, Slot
from dcs.unit import Unit
from dcs.vehicles import vehicle_map

from game import Game
from game.dcs.groundunittype import GroundUnitType
from game.theater import TheaterGroundObject
from qt_ui.dialogs import Dialog
from qt_ui.widgets.map.model.leaflet import LeafletLatLon
from qt_ui.windows.groundobject.QGroundObjectMenu import QGroundObjectMenu


class GroundObjectJs(QObject):
    nameChanged = Signal()
    controlPointNameChanged = Signal()
    unitsChanged = Signal()
    blueChanged = Signal()
    positionChanged = Signal()
    samThreatRangesChanged = Signal()
    samDetectionRangesChanged = Signal()
    categoryChanged = Signal()
    deadChanged = Signal()

    def __init__(self, tgo: TheaterGroundObject, game: Game) -> None:
        super().__init__()
        self.tgo = tgo
        self.game = game
        self.theater = game.theater
        self.buildings = self.theater.find_ground_objects_by_obj_name(self.tgo.obj_name)
        self.dialog: Optional[QGroundObjectMenu] = None

    @Slot()
    def showInfoDialog(self) -> None:
        if self.dialog is None:
            self.dialog = QGroundObjectMenu(
                None,
                self.tgo,
                self.buildings,
                self.tgo.control_point,
                self.game,
            )
        self.dialog.show()

    @Slot()
    def showPackageDialog(self) -> None:
        Dialog.open_new_package_dialog(self.tgo)

    @Property(str, notify=nameChanged)
    def name(self) -> str:
        return self.tgo.name

    @Property(str, notify=controlPointNameChanged)
    def controlPointName(self) -> str:
        return self.tgo.control_point.name

    @Property(str, notify=categoryChanged)
    def category(self) -> str:
        return self.tgo.category

    @staticmethod
    def make_unit_name(unit: Unit, dead: bool) -> str:
        dead_label = " [DEAD]" if dead else ""
        unit_display_name = unit.type
        dcs_unit_type = vehicle_map.get(unit.type)
        if dcs_unit_type is not None:
            # TODO: Make the TGO contain GroundUnitType instead of the pydcs Group.
            # This is a hack because we can't know which variant was used.
            try:
                unit_display_name = next(
                    GroundUnitType.for_dcs_type(dcs_unit_type)
                ).name
            except StopIteration:
                pass
        return f"Unit #{unit.id} - {unit_display_name}{dead_label}"

    @Property(list, notify=unitsChanged)
    def units(self) -> List[str]:
        units = []
        # TGOs with a non-empty group set are non-building TGOs. Building TGOs have no
        # groups set, but instead are one TGO per building "group" (DCS doesn't support
        # groups of statics) all with the same name.
        if self.tgo.groups:
            for unit in self.tgo.units:
                units.append(self.make_unit_name(unit, dead=False))
            for unit in self.tgo.dead_units:
                units.append(self.make_unit_name(unit, dead=True))
        else:
            for building in self.buildings:
                dead = " [DEAD]" if building.is_dead else ""
                units.append(f"{building.dcs_identifier}{dead}")
        return units

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.tgo.control_point.captured

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.tgo.position)
        return [ll.latitude, ll.longitude]

    @Property(bool, notify=deadChanged)
    def dead(self) -> bool:
        if not self.tgo.groups:
            return all(b.is_dead for b in self.buildings)
        return not any(g.units for g in self.tgo.groups)

    @Property(list, notify=samThreatRangesChanged)
    def samThreatRanges(self) -> List[float]:
        if not self.tgo.might_have_aa:
            return []

        ranges = []
        for group in self.tgo.groups:
            threat_range = self.tgo.threat_range(group)
            if threat_range:
                ranges.append(threat_range.meters)
        return ranges

    @Property(list, notify=samDetectionRangesChanged)
    def samDetectionRanges(self) -> List[float]:
        if not self.tgo.might_have_aa:
            return []

        ranges = []
        for group in self.tgo.groups:
            detection_range = self.tgo.detection_range(group)
            if detection_range:
                ranges.append(detection_range.meters)
        return ranges
