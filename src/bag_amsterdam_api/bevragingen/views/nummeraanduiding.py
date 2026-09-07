from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class NummeraanduidingView(BaseProxyView):
    endpoint_url = settings.BAG_NA_URL
    service_log_id = "nummeraanduidingen"
    query_parameters = qp.NummeraanduidingQP


class NummeraanduidingDetailView(BaseProxyView):
    base_url = settings.BAG_NA_URL
    endpoint_url = "{base_url}/{id}"
    service_log_id = "nummeraanduidingen"
    query_parameters = qp.NummeraanduidingDetailQP


class NummeraanduidingLvcView(BaseProxyView):
    base_url = settings.BAG_NA_URL
    endpoint_url = "{base_url}/{id}/lvc"
    service_log_id = "nummeraanduidingen"
    query_parameters = qp.NummeraanduidingLvcQP


class NummeraanduidingTimeRegistrationView(BaseProxyView):
    base_url = settings.BAG_NA_URL
    endpoint_url = "{base_url}/{id}/{version}/{timestamp}"
    service_log_id = "nummeraanduidingen"
