from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class BronhouderView(BaseProxyView):
    endpoint_url = settings.BAG_BR_URL
    service_log_id = "bronhouders"
    query_parameters = qp.BronhoudersQP


class BronhouderDetailView(BaseProxyView):
    endpoint_url = f"{settings.BAG_BR_URL}/{{id}}"
    service_log_id = "bronhouders-detail"
    query_parameters = qp.BronhoudersDetailQP


class BronhouderTimeRegistrationView(BaseProxyView):
    endpoint_url = f"{settings.BAG_BR_URL}/{{id}}/{{version}}/{{timestamp}}"
    service_log_id = "bronhouders-tmr"
