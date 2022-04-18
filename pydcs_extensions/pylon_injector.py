from typing import Tuple, Any


def inject_pylons(to_pylon: Any, from_pylon: Any) -> None:
    """
    Inject weapons/ordnance added by mods into the pylons of existing aircraft.
    This is done to support mods such as the CJS Super Hornet, which modify aircraft
    that exist in stock DCS. Ornance is injected pydcs aircraft classes via introspection
    :param to_pylon: The pydcs pylon class of the target aircraft
    :param from_pylon: The custom pylon class containing tuples with added weapon info
    :return: None
    """
    for key, value in from_pylon.__dict__.items():
        if key.startswith("__"):
            continue
        if isinstance(value, Tuple):
            setattr(to_pylon, key, value)
