from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseProxyView


class VerblijfsobjectView(BaseProxyView):
    endpoint_url = settings.BAG_VO_URL
    service_log_id = "verblijfsobjecten"
    query_parameters = dtos.VerblijfsobjectenQP


class VerblijfsobjectDetailView(BaseProxyView):
    endpoint_url = f"settings.BAG_VO_URL/{id}"
    service_log_id = "verblijfsobjecten"
    query_parameters = dtos.VerblijfsobjectenDetailQP


class VerblijfsobjectTimeRegView(BaseProxyView):
    endpoint_url = settings.BAG_VO_URL
    service_log_id = "verblijfsobjecten"
