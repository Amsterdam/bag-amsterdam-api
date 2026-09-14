from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class OpenbareRuimteView(BaseProxyView):
    endpoint_url = settings.BAG_OR_URL
    service_log_id = "openbareruimten"
    query_parameters = qp.OpenbareruimtenQP


class OpenbareRuimteDetailView(BaseProxyView):
    endpoint_url = f"{settings.BAG_OR_URL}/{{id}}"
    service_log_id = "openbareruimten-detail"
    query_parameters = qp.OpenbareruimtenDetailQP


class OpenbareRuimteLvcView(BaseProxyView):
    endpoint_url = f"{settings.BAG_OR_URL}/{{id}}/lvc"
    service_log_id = "openbareruimten-lvc"
    query_parameters = qp.OpenbareruimtenLvcQP


class OpenbareRuimteTimeRegistrationView(BaseProxyView):
    endpoint_url = f"{settings.BAG_OR_URL}/{{id}}/{{version}}/{{timestamp}}"
    service_log_id = "openbareruimten-tmr"
