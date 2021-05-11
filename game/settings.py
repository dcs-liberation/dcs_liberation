from dataclasses import dataclass, field
from datetime import timedelta
from typing import Dict, Optional

from dcs.forcedoptions import ForcedOptions


@dataclass
class Settings:

    # Difficulty settings
    player_skill: str = "Good"
    enemy_skill: str = "Average"
    enemy_vehicle_skill: str = "Average"
    map_coalition_visibility: ForcedOptions.Views = ForcedOptions.Views.All
    labels: str = "Full"
    only_player_takeoff: bool = True  # Legacy parameter do not use
    night_disabled: bool = False
    external_views_allowed: bool = True
    supercarrier: bool = False
    generate_marks: bool = True
    manpads: bool = True
    version: Optional[str] = None
    player_income_multiplier: float = 1.0
    enemy_income_multiplier: float = 1.0

    default_start_type: str = "Cold"

    # Mission specific
    desired_player_mission_duration: timedelta = 90

    # Campaign management
    automate_runway_repair: bool = False
    automate_front_line_reinforcements: bool = False
    automate_aircraft_reinforcements: bool = False
    restrict_weapons_by_date: bool = False
    disable_legacy_aewc: bool = False
    generate_dark_kneeboard: bool = False

    #: Feature flag for new ground unit behavior. Old campaigns are will not work with
    #: this so the old behavior remains an option until it breaks, at which point we'll
    #: remove it.
    enable_new_ground_unit_recruitment: bool = True

    # Performance oriented
    perf_red_alert_state: bool = True
    perf_smoke_gen: bool = True
    perf_smoke_spacing = 1600
    perf_artillery: bool = True
    perf_moving_units: bool = True
    perf_infantry: bool = True
    perf_destroyed_units: bool = True

    # Performance culling
    perf_culling: bool = False
    perf_culling_distance: int = 100
    perf_do_not_cull_carrier = True

    # LUA Plugins system
    plugins: Dict[str, bool] = field(default_factory=dict)

    # Cheating
    show_red_ato: bool = False
    enable_frontline_cheats: bool = False
    enable_base_capture_cheat: bool = False

    never_delay_player_flights: bool = False

    @staticmethod
    def plugin_settings_key(identifier: str) -> str:
        return f"plugins.{identifier}"

    def initialize_plugin_option(self, identifier: str, default_value: bool) -> None:
        try:
            self.plugin_option(identifier)
        except KeyError:
            self.set_plugin_option(identifier, default_value)

    def plugin_option(self, identifier: str) -> bool:
        return self.plugins[self.plugin_settings_key(identifier)]

    def set_plugin_option(self, identifier: str, enabled: bool) -> None:
        self.plugins[self.plugin_settings_key(identifier)] = enabled

    def __setstate__(self, state) -> None:
        # __setstate__ is called with the dict of the object being unpickled. We
        # can provide save compatibility for new settings options (which
        # normally would not be present in the unpickled object) by creating a
        # new settings object, updating it with the unpickled state, and
        # updating our dict with that.
        new_state = Settings().__dict__
        new_state.update(state)
        self.__dict__.update(new_state)
