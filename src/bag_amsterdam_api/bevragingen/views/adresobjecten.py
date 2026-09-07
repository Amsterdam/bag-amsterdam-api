from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class AdresseerbaarObjectView(BaseProxyView):
    endpoint_url = settings.BAG_AO_URL
    service_log_id = "adresseerbareobjecten"
    query_parameters = qp.AdresObjectQP


class AdresseerbaarObjectDetailView(BaseProxyView):
    base_url = settings.BAG_AO_URL
    endpoint_url = "{base_url}/{id}"
    service_log_id = "adresseerbareobjecten"
    query_parameters = qp.AdresObjectDetailQP


# voor nu gekozen voor aparte views in plaats van viewsets, net zoals brp
class AdresseerbaarObjectLvcView(BaseProxyView):
    base_url = settings.BAG_AO_URL
    endpoint_url = "{base_url}/{id}/lvc"
    service_log_id = "adresseerbareobjecten"
    query_parameters = qp.AdresObjectLvcQP
