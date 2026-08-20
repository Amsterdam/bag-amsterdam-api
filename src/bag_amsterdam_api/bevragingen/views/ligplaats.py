from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseProxyView


class LigplaatsView(BaseProxyView):
    endpoint_url = settings.BAG_LP_URL
    service_log_id = "ligplaatsen"
    query_parameters = dtos.LigplaatsenQP


class LigplaatsDetailView(BaseProxyView):
    endpoint_url = settings.BAG_LP_URL
    service_log_id = "ligplaatsen"
    query_parameters = dtos.LigplaatsenDetailQP


class LigplaatsTimeRegView(BaseProxyView):
    endpoint_url = settings.BAG_LP_URL
    service_log_id = "ligplaatsen"
