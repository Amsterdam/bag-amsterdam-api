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
    filter_dto = dtos.AdressenFilter


class AdresDetailView(BaseProxyView):
    endpoint_url = settings.BAG_AD_URL
    service_log_id = "adressen"
    filter_dto = dtos.AdressenDetailFilter


class AdresUitgebreidView(BaseProxyView):
    endpoint_url = settings.BAG_AU_URL
    service_log_id = "adressenuitgebreid"
    filter_dto = dtos.AdressenUitgebreidFilter


class AdresUitgebreidDetailView(BaseProxyView):
    endpoint_url = settings.BAG_AU_URL
    service_log_id = "adressenuitgebreid"
    filter_dto = dtos.AdressenUitgebreidDetailFilter
