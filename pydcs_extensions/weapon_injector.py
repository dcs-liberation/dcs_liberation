from typing import List, Any

from dcs.weapons_data import Weapons, weapon_ids


def inject_weapons(weapon_class: Any) -> None:
    """
    Inject custom weapons from mods into pydcs weapons databases via introspection
    :param weapon_class: The custom weapons class containing dictionaries with weapon info
    :return: None
    """
    for key, value in weapon_class.__dict__.items():
        if key.startswith("__"):
            continue
        if isinstance(value, dict) and value.get("clsid"):
            setattr(Weapons, key, value)
            weapon_ids[value["clsid"]] = value
