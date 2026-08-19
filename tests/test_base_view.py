import pytest
from django.urls import reverse

from .utils import build_jwt_token


class TestBaseProxyView:
    """Prove that the generic view offers the login check logic.
    This is tested through the concrete implementations though.
    """

    @pytest.mark.parametrize(
        "url",
        [
            "/bevragingen/v1/adresseerbareobjecten",
            "/bevragingen/v1/adressen",
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
        assert response.data["detail"] == "Authentication credentials were not provided."
        assert response.data["detail"].code == "not_authenticated"

    @pytest.mark.parametrize(
        "url, view_name",
        [
            ("/bevragingen/v1/adresseerbareobjecten", "Adresseerbaar Object"),
            ("/bevragingen/v1/adressen", "Adres"),
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

    # def test_invalid_api_key(self, api_client, requests_mock, caplog, common_headers):
    #     """Prove that incorrect API-key settings are handled gracefully."""
    #     requests_mock.post(
    #         "/lap/api/brp/personen",
    #         json={
    #             "type": "https://datatracker.ietf.org/doc/html/rfc7235#section-3.1",
    #             "title": "Niet correct geauthenticeerd.",
    #             "status": 401,
    #             "instance": "/lap/api/brp/personen",
    #             "code": "authentication",
    #         },
    #         status_code=401,
    #         headers={"content-type": "application/json"},
    #     )

    #     url = reverse("bag-adressen")
    #     token = build_jwt_token(["fp_mdw"])
    #     response = api_client.post(
    #         url,
    #         {
    #             "type": "ZoekMetPostcodeEnHuisnummer",
    #             "postcode": "1074VE",
    #             "huisnummer": 1,
    #             "fields": ["naam.aanduidingNaamgebruik"],
    #         },
    #         headers={
    #             "Authorization": f"Bearer {token}",
    #             **common_headers,
    #         },
    #     )

    #     assert response.status_code == 502
    #     assert any(
    #         m.startswith(
    #             "Access granted for 'personen.ZoekMetPostcodeEnHuisnummer' to '"
    #         )
    #         for m in caplog.messages
    #     ), caplog.messages
    #     assert response.json() == {
    #         "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.3",
    #         "title": "Connection failed (bad gateway)",
    #         "status": 502,
    #         "detail": "Backend is improperly configured,
    #         "final endpoint rejected our credentials.",
    #         "code": "backendConfig",
    #         "instance": "/bevragingen/v1/personen",
    #     }

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
        assert response.data["detail"] == f"A required header is missing: {remove_header.lower()}"
        # assert response.json() == {
        #     "code": "missingHeaders",
        #     "detail": (
        #         "The following headers are required:
        #         "X-User, X-Correlation-ID, X-Task-Description."
        #     ),
        #     "instance": "/bevragingen/v1/personen",
        #     "status": 403,
        #     "title": "You do not have permission to perform this action.",
        #     "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.3",
        # }

    # @pytest.mark.parametrize(
    #     "content_type",
    #     [
    #         "application/json",
    #         "application/problem+json",
    #         "application/json;charset=utf-8",
    #     ],
    # )
    # def test_error_response(
    #     self, api_client, requests_mock, caplog, common_headers, content_type
    # ):
    #     """Prove that RvIG BRP API errors are handled gracefully for all known content-types"""
    #     requests_mock.post(
    #         "/lap/api/brp/personen",
    #         json={
    #             "invalidParams": [
    #                 {
    #                     "name": "burgerservicenummer",
    #                     "code": "array",
    #                     "reason": "Parameter is geen array.",
    #                 }
    #             ],
    #             "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.1",
    #             "title": "Een of meerdere parameters zijn niet correct.",
    #             "status": 400,
    #             "detail": "De foutieve parameter(s) zijn: burgerservicenummer.",
    #             "instance": "/lap/api/brp/personen",
    #             "code": "paramsValidation",
    #         },
    #         status_code=400,
    #         headers={"content-type": content_type},
    #     )

    #     url = reverse("bag-adressen")
    #     token = build_jwt_token(["fp_mdw"])
    #     response = api_client.post(
    #         url,
    #         {
    #             "type": "RaadpleegMetBurgerservicenummer",
    #             "burgerservicenummer": "000009830",
    #         },
    #         headers={
    #             "Authorization": f"Bearer {token}",
    #             **common_headers,
    #         },
    #     )
    #     assert response.status_code == 400
    #     assert any(
    #         m.startswith(
    #             "Access granted for 'personen.RaadpleegMetBurgerservicenummer' to '"
    #         )
    #         for m in caplog.messages
    #     ), caplog.messages
    #     assert response.json() == {
    #         "code": "paramsValidation",
    #         "detail": "De foutieve parameter(s) zijn: burgerservicenummer.",
    #         "instance": "/bevragingen/v1/personen",
    #         "invalidParams": [
    #             {
    #                 "code": "array",
    #                 "name": "burgerservicenummer",
    #                 "reason": "Parameter is geen array.",
    #             }
    #         ],
    #         "status": 400,
    #         "title": "Een of meerdere parameters zijn niet correct.",
    #         "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.1",
    #     }
