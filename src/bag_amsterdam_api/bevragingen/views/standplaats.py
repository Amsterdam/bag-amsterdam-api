from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseProxyView


class StandplaatsView(BaseProxyView):
    endpoint_url = settings.BAG_SP_URL
    service_log_id = "standplaatsen"
    filter_dto = dtos.StandplaatsenFilter


class StandplaatsDetailView(BaseProxyView):
    endpoint_url = settings.BAG_SP_URL
    service_log_id = "standplaatsen"
    filter_dto = dtos.StandplaatsenDetailFilter


class StandplaatsTimeRegView(BaseProxyView):
    endpoint_url = settings.BAG_SP_URL
    service_log_id = "standplaatsen"
