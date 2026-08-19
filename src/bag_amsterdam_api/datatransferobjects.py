from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator

from bag_amsterdam_api.bevragingen import enums

BoundingBox = Annotated[list[float], Field(min_length=4, max_length=6)]


class AdresDetails(BaseModel):
    """These query parameters always appear in combination"""

    postcode: str | None = None
    huisnummer: int | None = None
    huisnummertoevoeging: str | None = None
    huisletter: str | None = None
    exacte_match: bool | None = None


class AdresObjectDetailFilter(BaseModel):
    # Forbid extra query_parameters send through this /adres/{id} endpoint
    model_config = ConfigDict(extra="forbid")
    # AdressFilter.model_validate({
    #     "street": "Main Street",
    #     "foo": "bar",
    # })
    # --> ValidationError: Extra inputs are not permitted
    adresseerbaar_object_identificatie: str | None = None
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    expand: str | None = None
    huidig: bool | None = None


class AdresObjectFilter(AdresObjectDetailFilter):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)  # To access raw string value
    nummeraanduiding_identificatie: str | None = None
    page: int | None = None
    page_size: int | None = None
    bbox: BoundingBox | None = None
    geconstateerd: bool | None = None
    oppervlakte: Oppervlakte | None = None
    gebruiksdoelen: list[enums.Gebruiksdoel] | None = None
    type: enums.Type | None = None
    pand_identificaties: list[str] | None = None


class AdresObjectLvcFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gehele_lvc: bool | None = None


class AdressenDetailFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expand: str | None = None
    inclusief_eindstatus: bool | None = None


class AdressenFilter(AdresDetails, AdressenDetailFilter):
    model_config = ConfigDict(extra="forbid")
    zoekresultaat_identificatie: str | None = None
    adresseerbaar_object_identificatie: str | None = None
    woonplaats_naam: str | None = None
    openbare_ruimte_naam: str | None = None
    pand_identificatie: str | None = None
    page: int | None = None
    page_size: int | None = None
    q: str | int | None = None
    openbare_ruimte_identificatie: str | None = None


class AdressenUitgebreidDetailFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    inclusief_eindstatus: bool | None = None


class AdressenUitgebreidFilter(AdresDetails, AdressenUitgebreidDetailFilter):
    model_config = ConfigDict(extra="forbid")
    adresseerbaar_object_identificatie: str | None = None
    woonplaats_naam: str | None = None
    openbare_ruimte_naam: str | None = None
    page: int | None = None
    page_size: int | None = None
    q: str | int | None = None
    pand_identificatie: str | None = None


class BronhoudersDetailFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None


class BronhoudersFilter(BronhoudersDetailFilter):
    model_config = ConfigDict(extra="forbid")
    object_identificatie: str | None = None


class LigplaatsenDetailFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    expand: str | None = None
    huidig: bool | None = None


class LigplaatsenFilter(LigplaatsenDetailFilter):
    model_config = ConfigDict(extra="forbid")
    page: int | None = None
    page_size: int | None = None
    point: GeometryPoint | None = None
    bbox: BoundingBox | None = None


class LigplaatsenLvcFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gehele_lvc: bool | None = None


class NummeraanduidingDetailFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    expand: str | None = None
    huidig: bool | None = None


class NummeraanduidingFilter(AdresDetails, NummeraanduidingDetailFilter):
    model_config = ConfigDict(extra="forbid")
    woonplaats_naam: str | None = None
    openbare_ruimte_naam: str | None = None
    openbare_ruimte_identificatie: str | None = None
    page: int | None = None
    page_size: int | None = None
    pand_identificatie: str | None = None


class NummeraanduidingLvcFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gehele_lvc: bool | None = None


class OpenbareruimtenDetailFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    expand: str | None = None
    huidig: bool | None = None


class OpenbareruimtenFilter(OpenbareruimtenDetailFilter):
    model_config = ConfigDict(extra="forbid")
    woonplaats_naam: str | None = None
    openbare_ruimte_naam: str | None = None
    woonplaats_identificatie: str | None = None
    page: int | None = None
    page_size: int | None = None


class OpenbareruimtenLvcFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gehele_lvc: bool | None = None


class PandenDetailFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    huidig: bool | None = None


class PandenFilter(PandenDetailFilter):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)
    page: int | None = None
    page_size: int | None = None
    point: GeometryPoint | None = None
    bbox: BoundingBox | None = None
    status_pand: list[enums.Status] | None = None
    geconstateerd: bool | None = None
    bouwjaar: Bouwjaar | None = None
    nummeraanduiding_identificatie: str | None = None
    adresseerbaar_object_identificatie: str | None = None


class PandenLvcFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gehele_lvc: bool | None = None


class StandplaatsenDetailFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    huidig: bool | None = None
    expand: str | None = None


class StandplaatsenFilter(StandplaatsenDetailFilter):
    model_config = ConfigDict(extra="forbid")
    page: int | None = None
    page_size: int | None = None
    point: GeometryPoint | None = None
    bbox: BoundingBox | None = None


class StandplaatsenLvcFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gehele_lvc: bool | None = None


class VerblijfsobjectenDetailFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    huidig: bool | None = None
    expand: str | None = None


class VerblijfsobjectenFilter(VerblijfsobjectenDetailFilter):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)
    pand_identificatie: str | None = None
    page: int | None = None
    page_size: int | None = None
    bbox: BoundingBox | None = None
    geconstateerd: bool | None = None
    oppervlakte: Oppervlakte | None = None
    gebruiksdoelen: list[enums.Gebruiksdoel] | None = None


class VerblijfsobjectenLvcFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gehele_lvc: bool | None = None


class WoonplaatsenDetailFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    huidig: bool | None = None
    expand: str | None = None


class WoonplaatsenFilter(WoonplaatsenDetailFilter):
    model_config = ConfigDict(extra="forbid")
    naam: str | None = None
    page: int | None = None
    page_size: int | None = None
    point: GeometryPoint | None = None
    bbox: BoundingBox | None = None


class WoonplaatsenLvcFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gehele_lvc: bool | None = None
    expand: str | None = None


class WoonplaatsenTimestampLvFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    expand: str | None = None


class Oppervlakte(BaseModel):
    """Geef de minimale en maximale oppervlakte op waarbinnen je wilt zoeken (in m2).
    Alleen verblijfsobjecten hebben een oppervlakte en kunnen met deze parameter worden gevonden.
    Ligplaatsen en standplaatsen hebben geen oppervlakte en kunnen met deze parameter niet
    worden gevonden. De oppervlakte van een verblijfsobject is een natuurlijk getal tussen 1
    (minimaal) en 999999 (maximaal). Het is niet toegestaan voor min een grotere waarde op te
    geven dan voor max. Is min > max dan treedt een foutmelding op.
    Bv: oppervlakte[min]=100&oppervlakte[max]=200"""

    min: Annotated[int, Field(gt=1, lt=1000000)] | None = None
    max: Annotated[int, Field(gt=1, lt=1000000)] | None = None

    @model_validator(mode="after")
    def validate(self) -> Oppervlakte:
        if self.min > self.max:
            raise ValueError(
                f"Minimum surface ({self.min}) cannot be larger than maximum surface ({self.max})."
            )
        return self


class Bouwjaar(BaseModel):
    """Bouwjaar van het pand. Geeft het minimale en/of maximale bouwjaar aan van het pand
    waarnaar moet worden gezocht. Een bouwjaar is een natuurlijk getal tussen 0 (minimaal)
    en 9999 (maximaal). Bv: bouwjaar[min]=1970&bouwjaar[max]=2010"""

    min: Annotated[int, Field(gte=0)] | None = None
    max: Annotated[int, Field(lte=9999)] | None = None


class GeometryPoint(BaseModel):
    """Punt conform OGC API Features standaard. Met de content-crs header wordt aangegeven in
    welk CRS de coördinaten van het punt is. Example : OrderedMap { "type": "Point",
    "coordinates": List [ 196733.51, 439931.89 ] }
    """


def validate_bbox(bbox: list[float]) -> list[float]:
    """Met de content-crs header wordt aangegeven in welk CRS de coördinaten van de bbox zijn.
    Coördinaten worden als volgt opgegeven: linksonder x, linksonder y, rechtsboven x,
    rechtsboven y. De oppervlakte van de bounding box mag maximaal 250.000 vierkante meter zijn.
    """
    ll, lr, ul, ur = bbox[:4]

    # Coordinates are in WSG 84
    if not (-180 <= ll <= 180) and (-180 <= ul <= 180):
        raise ValueError("Longitude must be between -180 and 180.")
    if not (-90 <= lr <= 90) and (-90 <= ur <= 90):
        raise ValueError("Latitude must be between -90 and 90.")
