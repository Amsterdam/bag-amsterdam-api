from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseHealthCheckView, BaseProxyView


class AdresHealthView(BaseHealthCheckView):
    """View to check backend access."""

    permission_classes = []
    endpoint_url = settings.BAG_AD_URL


class AdresView(BaseProxyView):
    endpoint_url = settings.BAG_AD_URL
    service_log_id = "adressen"
    query_parameters = qp.AdressenQP


class AdresDetailView(BaseProxyView):
    base_url = settings.BAG_AD_URL
    endpoint_url = "{base_url}/{id}"
    service_log_id = "adressen"
    query_parameters = qp.AdressenDetailQP

    # def get(self, request, *args, **kwargs):
    #     id = kwargs["nummeraanduidingIdentificatie"]
    #     endpoint_url = f"{settings.BAG_AD_URL}/{id}"


class AdresUitgebreidView(BaseProxyView):
    endpoint_url = settings.BAG_AU_URL
    service_log_id = "adressenuitgebreid"
    query_parameters = qp.AdressenUitgebreidQP


class AdresUitgebreidDetailView(BaseProxyView):
    base_url = settings.BAG_AU_URL
    endpoint_url = "{base_url}/{id}"
    service_log_id = "adressenuitgebreid"
    query_parameters = qp.AdressenUitgebreidDetailQP
