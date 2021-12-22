from collections.abc import Iterator
from dataclasses import Field, dataclass, field, fields
from datetime import timedelta
from enum import Enum, unique
from typing import Any, Dict, Optional

from dcs.forcedoptions import ForcedOptions

from .booleanoption import boolean_option
from .boundedfloatoption import bounded_float_option
from .boundedintoption import bounded_int_option
from .choicesoption import choices_option
from .minutesoption import minutes_option
from .optiondescription import OptionDescription, SETTING_DESCRIPTION_KEY
from .skilloption import skill_option
from ..ato.starttype import StartType


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

CAMPAIGN_MANAGEMENT_PAGE = "Campaign Management"

GENERAL_SECTION = "General"
PILOTS_AND_SQUADRONS_SECTION = "Pilots and Squadrons"
HQ_AUTOMATION_SECTION = "HQ Automation"

MISSION_GENERATOR_PAGE = "Mission Generator"

GAMEPLAY_SECTION = "Gameplay"

# TODO: Make sections a type and add headers.
# This section had the header: "Disabling settings below may improve performance, but
# will impact the overall quality of the experience."
PERFORMANCE_SECTION = "Performance"


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

    easy_communication: Optional[bool] = choices_option(
        "Easy Communication",
        page=DIFFICULTY_PAGE,
        section=MISSION_RESTRICTIONS_SECTION,
        choices={"Player preference": None, "Enforced on": True, "Enforced off": False},
        default=None,
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
    restrict_weapons_by_date: bool = boolean_option(
        "Restrict weapons by date (WIP)",
        page=CAMPAIGN_MANAGEMENT_PAGE,
        section=GENERAL_SECTION,
        default=False,
        detail=(
            "Restricts weapon availability based on the campaign date. Data is "
            "extremely incomplete so does not affect all weapons."
        ),
    )
    disable_legacy_aewc: bool = boolean_option(
        "Spawn invulnerable, always-available AEW&C aircraft (deprecated)",
        page=CAMPAIGN_MANAGEMENT_PAGE,
        section=GENERAL_SECTION,
        default=True,
        invert=True,
        detail=(
            "If checked, an invulnerable friendly AEW&C aircraft that begins the "
            "mission on station will be be spawned. This behavior will be removed in a "
            "future release."
        ),
    )
    disable_legacy_tanker: bool = boolean_option(
        "Spawn invulnerable, always-available tanker aircraft (deprecated)",
        page=CAMPAIGN_MANAGEMENT_PAGE,
        section=GENERAL_SECTION,
        default=True,
        invert=True,
        detail=(
            "If checked, an invulnerable friendly tanker aircraft that begins the "
            "mission on station will be be spawned. This behavior will be removed in a "
            "future release."
        ),
    )
    # Pilots and Squadrons
    ai_pilot_levelling: bool = boolean_option(
        "Allow AI pilot leveling",
        CAMPAIGN_MANAGEMENT_PAGE,
        PILOTS_AND_SQUADRONS_SECTION,
        default=True,
        detail=(
            "Set whether or not AI pilots will level up after completing a number of"
            " sorties. Since pilot level affects the AI skill, you may wish to disable"
            " this, lest you face an Ace!"
        ),
    )
    #: Feature flag for squadron limits.
    enable_squadron_pilot_limits: bool = boolean_option(
        "Enable per-squadron pilot limits (WIP)",
        CAMPAIGN_MANAGEMENT_PAGE,
        PILOTS_AND_SQUADRONS_SECTION,
        default=False,
        detail=(
            "If set, squadrons will be limited to a maximum number of pilots and dead "
            "pilots will replenish at a fixed rate, each defined with the settings"
            "below. Auto-purchase may buy aircraft for which there are no pilots"
            "available, so this feature is still a work-in-progress."
        ),
    )
    #: The maximum number of pilots a squadron can have at one time. Changing this after
    #: the campaign has started will have no immediate effect; pilots already in the
    #: squadron will not be removed if the limit is lowered and pilots will not be
    #: immediately created if the limit is raised.
    squadron_pilot_limit: int = bounded_int_option(
        "Maximum number of pilots per squadron",
        CAMPAIGN_MANAGEMENT_PAGE,
        PILOTS_AND_SQUADRONS_SECTION,
        default=12,
        min=12,
        max=72,
        detail=(
            "Sets the maximum number of pilots a squadron may have active. "
            "Changing this value will not have an immediate effect, but will alter "
            "replenishment for future turns."
        ),
    )
    #: The number of pilots a squadron can replace per turn.
    squadron_replenishment_rate: int = bounded_int_option(
        "Squadron pilot replenishment rate",
        CAMPAIGN_MANAGEMENT_PAGE,
        PILOTS_AND_SQUADRONS_SECTION,
        default=4,
        min=1,
        max=20,
        detail=(
            "Sets the maximum number of pilots that will be recruited to each squadron "
            "at the end of each turn. Squadrons will not recruit new pilots beyond the "
            "pilot limit, but each squadron with room for more pilots will recruit "
            "this many pilots each turn up to the limit."
        ),
    )

    # HQ Automation
    automate_runway_repair: bool = boolean_option(
        "Automate runway repairs",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=False,
    )
    automate_front_line_reinforcements: bool = boolean_option(
        "Automate front-line purchases",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=False,
    )
    automate_aircraft_reinforcements: bool = boolean_option(
        "Automate aircraft purchases",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=False,
    )
    auto_ato_behavior: AutoAtoBehavior = choices_option(
        "Automatic package planning behavior",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=AutoAtoBehavior.Default,
        choices={v.value: v for v in AutoAtoBehavior},
        detail=(
            "Aircraft auto-purchase is directed by the auto-planner, so disabling "
            "auto-planning disables auto-purchase."
        ),
    )
    auto_ato_player_missions_asap: bool = boolean_option(
        "Automatically generated packages with players are scheduled ASAP",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=True,
    )
    automate_front_line_stance: bool = boolean_option(
        "Automatically manage front line stances",
        CAMPAIGN_MANAGEMENT_PAGE,
        HQ_AUTOMATION_SECTION,
        default=True,
    )
    reserves_procurement_target: int = 10

    # Mission Generator
    # Gameplay
    fast_forward_to_first_contact: bool = boolean_option(
        "Fast forward mission to first contact (WIP)",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=False,
        detail=(
            "If enabled, the mission will be generated at the point of first contact."
        ),
    )
    player_mission_interrupts_sim_at: Optional[StartType] = choices_option(
        "Player missions interrupt fast forward",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=None,
        choices={
            "Never": None,
            "At startup time": StartType.COLD,
            "At taxi time": StartType.WARM,
            "At takeoff time": StartType.RUNWAY,
        },
        detail=(
            "Determines what player mission states will interrupt fast-forwarding to "
            "first contact, if enabled. If never is selected player missions will not "
            "impact simulation and player missions may be generated mid-flight. The "
            "other options will cause the mission to be generated as soon as a player "
            "mission reaches the set state or at first contact, whichever comes first."
        ),
    )
    auto_resolve_combat: bool = boolean_option(
        "Auto-resolve combat during fast-forward (WIP)",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=False,
        detail=(
            "If enabled, aircraft entering combat during fast forward will have their "
            "combat auto-resolved after a period of time. This allows the simulation "
            "to advance further into the mission before requiring mission generation, "
            "but simulation is currently very rudimentary so may result in huge losses."
        ),
    )
    supercarrier: bool = boolean_option(
        "Use supercarrier module",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=False,
    )
    generate_marks: bool = boolean_option(
        "Put objective markers on the map",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=True,
    )
    generate_dark_kneeboard: bool = boolean_option(
        "Generate dark kneeboard",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=False,
        detail=(
            "Dark kneeboard for night missions. This will likely make the kneeboard on "
            "the pilot leg unreadable."
        ),
    )
    never_delay_player_flights: bool = boolean_option(
        "Player flights ignore TOT and spawn immediately",
        MISSION_GENERATOR_PAGE,
        GAMEPLAY_SECTION,
        default=False,
        detail=(
            "Does not adjust package waypoint times. Should not be used if players "
            "have runway or in-air starts."
        ),
        tooltip=(
            "Always spawns player aircraft immediately, even if their start time is "
            "more than 10 minutes after the start of the mission. <strong>This does "
            "not alter the timing of your mission. Your TOT will not change. This "
            "option only allows the player to wait on the ground.</strong>"
        ),
    )
    default_start_type: StartType = choices_option(
        "Default start type for AI aircraft",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        choices={v.value: v for v in StartType},
        default=StartType.COLD,
        detail=(
            "Warning: Options other than Cold will significantly reduce the number of "
            "targets available for OCA/Aircraft missions, and OCA/Aircraft flights "
            "will not be included in automatically planned OCA packages."
        ),
    )
    # Mission specific
    desired_player_mission_duration: timedelta = minutes_option(
        "Desired mission duration",
        page=MISSION_GENERATOR_PAGE,
        section=GAMEPLAY_SECTION,
        default=timedelta(minutes=60),
        min=30,
        max=150,
    )

    # Performance
    perf_smoke_gen: bool = boolean_option(
        "Smoke visual effect on the front line",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_smoke_spacing: int = bounded_int_option(
        "Smoke generator spacing (higher means less smoke)",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=1600,
        min=800,
        max=24000,
    )
    perf_red_alert_state: bool = boolean_option(
        "SAM starts in red alert mode",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_artillery: bool = boolean_option(
        "Artillery strikes",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_moving_units: bool = boolean_option(
        "Moving ground units",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    convoys_travel_full_distance: bool = boolean_option(
        "Convoys drive the full distance between control points",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_infantry: bool = boolean_option(
        "Generate infantry squads alongside vehicles",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_destroyed_units: bool = boolean_option(
        "Generate carcasses for units destroyed in previous turns",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    # Performance culling
    perf_culling: bool = boolean_option(
        "Culling of distant units enabled",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=False,
    )
    perf_culling_distance: int = bounded_int_option(
        "Culling distance (km)",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=100,
        min=10,
        max=10000,
        causes_expensive_game_update=True,
    )
    perf_do_not_cull_threatening_iads: bool = boolean_option(
        "Do not cull threatening IADS",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
    )
    perf_do_not_cull_carrier: bool = boolean_option(
        "Do not cull carrier's surroundings",
        page=MISSION_GENERATOR_PAGE,
        section=PERFORMANCE_SECTION,
        default=True,
        causes_expensive_game_update=True,
    )

    # Cheating. Not using auto settings because the same page also has buttons which do
    # not alter settings.
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
