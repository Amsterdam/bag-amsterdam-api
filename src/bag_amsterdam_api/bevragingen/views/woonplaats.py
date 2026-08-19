from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseProxyView


class WoonplaatsView(BaseProxyView):
    endpoint_url = settings.BAG_WP_URL
    service_log_id = "woonplaatsen"
    filter_dto = dtos.WoonplaatsenFilter


class WoonplaatsDetailView(BaseProxyView):
    endpoint_url = f"settings.BAG_WP_URL/{id}"
    service_log_id = "woonplaatsen"
    filter_dto = dtos.WoonplaatsenDetailFilter


class WoonplaatsTimeRegView(BaseProxyView):
    endpoint_url = settings.BAG_WP_URL
    service_log_id = "woonplaatsen"
