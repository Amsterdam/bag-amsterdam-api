from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class AdresView(BaseProxyView):
    endpoint_url = settings.BAG_AD_URL
    service_log_id = "adressen"
    query_parameters = qp.AdressenQP


class AdresDetailView(BaseProxyView):
    endpoint_url = f"{settings.BAG_AD_URL}/{{id}}"
    service_log_id = "adressen-detail"
    query_parameters = qp.AdressenDetailQP


class AdresUitgebreidView(BaseProxyView):
    endpoint_url = settings.BAG_AU_URL
    service_log_id = "adressenuitgebreid"
    query_parameters = qp.AdressenUitgebreidQP


class AdresUitgebreidDetailView(BaseProxyView):
    endpoint_url = f"{settings.BAG_AU_URL}/{{id}}"
    service_log_id = "adressenuitgebreid-detail"
    query_parameters = qp.AdressenUitgebreidDetailQP
