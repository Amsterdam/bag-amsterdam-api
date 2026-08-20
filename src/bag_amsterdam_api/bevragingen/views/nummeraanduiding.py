from django.conf import settings

from bag_amsterdam_api import datatransferobjects as dtos

from .base import BaseProxyView


class NummeraanduidingView(BaseProxyView):
    endpoint_url = settings.BAG_NA_URL
    service_log_id = "nummeraanduidingen"
    query_parameters = dtos.NummeraanduidingQP


class NummeraanduidingDetailView(BaseProxyView):
    endpoint_url = settings.BAG_NA_URL
    service_log_id = "nummeraanduidingen"
    query_parameters = dtos.NummeraanduidingDetailQP


class NummeraanduidingTimeRegView(BaseProxyView):
    endpoint_url = settings.BAG_NA_URL
    service_log_id = "nummeraanduidingen"
