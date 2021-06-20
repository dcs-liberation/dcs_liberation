from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum, unique
from typing import Dict, Optional

from dcs.forcedoptions import ForcedOptions


@unique
class AutoAtoBehavior(Enum):
    Disabled = "Disabled"
    Never = "Never assign player pilots"
    Default = "No preference"
    Prefer = "Prefer player pilots"


@dataclass
class Settings:

    # Difficulty settings
    player_skill: str = "Good"
    enemy_skill: str = "Average"
    ai_pilot_levelling: bool = True
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

    #: Feature flag for squadron limits.
    enable_squadron_pilot_limits: bool = False

    #: The maximum number of pilots a squadron can have at one time. Changing this after
    #: the campaign has started will have no immediate effect; pilots already in the
    #: squadron will not be removed if the limit is lowered and pilots will not be
    #: immediately created if the limit is raised.
    squadron_pilot_limit: int = 12

    #: The number of pilots a squadron can replace per turn.
    squadron_replenishment_rate: int = 4

    default_start_type: str = "Cold"

    # Mission specific
    desired_player_mission_duration: timedelta = timedelta(minutes=60)

    # Campaign management
    automate_runway_repair: bool = False
    automate_front_line_reinforcements: bool = False
    automate_aircraft_reinforcements: bool = False
    restrict_weapons_by_date: bool = False
    disable_legacy_aewc: bool = True
    disable_legacy_tanker: bool = True
    generate_dark_kneeboard: bool = False
    invulnerable_player_pilots: bool = True
    auto_ato_behavior: AutoAtoBehavior = AutoAtoBehavior.Default
    auto_ato_player_missions_asap: bool = True

    # Performance oriented
    perf_red_alert_state: bool = True
    perf_smoke_gen: bool = True
    perf_smoke_spacing = 1600
    perf_artillery: bool = True
    perf_moving_units: bool = True
    perf_infantry: bool = True
    perf_destroyed_units: bool = True
    reserves_procurement_target: int = 10

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


@dataclass
class ModSettings:
    # Aircraft Mods
    a4_skyhawk: bool = False
    f22_raptor: bool = False
    hercules: bool = False
    jas39_gripen: bool = False
    su57_felon: bool = False
    # Ground Asset Mods
    frenchpack: bool = False
    high_digit_sams: bool = False
