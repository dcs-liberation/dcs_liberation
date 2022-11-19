from dataclasses import dataclass


@dataclass(frozen=True)
class UiFlags:
    """Flags for the UI that are not exposed in settings.

    These flags are hidden from the settings UI because they can only be controlled from
    the command-line during startup.
    """

    # True if the front-end should connect to the development react webserver instead of
    # the built front-end app.
    dev_ui_webserver: bool

    # True if the play/pause/speed controls should be visible in the top panel.
    show_sim_speed_controls: bool
