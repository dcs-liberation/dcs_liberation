from dcs.countries import country_dict
from dcs.country import Country


def country_with_name(name: str) -> Country:
    for country in country_dict.values():
        if country.name == name:
            return country()
    raise KeyError(f"No country found named {name}")
