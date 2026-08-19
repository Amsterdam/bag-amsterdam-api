from enum import StrEnum


class StrChoicesEnum(StrEnum):
    """Implemented choices method for easy conversion to tuples used in Django Models."""

    @classmethod
    def choices(cls, upper: bool = False):
        if upper:
            return tuple(
                (cls[item].value, item.upper().replace("_", " ")) for item in list(cls.__members__)
            )
        return tuple(
            (cls[item].value, item.lower().replace("_", " ").capitalize())
            for item in list(cls.__members__)
        )


class Gebruiksdoel(StrChoicesEnum):
    WOONFUNCTIE = "WOON"
    BIJEENKOMSTFUNCTIE = "B"
    CELFUNCTIE = "C"
    GEZONDHEIDSZORGFUNCTIE = "G"
    INDUSTRIEFUNCTIE = "I"
    KANTOORFUNCTIE = "K"
    LOGIESFUNCTIE = "L"
    ONDERWIJSFUNCTIE = "O"
    SPORTFUNCTIE = "S"
    WINKELFUNCTIE = "WINK"
    OVERIGE_GEBRUIKSFUNCTIE = "O"


class Type(StrChoicesEnum):
    VERBLIJFSOBJECT = "V"
    STANDPLAATS = "S"
    LIGPLAATS = "L"


class Status(StrChoicesEnum):
    BOUWVERGUNNING_VERLEEND = "BV"
    NIET_GEREALISEERD_PAND = "NG"
    BOUW_GESTART = "BG"
    PAND_IN_GEBRUIK_NIET_INGEMETEN = "PGN"
    PAND_IN_GEBRUIK = "PIG"
    VERBOUWING_PAND = "VP"
    SLOOPVERGUNNING_VERLEEND = "SV"
    PAND_GESLOOPT = "PG"
    PAND_BUITEN_GEBRUIK = "PB"
    PAND_TEN_ONRECHTE_OPGEVOERD = "PO"
