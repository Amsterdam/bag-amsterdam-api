from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseProxyView


class PandView(BaseProxyView):
    endpoint_url = settings.BAG_PA_URL
    service_log_id = "panden"
    query_parameters = dtos.PandenQP


class PandDetailView(BaseProxyView):
    endpoint_url = settings.BAG_PA_URL
    service_log_id = "panden"
    query_parameters = dtos.PandenDetailQP


class PandTimeRegView(BaseProxyView):
    endpoint_url = settings.BAG_PA_URL
    service_log_id = "panden"
