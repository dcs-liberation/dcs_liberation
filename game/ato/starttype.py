from enum import Enum, unique


@unique
class StartType(Enum):
    """The start type for a Flight.

    This is distinct from dcs.mission.StartType because we need a fourth state:
    IN_FLIGHT.
    """

    COLD = "Cold"
    WARM = "Warm"
    RUNWAY = "Runway"
    IN_FLIGHT = "In Flight"
