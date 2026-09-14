from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class NummeraanduidingView(BaseProxyView):
    endpoint_url = settings.BAG_NA_URL
    service_log_id = "nummeraanduidingen"
    query_parameters = qp.NummeraanduidingQP


class NummeraanduidingDetailView(BaseProxyView):
    endpoint_url = f"{settings.BAG_NA_URL}/{{id}}"
    service_log_id = "nummeraanduidingen-detail"
    query_parameters = qp.NummeraanduidingDetailQP


class NummeraanduidingLvcView(BaseProxyView):
    endpoint_url = f"{settings.BAG_NA_URL}/{{id}}/lvc"
    service_log_id = "nummeraanduidingen-lvc"
    query_parameters = qp.NummeraanduidingLvcQP


class NummeraanduidingTimeRegistrationView(BaseProxyView):
    endpoint_url = f"{settings.BAG_NA_URL}/{{id}}/{{version}}/{{timestamp}}"
    service_log_id = "nummeraanduidingen-tmr"
