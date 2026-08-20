from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseProxyView


class AdresseerbaarObjectView(BaseProxyView):
    endpoint_url = settings.BAG_AO_URL
    service_log_id = "adresseerbareobjecten"
    query_parameters = dtos.AdresObjectQP


class AdresseerbaarObjectDetailView(BaseProxyView):
    endpoint_url = settings.BAG_AO_URL
    service_log_id = "adresseerbareobjecten"
    query_parameters = dtos.AdresObjectDetailQP


class AdresseerbaarObjectLvcView(BaseProxyView):
    endpoint_url = settings.BAG_AO_URL
    service_log_id = "adresseerbareobjecten"
