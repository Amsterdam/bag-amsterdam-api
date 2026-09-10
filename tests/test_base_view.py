import pytest
from django.urls import reverse

from .utils import build_jwt_token


class TestBaseProxyView:
    """Prove that the generic view offers the login check logic.
    This is tested through the concrete implementations though.
    """

    # RESPONSE_BEWONINGEN = {
    #     "bewoningen": [
    #         {
    #             "adresseerbaarObjectIdentificatie": "0518010000832200",
    #             "periode": {"datumVan": "2020-09-24", "datumTot": "2020-09-25"},
    #             "bewoners": [{"burgerservicenummer": "999993240"}],
    #             "mogelijkeBewoners": [{"burgerservicenummer": "999993241"}],
    #         },
    #         {
    #             "adresseerbaarObjectIdentificatie": "0518010000832200",
    #             "periode": {"datumVan": "2016-03-02", "datumTot": "2020-09-24"},
    #             "bewoners": [{"burgerservicenummer": "999991371"}],
    #             "mogelijkeBewoners": [],
    #         },
    #     ]
    # }

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
                    "href": "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/v2/panden/0484100000045095"
                }
            ],
            "self": {
                "href": "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/v2/adressen/0484200002040489"
            },
            "woonplaats": {
                "href": "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/v2/woonplaatsen/2852"
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

    @pytest.mark.parametrize(
        "url",
        [
            "/bevragingen/v1/adresseerbareobjecten",
            "/bevragingen/adressen",
            "/bevragingen/v1/adressenuitgebreid",
            "/bevragingen/v1/info",
            "/bevragingen/v1/bronhouders",
            "/bevragingen/v1/ligplaatsen",
            "/bevragingen/v1/nummeraanduidingen",
            "/bevragingen/v1/openbareruimten",
            "/bevragingen/v1/panden",
            "/bevragingen/v1/standplaatsen",
            "/bevragingen/v1/verblijfsobjecten",
            "/bevragingen/v1/woonplaatsen",
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
            ("/bevragingen/v1/adresseerbareobjecten", "Adresseerbaar Object"),
            ("/bevragingen/adressen", "Adres"),
            ("/bevragingen/v1/adressenuitgebreid", "Adres Uitgebreid"),
            ("/bevragingen/v1/info", "Info"),
            ("/bevragingen/v1/bronhouders", "Bronhouder"),
            ("/bevragingen/v1/ligplaatsen", "Ligplaats"),
            ("/bevragingen/v1/nummeraanduidingen", "Nummeraanduiding"),
            ("/bevragingen/v1/openbareruimten", "Openbare Ruimte"),
            ("/bevragingen/v1/panden", "Pand"),
            ("/bevragingen/v1/standplaatsen", "Standplaats"),
            ("/bevragingen/v1/verblijfsobjecten", "Verblijfsobject"),
            ("/bevragingen/v1/woonplaatsen", "Woonplaats"),
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

    @pytest.mark.parametrize("remove_header", ["X-Correlation-ID", "X-User", "X-Task-Description"])
    def test_missing_common_headers(self, api_client, common_headers, remove_header):
        """Prove that not providing the common headers is accurately reported back"""
        url = reverse("bag-adressen")
        token = build_jwt_token(["fp_mdw"])
        headers = {
            "Authorization": f"Bearer {token}",
            **common_headers,
        }
        del headers[remove_header]
        response = api_client.get(
            url,
            headers=headers,
        )
        assert response.status_code == 403
        assert response.json() == {
            "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.3",
            "code": "missingHeaders",
            "title": "You do not have permission to perform this action.",
            "detail": (f"A required header is missing: {remove_header.lower()}"),
            "status": 403,
            "instance": "/bevragingen/adressen",
        }

    def test_invalid_query_parameters(self, api_client, common_headers):
        """Prove that pydantic validation errors for query parameters are handled gracefully"""
        url = reverse("bag-adressen")
        token = build_jwt_token(["fp_mdw"])
        response = api_client.get(
            url,
            {"unknown": "value"},
            headers={
                "Authorization": f"Bearer {token}",
                **common_headers,
            },
        )

        assert response.status_code == 400
        assert response.json() == {
            "detail": [
                {
                    "type": "extra_forbidden",
                    "loc": ["unknown"],
                    "msg": "Extra inputs are not permitted",
                    "input": "value",
                    "url": "https://errors.pydantic.dev/2.13/v/extra_forbidden",
                }
            ]
        }

        response = api_client.get(
            url,
            {"page_size": "not_an_int"},
            headers={
                "Authorization": f"Bearer {token}",
                **common_headers,
            },
        )

        assert response.status_code == 400
        assert response.json() == {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["page_size"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "not_an_int",
                    "url": "https://errors.pydantic.dev/2.13/v/int_parsing",
                }
            ]
        }

    # def test_valid_query_parameters(self, api_client, common_headers):
    #     url = reverse("bag-adresobjecten")
    #     token = build_jwt_token(["fp_mdw"])
    #     response = api_client.get(
    #         url,
    #         {"type": "V"},
    #         headers={
    #             "Authorization": f"Bearer {token}",
    #             **common_headers,
    #         },
    #     )
    #     assert response.status_code == 400

    def test_test_valid_query_params(self, api_client, requests_mock, common_headers):
        requests_mock.get(
            "http://localhost:5010/lv/api/bag/bevragingen/adressen/0484200002040489",
            json=self.RESPONSE_ADRESSEN,
            headers={"content-type": "application/json"},
        )

        url = reverse("bag-adressen")  # bag-adressen-detail geeft noreversematch
        token = build_jwt_token(["fp_mdw"])
        response = api_client.get(
            f"{url}?id=0484200002040489",
            {"expand": "false"},
            headers={
                "Authorization": f"Bearer {token}",
                **common_headers,
            },
        )
        assert response.status_code == 200, response
        assert response.json() == self.RESPONSE_ADRESSEN, response.data
