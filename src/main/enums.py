from enum import StrEnum


class Language(StrEnum):
    COR = "Cornish"
    GV = "Manx"
    BR = "Breton"
    IU = "Inuktitut"
    KL = "Kalaallisut"
    ROM = "Romani"
    OC = "Occitan"
    LAD = "Ladino"
    SE = "Northern Sami"
    HSB = "Upper Sorbian"
    CSB = "Kashubian"
    ZZA = "Zazaki"
    CV = "Chuvash"
    LIV = "Livonian"
    TSK = "Tsakonian"
    SRM = "Saramaccan"
    BI = "Bislama"

    @classmethod
    def exists(cls, value: str) -> bool:
        return value in cls._value2member_map_
