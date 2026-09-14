from datetime import date, datetime
from typing import Annotated, Literal

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


class AdresObjectDetailQP(BaseModel):
    # Forbid extra query_parameters send through this endpoint
    # model_config = ConfigDict(extra="forbid")
    adresseerbaar_object_identificatie: str | None = None
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    expand: str | None = None
    huidig: bool | None = None


class AdresObjectQP(AdresObjectDetailQP):
    model_config = ConfigDict(use_enum_values=True)  # To access raw string value
    nummeraanduiding_identificatie: str | None = None
    page: int | None = None
    page_size: int | None = None
    bbox: BoundingBox | None = None
    geconstateerd: bool | None = None
    oppervlakte: Oppervlakte | None = None
    gebruiksdoelen: list[enums.Gebruiksdoel] | None = None
    type: enums.Type | None = None
    pand_identificaties: list[str] | None = None


class AdresObjectLvcQP(BaseModel):
    gehele_lvc: bool | None = None


class AdressenDetailQP(BaseModel):
    expand: str | None = None
    inclusief_eindstatus: bool | None = None


class AdressenQP(AdresDetails, AdressenDetailQP):
    zoekresultaat_identificatie: str | None = None
    adresseerbaar_object_identificatie: str | None = None
    woonplaats_naam: str | None = None
    openbare_ruimte_naam: str | None = None
    pand_identificatie: str | None = None
    page: int | None = None
    page_size: int | None = None
    q: str | int | None = None
    openbare_ruimte_identificatie: str | None = None


class AdressenUitgebreidDetailQP(BaseModel):
    inclusief_eindstatus: bool | None = None


class AdressenUitgebreidQP(AdresDetails, AdressenUitgebreidDetailQP):
    adresseerbaar_object_identificatie: str | None = None
    woonplaats_naam: str | None = None
    openbare_ruimte_naam: str | None = None
    page: int | None = None
    page_size: int | None = None
    q: str | int | None = None
    pand_identificatie: str | None = None


class BronhoudersDetailQP(BaseModel):
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None


class BronhoudersQP(BronhoudersDetailQP):
    object_identificatie: str | None = None


class LigplaatsenDetailQP(BaseModel):
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    expand: str | None = None
    huidig: bool | None = None


class LigplaatsenQP(LigplaatsenDetailQP):
    page: int | None = None
    page_size: int | None = None
    point: GeometryPoint | None = None
    bbox: BoundingBox | None = None


class LigplaatsenLvcQP(BaseModel):
    gehele_lvc: bool | None = None


class NummeraanduidingDetailQP(BaseModel):
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    expand: str | None = None
    huidig: bool | None = None


class NummeraanduidingQP(AdresDetails, NummeraanduidingDetailQP):
    woonplaats_naam: str | None = None
    openbare_ruimte_naam: str | None = None
    openbare_ruimte_identificatie: str | None = None
    page: int | None = None
    page_size: int | None = None
    pand_identificatie: str | None = None


class NummeraanduidingLvcQP(BaseModel):
    gehele_lvc: bool | None = None


class OpenbareruimtenDetailQP(BaseModel):
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    expand: str | None = None
    huidig: bool | None = None


class OpenbareruimtenQP(OpenbareruimtenDetailQP):
    woonplaats_naam: str | None = None
    openbare_ruimte_naam: str | None = None
    woonplaats_identificatie: str | None = None
    page: int | None = None
    page_size: int | None = None


class OpenbareruimtenLvcQP(BaseModel):
    gehele_lvc: bool | None = None


class PandenDetailQP(BaseModel):
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    huidig: bool | None = None


class PandenQP(PandenDetailQP):
    model_config = ConfigDict(use_enum_values=True)
    page: int | None = None
    page_size: int | None = None
    point: GeometryPoint | None = None
    bbox: BoundingBox | None = None
    status_pand: list[enums.Status] | None = None
    geconstateerd: bool | None = None
    bouwjaar: Bouwjaar | None = None
    nummeraanduiding_identificatie: str | None = None
    adresseerbaar_object_identificatie: str | None = None


class PandenLvcQP(BaseModel):
    gehele_lvc: bool | None = None


class StandplaatsenDetailQP(BaseModel):
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    huidig: bool | None = None
    expand: str | None = None


class StandplaatsenQP(StandplaatsenDetailQP):
    page: int | None = None
    page_size: int | None = None
    point: GeometryPoint | None = None
    bbox: BoundingBox | None = None


class StandplaatsenLvcQP(BaseModel):
    gehele_lvc: bool | None = None


class VerblijfsobjectenDetailQP(BaseModel):
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    huidig: bool | None = None
    expand: str | None = None


class VerblijfsobjectenQP(VerblijfsobjectenDetailQP):
    model_config = ConfigDict(use_enum_values=True)
    pand_identificatie: str | None = None
    page: int | None = None
    page_size: int | None = None
    bbox: BoundingBox | None = None
    geconstateerd: bool | None = None
    oppervlakte: Oppervlakte | None = None
    gebruiksdoelen: list[enums.Gebruiksdoel] | None = None


class VerblijfsobjectenLvcQP(BaseModel):
    gehele_lvc: bool | None = None


class WoonplaatsenDetailQP(BaseModel):
    geldig_op: date | None = None
    beschikbaar_op: datetime | None = None
    huidig: bool | None = None
    expand: str | None = None


class WoonplaatsenQP(WoonplaatsenDetailQP):
    naam: str | None = None
    page: int | None = None
    page_size: int | None = None
    point: GeometryPoint | None = None
    bbox: BoundingBox | None = None


class WoonplaatsenLvcQP(BaseModel):
    gehele_lvc: bool | None = None
    expand: str | None = None


class WoonplaatsenTimestampLvQP(BaseModel):
    expand: str | None = None


class Oppervlakte(BaseModel):
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
    min: Annotated[int, Field(gte=0)] | None = None
    max: Annotated[int, Field(lte=9999)] | None = None


class GeometryPoint(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float] = Field()


def validate_bbox(bbox: list[float]) -> list[float]:
    ll, lr, ul, ur = bbox[:4]

    # Coordinates are in WSG 84
    if not (-180 <= ll <= 180) and (-180 <= ul <= 180):
        raise ValueError("Longitude must be between -180 and 180.")
    if not (-90 <= lr <= 90) and (-90 <= ur <= 90):
        raise ValueError("Latitude must be between -90 and 90.")
