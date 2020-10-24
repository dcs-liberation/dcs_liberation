from typing import Dict


class Settings:

    def __init__(self):
        # Generator settings
        self.inverted = False
        self.do_not_generate_carrier = False # TODO : implement
        self.do_not_generate_lha = False     # TODO : implement
        self.do_not_generate_player_navy = True          # TODO : implement
        self.do_not_generate_enemy_navy = True           # TODO : implement

        # Difficulty settings
        self.player_skill = "Good"
        self.enemy_skill = "Average"
        self.enemy_vehicle_skill = "Average"
        self.map_coalition_visibility = "All Units"
        self.labels = "Full"
        self.only_player_takeoff = True  # Legacy parameter do not use
        self.night_disabled = False
        self.external_views_allowed = True
        self.supercarrier = False
        self.multiplier = 1
        self.generate_marks = True
        self.sams = True # Legacy parameter do not use
        self.cold_start = False # Legacy parameter do not use
        self.version = None

        # Performance oriented
        self.perf_red_alert_state = True
        self.perf_smoke_gen = True
        self.perf_artillery = True
        self.perf_moving_units = True
        self.perf_infantry = True
        self.perf_ai_parking_start = True
        self.perf_destroyed_units = True

        # Performance culling
        self.perf_culling = False
        self.perf_culling_distance = 100

        # LUA Plugins system
        self.plugins: Dict[str, bool] = {}

        # Cheating
        self.show_red_ato = False

        self.never_delay_player_flights = False

    @staticmethod
    def plugin_settings_key(identifier: str) -> str:
        return f"plugins.{identifier}"

    def initialize_plugin_option(self, identifier: str,
                                 default_value: bool) -> None:
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
