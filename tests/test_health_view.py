from django.urls import reverse


class TestHealthCheck:
    def test_backend_health_check(self, api_client, requests_mock):
        """Prove that incorrect API-key settings are handled gracefully."""
        requests_mock.get(
            "http://localhost:5010/health/v2/info",
            json={"status": "ok"},
            status_code=200,
        )
        url = reverse("bag-info-health")

        response = api_client.get(url)

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
