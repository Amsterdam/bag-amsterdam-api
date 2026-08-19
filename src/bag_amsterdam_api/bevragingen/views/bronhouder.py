from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseProxyView


class BronhouderView(BaseProxyView):
    endpoint_url = settings.BAG_BR_URL
    service_log_id = "bronhouders"
    filter_dto = dtos.BronhoudersFilter


class BronhouderDetailView(BaseProxyView):
    endpoint_url = settings.BAG_BR_URL
    service_log_id = "bronhouders"
    filter_dto = dtos.BronhoudersDetailFilter


class BronhouderTimeRegView(BaseProxyView):
    endpoint_url = settings.BAG_BR_URL
    service_log_id = "bronhouders"
