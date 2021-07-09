from .event import Event


class FrontlineAttackEvent(Event):
    """
    An event centered on a FrontLine Conflict.
    Currently the same as its parent, but here for legacy compatibility as well as to allow for
    future unique Event handling
    """

    def __str__(self) -> str:
        return "Frontline attack"
