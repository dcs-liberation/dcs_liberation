from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QLabel,
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QSpinBox,
    QCheckBox,
)

from game import Game
from game.ato.flight import Flight
from game.ato.flightmember import FlightMember
from game.ato.loadouts import Loadout
from qt_ui.widgets.QLabeledWidget import QLabeledWidget
from .QLoadoutEditor import QLoadoutEditor
from .ownlasercodeinfo import OwnLaserCodeInfo
from .propertyeditor import PropertyEditor
from .weaponlasercodeselector import WeaponLaserCodeSelector


class DcsLoadoutSelector(QComboBox):
    def __init__(self, flight: Flight, member: FlightMember) -> None:
        super().__init__()
        for loadout in Loadout.iter_for(flight):
            self.addItem(loadout.name, loadout)
        self.model().sort(0)
        self.setDisabled(member.loadout.is_custom)
        if member.loadout.is_custom:
            self.setCurrentText(Loadout.default_for(flight).name)
        else:
            self.setCurrentText(member.loadout.name)


class FlightMemberSelector(QSpinBox):
    def __init__(self, flight: Flight, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.flight = flight
        self.setMinimum(1)
        self.setMaximum(flight.count)

    @property
    def selected_member(self) -> FlightMember:
        return self.flight.roster.members[self.value() - 1]


class QFlightPayloadTab(QFrame):
    def __init__(self, flight: Flight, game: Game):
        super(QFlightPayloadTab, self).__init__()
        self.flight = flight
        self.payload_editor = QLoadoutEditor(
            flight, self.flight.roster.members[0], game
        )
        self.payload_editor.toggled.connect(self.on_custom_toggled)

        layout = QVBoxLayout()

        self.member_selector = FlightMemberSelector(self.flight, self)
        self.member_selector.valueChanged.connect(self.rebind_to_selected_member)
        layout.addLayout(QLabeledWidget("Flight member:", self.member_selector))
        self.same_loadout_for_all_checkbox = QCheckBox(
            "Use same loadout for all flight members"
        )
        self.same_loadout_for_all_checkbox.setChecked(
            self.flight.use_same_loadout_for_all_members
        )
        self.same_loadout_for_all_checkbox.toggled.connect(self.on_same_loadout_toggled)
        layout.addWidget(self.same_loadout_for_all_checkbox)
        layout.addWidget(
            QLabel(
                "<strong>Warning: AI flights should use the same loadout for all members.</strong>"
            )
        )

        scroll_content = QWidget()
        scrolling_layout = QVBoxLayout()
        scroll_content.setLayout(scrolling_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(scroll)

        # Docs Link
        docsText = QLabel(
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Custom-Loadouts"><span style="color:#FFFFFF;">How to create your own default loadout</span></a>'
        )
        docsText.setAlignment(Qt.AlignCenter)
        docsText.setOpenExternalLinks(True)

        self.own_laser_code_info = OwnLaserCodeInfo(
            game, self.member_selector.selected_member
        )
        scrolling_layout.addLayout(self.own_laser_code_info)

        self.weapon_laser_code_selector = WeaponLaserCodeSelector(
            game, self.member_selector.selected_member, self
        )
        self.own_laser_code_info.assigned_laser_code_changed.connect(
            self.weapon_laser_code_selector.rebuild
        )
        scrolling_layout.addLayout(
            QLabeledWidget(
                "Preset laser code for weapons:", self.weapon_laser_code_selector
            )
        )
        scrolling_layout.addWidget(
            QLabel(
                "Equipped weapons will be pre-configured to the selected laser code at "
                "mission start."
            )
        )

        self.property_editor = PropertyEditor(
            self.flight, self.member_selector.selected_member
        )
        scrolling_layout.addLayout(self.property_editor)
        self.loadout_selector = DcsLoadoutSelector(
            flight, self.member_selector.selected_member
        )
        self.loadout_selector.currentIndexChanged.connect(self.on_new_loadout)
        scrolling_layout.addWidget(self.loadout_selector)
        scrolling_layout.addWidget(self.payload_editor)
        scrolling_layout.addWidget(docsText)

        self.setLayout(layout)
        # Increase width of tab when there are long loadout names. Add 50px to loadout selector
        # to account for padding around the selector.
        width = max(
            self.sizeHint().width(), self.loadout_selector.sizeHint().width() + 50
        )
        self.setMinimumWidth(width)

    def resize_for_flight(self) -> None:
        self.member_selector.setMaximum(self.flight.count - 1)

    def reload_from_flight(self) -> None:
        self.loadout_selector.setCurrentText(
            self.member_selector.selected_member.loadout.name
        )

    def rebind_to_selected_member(self) -> None:
        member = self.member_selector.selected_member
        self.property_editor.set_flight_member(member)
        self.loadout_selector.setCurrentText(member.loadout.name)
        self.loadout_selector.setDisabled(member.loadout.is_custom)
        self.payload_editor.set_flight_member(member)
        self.weapon_laser_code_selector.set_flight_member(member)
        self.own_laser_code_info.set_flight_member(member)
        if self.member_selector.value() != 0:
            self.loadout_selector.setDisabled(
                self.flight.use_same_loadout_for_all_members
            )
            self.payload_editor.setDisabled(
                self.flight.use_same_loadout_for_all_members
            )
        else:
            self.loadout_selector.setEnabled(True)
            self.payload_editor.setEnabled(True)

    def loadout_at(self, index: int) -> Loadout:
        loadout = self.loadout_selector.itemData(index)
        if loadout is None:
            return Loadout.empty_loadout()
        return loadout

    def current_loadout(self) -> Loadout:
        loadout = self.loadout_selector.currentData()
        if loadout is None:
            return Loadout.empty_loadout()
        return loadout

    def on_new_loadout(self, index: int) -> None:
        loadout = self.loadout_at(index)
        self.member_selector.selected_member.loadout = loadout
        if self.flight.use_same_loadout_for_all_members:
            self.flight.roster.use_same_loadout_for_all_members()
        self.payload_editor.reset_pylons()

    def on_custom_toggled(self, use_custom: bool) -> None:
        self.loadout_selector.setDisabled(use_custom)
        member = self.member_selector.selected_member
        member.use_custom_loadout = use_custom
        if use_custom:
            member.loadout = member.loadout.derive_custom("Custom")
        else:
            member.loadout = self.current_loadout()
            self.payload_editor.reset_pylons()

        if self.flight.use_same_loadout_for_all_members:
            self.flight.roster.use_same_loadout_for_all_members()

    def on_same_loadout_toggled(self, checked: bool) -> None:
        self.flight.use_same_loadout_for_all_members = checked
        if self.member_selector.value():
            self.loadout_selector.setDisabled(checked)
            self.payload_editor.setDisabled(checked)
        if checked:
            self.flight.roster.use_same_loadout_for_all_members()
            if self.member_selector.value():
                self.rebind_to_selected_member()
        else:
            self.flight.roster.use_distinct_loadouts_for_each_member()
