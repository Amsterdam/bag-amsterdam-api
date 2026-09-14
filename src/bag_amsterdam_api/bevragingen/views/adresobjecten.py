from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class AdresseerbaarObjectView(BaseProxyView):
    endpoint_url = settings.BAG_AO_URL
    service_log_id = "adresseerbareobjecten"
    query_parameters = qp.AdresObjectQP


class AdresseerbaarObjectDetailView(BaseProxyView):
    base_url = settings.BAG_AO_URL
    endpoint_url = f"{settings.BAG_AO_URL}/{{id}}"
    service_log_id = "adresseerbareobjecten-detail"
    query_parameters = qp.AdresObjectDetailQP


class AdresseerbaarObjectLvcView(BaseProxyView):
    base_url = settings.BAG_AO_URL
    endpoint_url = f"{settings.BAG_AO_URL}/{{id}}/lvc"
    service_log_id = "adresseerbareobjecten-lvc"
    query_parameters = qp.AdresObjectLvcQP
