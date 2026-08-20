from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseProxyView


class BronhouderView(BaseProxyView):
    endpoint_url = settings.BAG_BR_URL
    service_log_id = "bronhouders"
    query_parameters = dtos.BronhoudersQP


class BronhouderDetailView(BaseProxyView):
    endpoint_url = settings.BAG_BR_URL
    service_log_id = "bronhouders"
    query_parameters = dtos.BronhoudersDetailQP


class BronhouderTimeRegView(BaseProxyView):
    endpoint_url = settings.BAG_BR_URL
    service_log_id = "bronhouders"
