from collections import Iterator
from dataclasses import Field, dataclass, field, fields
from datetime import timedelta
from enum import Enum, unique
from typing import Any, Dict, Optional

from dcs.forcedoptions import ForcedOptions

from .booleanoption import boolean_option
from .boundedfloatoption import bounded_float_option
from .choicesoption import choices_option
from .optiondescription import OptionDescription, SETTING_DESCRIPTION_KEY
from .skilloption import skill_option


@unique
class AutoAtoBehavior(Enum):
    Disabled = "Disabled"
    Never = "Never assign player pilots"
    Default = "No preference"
    Prefer = "Prefer player pilots"


DIFFICULTY_PAGE = "Difficulty"

AI_DIFFICULTY_SECTION = "AI Difficulty"
MISSION_DIFFICULTY_SECTION = "Mission Difficulty"
MISSION_RESTRICTIONS_SECTION = "Mission Restrictions"


@dataclass
class Settings:
    version: Optional[str] = None

    # Difficulty settings
    # AI Difficulty
    player_skill: str = skill_option(
        "Player coalition skill",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        default="Good",
    )
    enemy_skill: str = skill_option(
        "Enemy coalition skill",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        default="Average",
    )
    enemy_vehicle_skill: str = skill_option(
        "Enemy AA and vehicles skill",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        default="Average",
    )
    player_income_multiplier: float = bounded_float_option(
        "Player income multiplier",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        min=0,
        max=5,
        divisor=10,
        default=1.0,
    )
    enemy_income_multiplier: float = bounded_float_option(
        "Enemy income multiplier",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        min=0,
        max=5,
        divisor=10,
        default=1.0,
    )
    invulnerable_player_pilots: bool = boolean_option(
        "Player pilots cannot be killed",
        page=DIFFICULTY_PAGE,
        section=AI_DIFFICULTY_SECTION,
        detail=(
            "Aircraft are vulnerable, but the player's pilot will be returned to the "
            "squadron at the end of the mission"
        ),
        default=True,
    )
    # Mission Difficulty
    manpads: bool = boolean_option(
        "Manpads on frontlines",
        page=DIFFICULTY_PAGE,
        section=MISSION_DIFFICULTY_SECTION,
        default=True,
    )
    night_disabled: bool = boolean_option(
        "No night missions",
        page=DIFFICULTY_PAGE,
        section=MISSION_DIFFICULTY_SECTION,
        default=False,
    )
    # Mission Restrictions
    labels: str = choices_option(
        "In game labels",
        page=DIFFICULTY_PAGE,
        section=MISSION_RESTRICTIONS_SECTION,
        choices=["Full", "Abbreviated", "Dot Only", "Neutral Dot", "Off"],
        default="Full",
    )
    map_coalition_visibility: ForcedOptions.Views = choices_option(
        "Map visibility options",
        page=DIFFICULTY_PAGE,
        section=MISSION_RESTRICTIONS_SECTION,
        choices={
            "All": ForcedOptions.Views.All,
            "Fog of war": ForcedOptions.Views.Allies,
            "Allies only": ForcedOptions.Views.OnlyAllies,
            "Own aircraft only": ForcedOptions.Views.MyAircraft,
            "Map only": ForcedOptions.Views.OnlyMap,
        },
        default=ForcedOptions.Views.All,
    )
    external_views_allowed: bool = boolean_option(
        "Allow external views",
        DIFFICULTY_PAGE,
        MISSION_RESTRICTIONS_SECTION,
        default=True,
    )
    battle_damage_assessment: Optional[bool] = choices_option(
        "Battle damage assessment",
        page=DIFFICULTY_PAGE,
        section=MISSION_RESTRICTIONS_SECTION,
        choices={"Player preference": None, "Enforced on": True, "Enforced off": False},
        default=None,
    )

    # Campaign management
    # General
    restrict_weapons_by_date: bool = False
    disable_legacy_aewc: bool = True
    disable_legacy_tanker: bool = True
    # Pilots and Squadrons
    ai_pilot_levelling: bool = True
    #: Feature flag for squadron limits.
    enable_squadron_pilot_limits: bool = False
    #: The maximum number of pilots a squadron can have at one time. Changing this after
    #: the campaign has started will have no immediate effect; pilots already in the
    #: squadron will not be removed if the limit is lowered and pilots will not be
    #: immediately created if the limit is raised.
    squadron_pilot_limit: int = 12
    #: The number of pilots a squadron can replace per turn.
    squadron_replenishment_rate: int = 4
    # HQ Automation
    automate_runway_repair: bool = False
    automate_front_line_reinforcements: bool = False
    automate_aircraft_reinforcements: bool = False
    auto_ato_behavior: AutoAtoBehavior = AutoAtoBehavior.Default
    auto_ato_player_missions_asap: bool = True
    automate_front_line_stance: bool = True
    reserves_procurement_target: int = 10

    # Mission Generator
    # Gameplay
    supercarrier: bool = False
    generate_marks: bool = True
    generate_dark_kneeboard: bool = False
    never_delay_player_flights: bool = False
    default_start_type: str = "Cold"
    # Mission specific
    desired_player_mission_duration: timedelta = timedelta(minutes=60)
    # Performance
    perf_smoke_gen: bool = True
    perf_smoke_spacing = 1600
    perf_red_alert_state: bool = True
    perf_artillery: bool = True
    perf_moving_units: bool = True
    perf_infantry: bool = True
    perf_destroyed_units: bool = True
    # Performance culling
    perf_culling: bool = False
    perf_culling_distance: int = 100
    perf_do_not_cull_carrier = True

    # Cheating
    show_red_ato: bool = False
    enable_frontline_cheats: bool = False
    enable_base_capture_cheat: bool = False

    # LUA Plugins system
    plugins: Dict[str, bool] = field(default_factory=dict)

    only_player_takeoff: bool = True  # Legacy parameter do not use

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

    def __setstate__(self, state: dict[str, Any]) -> None:
        # __setstate__ is called with the dict of the object being unpickled. We
        # can provide save compatibility for new settings options (which
        # normally would not be present in the unpickled object) by creating a
        # new settings object, updating it with the unpickled state, and
        # updating our dict with that.
        new_state = Settings().__dict__
        new_state.update(state)
        self.__dict__.update(new_state)

    @classmethod
    def _field_description(cls, settings_field: Field[Any]) -> OptionDescription:
        return settings_field.metadata[SETTING_DESCRIPTION_KEY]

    @classmethod
    def pages(cls) -> Iterator[str]:
        seen: set[str] = set()
        for settings_field in cls._user_fields():
            description = cls._field_description(settings_field)
            if description.page not in seen:
                yield description.page
                seen.add(description.page)

    @classmethod
    def sections(cls, page: str) -> Iterator[str]:
        seen: set[str] = set()
        for settings_field in cls._user_fields():
            description = cls._field_description(settings_field)
            if description.page == page and description.section not in seen:
                yield description.section
                seen.add(description.section)

    @classmethod
    def fields(cls, page: str, section: str) -> Iterator[tuple[str, OptionDescription]]:
        for settings_field in cls._user_fields():
            description = cls._field_description(settings_field)
            if description.page == page and description.section == section:
                yield settings_field.name, description

    @classmethod
    def _user_fields(cls) -> Iterator[Field[Any]]:
        for settings_field in fields(cls):
            if SETTING_DESCRIPTION_KEY in settings_field.metadata:
                yield settings_field
