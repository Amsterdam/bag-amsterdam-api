from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseProxyView


class AdresseerbaarObjectView(BaseProxyView):
    endpoint_url = settings.BAG_AO_URL
    service_log_id = "adresseerbareobjecten"
    filter_dto = dtos.AdresObjectFilter


class AdresseerbaarObjectDetailView(BaseProxyView):
    endpoint_url = settings.BAG_AO_URL
    service_log_id = "adresseerbareobjecten"
    filter_dto = dtos.AdresObjectDetailFilter


class AdresseerbaarObjectLvcView(BaseProxyView):
    endpoint_url = settings.BAG_AO_URL
    service_log_id = "adresseerbareobjecten"
