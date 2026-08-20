from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseHealthCheckView, BaseProxyView


class AdresHealthView(BaseHealthCheckView):
    """View to check backend access."""

    permission_classes = []
    endpoint_url = settings.BAG_AD_URL


class AdresView(BaseProxyView):
    endpoint_url = settings.BAG_AD_URL
    service_log_id = "adressen"
    query_parameters = dtos.AdressenQP


class AdresDetailView(BaseProxyView):
    endpoint_url = settings.BAG_AD_URL
    service_log_id = "adressen"
    query_parameters = dtos.AdressenDetailQP


class AdresUitgebreidView(BaseProxyView):
    endpoint_url = settings.BAG_AU_URL
    service_log_id = "adressenuitgebreid"
    query_parameters = dtos.AdressenUitgebreidQP


class AdresUitgebreidDetailView(BaseProxyView):
    endpoint_url = settings.BAG_AU_URL
    service_log_id = "adressenuitgebreid"
    query_parameters = dtos.AdressenUitgebreidDetailQP
