import pytest
from django.urls import reverse

from src.bag_amsterdam_api.bevragingen.views.base import BaseProxyView
from src.bag_amsterdam_api.query_parameters import VerblijfsobjectenQP

from .utils import build_jwt_token


class TestBaseProxyView:
    """Prove that the generic view offers the login check logic.
    This is tested through the concrete implementations though.
    """

    RESPONSE_ADRESSEN = {
        "openbareRuimteNaam": "Belgiëlaan",
        "huisnummer": 1,
        "woonplaatsNaam": "Hazerswoude-Dorp",
        "nummeraanduidingIdentificatie": "0484200002040489",
        "openbareRuimteIdentificatie": "1672300000000110",
        "woonplaatsIdentificatie": "2852",
        "_links": {
            "adresseerbaarObject": {
                "href": "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/verblijfsobjecten/0484010002033603"
            },
            "nummeraanduiding": {
                "href": "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/nummeraanduidingen/0484200002040489"
            },
            "openbareRuimte": {
                "href": "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/openbareruimten/1672300000000110"
            },
            "panden": [
                {
                    "href": "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/panden/0484100000045095"
                }
            ],
            "self": {
                "href": "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/adressen/0484200002040489"
            },
            "woonplaats": {
                "href": "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/woonplaatsen/2852"
            },
        },
        "adresregel5": "Belgiëlaan 1 A3",
        "adresregel6": "2391 PH  HAZERSWOUDE-DORP",
        "adresseerbaarObjectIdentificatie": "0484010002033603",
        "huisletter": "A",
        "huisnummertoevoeging": "3",
        "korteNaam": "Belgiëlaan",
        "pandIdentificaties": ["0484100000045095"],
        "postcode": "2391PH",
    }

    RESPONSE_ADRESOBJECT = {
        "type": "Verblijfsobject",
        "identificatie": "0226010000038820",
        "domein": "NL.IMBAG.Verblijfsobject",
        "geometrie": {"punt": {"type": "Point", "coordinates": [196733.427, 439931.991, 0.0]}},
        "gebruiksdoelen": ["overige gebruiksfunctie"],
        "oppervlakte": 205,
        "status": "Verblijfsobject in gebruik",
        "geconstateerd": "N",
        "documentdatum": "2019-11-22",
        "documentnummer": "19SZ2048",
        "voorkomen": {
            "tijdstipRegistratie": "2019-12-06T11:51:31",
            "versie": 1,
            "beginGeldigheid": "2019-11-22",
            "tijdstipRegistratieLV": "2019-12-06T12:00:26.425",
        },
        "maaktDeelUitVan": ["0226100000008856"],
        "heeftAlsHoofdAdres": "0226200000038923",
    }

    RESPONSE_LIGPLAATSEN = {
        "type": "Ligplaats",
        "identificatie": "0797020000056894",
        "domein": "NL.IMBAG.Ligplaats",
        "status": "Plaats aangewezen",
        "geometrie": {"punt": {"type": "Point", "coordinates": [196733.51, 439931.89]}},
        "geconstateerd": "N",
        "documentdatum": "2011-12-30",
        "documentnummer": "AVGEL30122011-07",
        "voorkomen": {
            "tijdstipRegistratie": "2013-03-18T14:26:45",
            "versie": 1,
            "beginGeldigheid": "2011-12-30",
            "tijdstipRegistratieLV": "2013-03-18T14:35:39.303",
        },
        "heeftAlsHoofdAdres": "0797200000825818",
    }

    @pytest.mark.parametrize(
        "url",
        [
            "/individuelebevragingen/v2/adresseerbareobjecten",
            "/individuelebevragingen/v2/adressen",
            "/individuelebevragingen/v2/adressenuitgebreid",
            "/individuelebevragingen/v2/bronhouders",
            "/individuelebevragingen/v2/ligplaatsen",
            "/individuelebevragingen/v2/nummeraanduidingen",
            "/individuelebevragingen/v2/openbareruimten",
            "/individuelebevragingen/v2/panden",
            "/individuelebevragingen/v2/standplaatsen",
            "/individuelebevragingen/v2/verblijfsobjecten",
            "/individuelebevragingen/v2/woonplaatsen",
        ],
    )
    def test_no_login(self, api_client, url):
        """Prove that accessing the view fails without a login token."""
        response = api_client.get(url)
        assert response.status_code == 401
        assert response.data == {
            "type": "https://datatracker.ietf.org/doc/html/rfc7235#section-3.1",
            "code": "notAuthenticated",
            "title": "Authentication credentials were not provided.",
            "detail": "",
            "status": 401,
            "instance": url,
        }

    @pytest.mark.parametrize(
        "url, view_name",
        [
            ("/individuelebevragingen/v2/adresseerbareobjecten", "Adresseerbaar Object"),
            ("/individuelebevragingen/v2/adressen", "Adres"),
            ("/individuelebevragingen/v2/adressenuitgebreid", "Adres Uitgebreid"),
            ("/individuelebevragingen/v2/bronhouders", "Bronhouder"),
            ("/individuelebevragingen/v2/ligplaatsen", "Ligplaats"),
            ("/individuelebevragingen/v2/nummeraanduidingen", "Nummeraanduiding"),
            ("/individuelebevragingen/v2/openbareruimten", "Openbare Ruimte"),
            ("/individuelebevragingen/v2/panden", "Pand"),
            ("/individuelebevragingen/v2/standplaatsen", "Standplaats"),
            ("/individuelebevragingen/v2/verblijfsobjecten", "Verblijfsobject"),
            ("/individuelebevragingen/v2/woonplaatsen", "Woonplaats"),
        ],
    )
    def test_options_call(self, api_client, url, view_name):
        """Prove that an options call doesn't raise any errors."""
        response = api_client.options(url)
        assert response.status_code == 200
        assert response.data == {
            "name": view_name,
            "description": "",
            "renders": ["application/json", "text/html"],
            "parses": [
                "application/json",
            ],
        }

    def test_backend_exception(self, api_client, requests_mock):
        """Prove that downstream connection errors are handled gracefully."""

        requests_mock.get(
            "/api/individuelebevragingen/v2/adressen",
            exc=OSError("Connection refused"),
        )

        url = reverse("bag-adressen")
        token = build_jwt_token(["FP/MDW"])
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        response = api_client.get(url, headers=headers)
        assert response.status_code == 503

    def test_backend_500_exception(self, api_client, requests_mock):
        """Prove that downstream connection errors are handled gracefully."""
        error_html = "<html><body><h1>500 Internal Server Error</h1></body></html>"

        requests_mock.get(
            "/api/individuelebevragingen/v2/adressen",
            text=error_html,
            status_code=500,
            headers={"content-type": "text/html"},
        )

        url = reverse("bag-adressen")
        token = build_jwt_token(["FP/MDW"])
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        response = api_client.get(url, headers=headers)
        assert response.status_code == 502

    def test_index_view(self, api_client):
        """Prove that index view works"""
        url = reverse("bag-index")
        token = build_jwt_token(["FP/MDW"])
        response = api_client.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        assert response.status_code == 200

    def test_invalid_scope(self, api_client):
        """Prove that access is checked"""
        url = reverse("bag-adressen")
        token = build_jwt_token(["some_other_scope"])
        response = api_client.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        assert response.status_code == 403, response.data
        assert response.data["code"] == "permissionDenied"
        assert response.data == {
            "code": "permissionDenied",
            "detail": "Required scopes not given in token.",
            "instance": "/individuelebevragingen/v2/adressen",
            "status": 403,
            "title": "You do not have permission to perform this action.",
            "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.3",
        }

    def test_rewrite_links_rewrites_matching_href(self):
        view = BaseProxyView()

        data = self.RESPONSE_ADRESSEN

        rewrites = [
            (
                "https://api.bag.kadaster.nl/lvbag",
                "http://localhost:8098",
            )
        ]

        view._rewrite_links(data, rewrites)

        assert (
            data["_links"]["panden"][0]["href"]
            == "http://localhost:8098/individuelebevragingen/panden/0484100000045095"
        )

    def test_valid_query_params(self, api_client, requests_mock):
        requests_mock.get(
            "/api/individuelebevragingen/v2/adressen/0484200002040489",
            json=self.RESPONSE_ADRESSEN,
            headers={"content-type": "application/json"},
        )

        url = reverse("bag-adressen-detail", kwargs={"id": "0484200002040489"})
        token = build_jwt_token(["FP/MDW"])
        response = api_client.get(
            url,
            {"expand": "false"},
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )
        assert response.status_code == 200, response
        assert response.json() == self.RESPONSE_ADRESSEN, response.data

    def test_invalid_query_parameter_type(self, api_client, requests_mock):
        """Prove that pydantic validation errors for query parameters are handled gracefully"""
        requests_mock.get(
            "/api/individuelebevragingen/v2/adressen",
            json=self.RESPONSE_ADRESSEN,
            headers={"content-type": "application/json"},
        )

        url = reverse("bag-adressen")
        token = build_jwt_token(["FP/MDW"])

        response = api_client.get(
            url,
            {"page_size": "not_an_int"},
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )

        assert response.status_code == 400
        assert response.json() == {
            "status": 400,
            "type": "https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#/10.4.1 400 Bad "
            "Request",
            "detail": "Input should be a valid integer, unable to parse string as an integer",
            "instance": "http://localhost:5010/api/individuelebevragingen/v2/adressen",
            "code": "paramsValidation",
            "invalid-params": [
                {
                    "type": "https://errors.pydantic.dev/2.13/v/int_parsing",
                    "name": "page_size",
                    "code": "int_parsing",
                    "reason": "Input should be a valid integer, unable to parse string as an "
                    "integer",
                }
            ],
        }

    @pytest.mark.parametrize(
        "query, status, expected",
        [
            (
                {"type": "V"},
                200,
                RESPONSE_ADRESOBJECT,
            ),
            (
                {"type": "A"},
                400,
                {
                    "status": 400,
                    "type": "https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#/10.4.1 400 "
                    "Bad Request",
                    "detail": "Input should be 'V', 'S' or 'L'",
                    "instance": "http://localhost:5010/api/individuelebevragingen/v2/adresseerbareobjecten",
                    "code": "paramsValidation",
                    "invalid-params": [
                        {
                            "type": "https://errors.pydantic.dev/2.13/v/enum",
                            "name": "type",
                            "code": "enum",
                            "reason": "Input should be 'V', 'S' or 'L'",
                        }
                    ],
                },
            ),
        ],
    )
    def test_enum_query_parameter(self, api_client, requests_mock, query, status, expected):
        """Prove that pydantic validation errors for query parameters are handled gracefully"""
        requests_mock.get(
            "/api/individuelebevragingen/v2/adresseerbareobjecten",
            json=self.RESPONSE_ADRESOBJECT,
            headers={"content-type": "application/json"},
        )

        url = reverse("bag-adresobjecten")
        token = build_jwt_token(["FP/MDW"])

        response = api_client.get(
            url,
            query,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )

        assert response.status_code == status, response
        assert response.json() == expected

    @pytest.mark.parametrize(
        "query, status, expected",
        [
            (
                {"oppervlakte[min]": 4000, "oppervlakte[max]": 5000},
                200,
                RESPONSE_ADRESOBJECT,
            ),
            (
                {"oppervlakte[min]": 8000, "oppervlakte[max]": 5000},
                400,
                {
                    "status": 400,
                    "type": "https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#/10.4.1 400 "
                    "Bad Request",
                    "detail": "Value error, Minimum surface (8000) cannot be larger than maximum "
                    "surface (5000)",
                    "instance": "http://localhost:5010/api/individuelebevragingen/v2/adresseerbareobjecten",
                    "code": "paramsValidation",
                    "invalid-params": [
                        {
                            "type": "https://errors.pydantic.dev/2.13/v/value_error",
                            "name": "",
                            "code": "value_error",
                            "reason": "Value error, Minimum surface (8000) cannot be larger than "
                            "maximum surface (5000)",
                        }
                    ],
                },
            ),
        ],
    )
    def test_value_query_parameter(self, api_client, requests_mock, query, status, expected):
        """Prove that pydantic validation errors for query parameters are handled gracefully"""
        requests_mock.get(
            "/api/individuelebevragingen/v2/adresseerbareobjecten",
            json=self.RESPONSE_ADRESOBJECT,
            headers={"content-type": "application/json"},
        )

        url = reverse("bag-adresobjecten")
        token = build_jwt_token(["FP/MDW"])

        response = api_client.get(
            url,
            query,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )

        assert response.status_code == status, response
        assert response.json() == expected

    @pytest.mark.parametrize(
        "query, status, expected",
        [
            (
                {"point": "type,Point,coordinates,196733.51,439931.89"},
                200,
                RESPONSE_LIGPLAATSEN,
            ),
            (
                {"point": "type,Point,coordinates,196733.51,439931.89,196733.51"},
                400,
                {
                    "status": 400,
                    "type": "https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#/10.4.1 400 "
                    "Bad Request",
                    "detail": "Value error, Invalid Point query parameter",
                    "instance": "http://localhost:5010/api/individuelebevragingen/v2/ligplaatsen",
                    "code": "paramsValidation",
                    "invalid-params": [
                        {
                            "type": "https://errors.pydantic.dev/2.13/v/value_error",
                            "name": "point",
                            "code": "value_error",
                            "reason": "Value error, Invalid Point query parameter",
                        }
                    ],
                },
            ),
        ],
    )
    def test_point_query_parameter(self, api_client, requests_mock, query, status, expected):
        """Prove that pydantic validation errors for query parameters are handled gracefully"""
        requests_mock.get(
            "/api/individuelebevragingen/v2/ligplaatsen",
            json=self.RESPONSE_LIGPLAATSEN,
            headers={"content-type": "application/json"},
        )

        url = reverse("bag-ligplaatsen")
        token = build_jwt_token(["FP/MDW"])

        response = api_client.get(
            url,
            query,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )

        assert response.status_code == status, response
        assert response.json() == expected

    @pytest.mark.parametrize(
        "query, status, expected",
        [
            (
                {"bbox": "196733.51,439931.89,196833.51,440031.89"},
                200,
                RESPONSE_ADRESOBJECT,
            ),
            (
                {"bbox": "196733.51,439931.89,196833.51"},
                400,
                {
                    "status": 400,
                    "type": "https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#/10.4.1 400 "
                    "Bad Request",
                    "detail": "List should have at least 4 items after validation, not 3",
                    "instance": "http://localhost:5010/api/individuelebevragingen/v2/adresseerbareobjecten",
                    "code": "paramsValidation",
                    "invalid-params": [
                        {
                            "type": "https://errors.pydantic.dev/2.13/v/too_short",
                            "name": "bbox",
                            "code": "too_short",
                            "reason": "List should have at least 4 items after validation, not 3",
                        }
                    ],
                },
            ),
        ],
    )
    def test_bbox_query_parameter(self, api_client, requests_mock, query, status, expected):
        """Prove that pydantic validation errors for query parameters are handled gracefully"""
        requests_mock.get(
            "/api/individuelebevragingen/v2/adresseerbareobjecten",
            json=self.RESPONSE_ADRESOBJECT,
            headers={"content-type": "application/json"},
        )

        url = reverse("bag-adresobjecten")
        token = build_jwt_token(["FP/MDW"])

        response = api_client.get(
            url,
            query,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )

        assert response.status_code == status, response
        assert response.json() == expected


def test_bbox_returns_unchanged_list():
    bbox = [196733.51, 439931.89, 196833.51, 440031.89]
    model = VerblijfsobjectenQP(bbox=bbox)

    assert model.bbox == bbox
