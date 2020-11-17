from dataclasses import dataclass
from enum import Enum
from typing import Optional, Mapping
from types import MappingProxyType


class Locale(str, Enum):
    EN_US: str = "en_US"
    CN: str = "CN"


@dataclass
class LocaleModel:
    lang_desc: Mapping[Locale, str] = MappingProxyType(
        {
            Locale.EN_US: "US English",
            Locale.CN: "Chinese",
        }
    )


class Localize:
    """Methods for describing and fetching localization options"""
    locale: Locale = Locale.EN_US

    @staticmethod
    def lang_desc(locale: Locale) -> str:
        return LocaleModel.lang_desc[locale]

    @staticmethod
    def get_locale_from_desc(desc: str) -> Locale:
        for k, v in LocaleModel.lang_desc.items():
            print(f"LOCALE: {k}, {v}", desc)
            if v == desc:
                return k
        raise RuntimeWarning(f"No mapped Locale exists for description <{desc}>")

    @classmethod
    def locale_str(cls) -> str:
        return cls.locale.value
