from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

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
    oppervlakte_min: int | None = Field(
        default=None,
        validation_alias="oppervlakte[min]",
        gte=0,
    )
    oppervlakte_max: int | None = Field(
        default=None,
        validation_alias="oppervlakte[max]",
        lte=999999,
    )
    gebruiksdoelen: enums.Gebruiksdoel | None = None
    type: enums.Type | None = None
    pand_identificaties: list[str] | None = None

    # boundingbox is passed like bbox=196733.51,439931.89,196833.51,440031.89
    @field_validator("bbox", mode="before")
    @classmethod
    def parse_bbox(cls, v):
        if isinstance(v, str):
            return [float(x) for x in v.split(",")]
        return v

    @model_validator(mode="after")
    def validate_oppervlakte(self):
        if (
            self.oppervlakte_min is not None
            and self.oppervlakte_max is not None
            and self.oppervlakte_min > self.oppervlakte_max
        ):
            raise ValueError(
                f"Minimum surface ({self.oppervlakte_min}) cannot be larger than "
                f"maximum surface ({self.oppervlakte_max})"
            )
        return self


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
    status_pand: enums.Status | None = None
    geconstateerd: bool | None = None
    bouwjaar_min: int | None = Field(default=None, validation_alias="bouwjaar[min]", gte=0)
    bouwjaar_max: int | None = Field(
        default=None,
        validation_alias="bouwjaar[max]",
        lte=9999,
    )
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
    oppervlakte_min: int | None = Field(
        default=None,
        validation_alias="oppervlakte[min]",
        gte=0,
    )
    oppervlakte_max: int | None = Field(
        default=None,
        validation_alias="oppervlakte[max]",
        lte=999999,
    )
    gebruiksdoelen: enums.Gebruiksdoel | None = None

    @field_validator("bbox", mode="before")
    @classmethod
    def parse_bbox(cls, v):
        if isinstance(v, str):
            return [float(x) for x in v.split(",")]
        return v

    @model_validator(mode="after")
    def validate_oppervlakte(self):
        if (
            self.oppervlakte_min is not None
            and self.oppervlakte_max is not None
            and self.oppervlakte_min > self.oppervlakte_max
        ):
            raise ValueError(
                f"Minimum surface ({self.oppervlakte_min}) cannot be larger than "
                f"maximum surface ({self.oppervlakte_max})"
            )
        return self


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


class GeometryPoint(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float]

    @model_validator(mode="before")
    @classmethod
    def parse_query_param(cls, value):
        if isinstance(value, str):
            parts = value.split(",")

            if len(parts) != 5:
                raise ValueError("Invalid Point query parameter")

            if parts[:3] != ["type", "Point", "coordinates"]:
                raise ValueError("Invalid Point query parameter")

            return {
                "type": parts[1],
                "coordinates": (float(parts[3]), float(parts[4])),
            }

        return value

    def to_query_param(self) -> str:
        # point is passed like point=type,Point,coordinates,196733.51,439931.8
        x, y = self.coordinates
        return f"type,{self.type},coordinates,{x},{y}"
