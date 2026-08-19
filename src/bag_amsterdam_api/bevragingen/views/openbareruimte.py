from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseProxyView


class OpenbareRuimteView(BaseProxyView):
    endpoint_url = settings.BAG_OR_URL
    service_log_id = "openbareruimten"
    filter_dto = dtos.OpenbareruimtenFilter


class OpenbareRuimteDetailView(BaseProxyView):
    endpoint_url = settings.BAG_OR_URL
    service_log_id = "openbareruimten"
    filter_dto = dtos.OpenbareruimtenDetailFilter


class OpenbareRuimteTimeRegView(BaseProxyView):
    endpoint_url = settings.BAG_OR_URL
    service_log_id = "openbareruimten"
