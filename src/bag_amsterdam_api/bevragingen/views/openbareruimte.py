from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class OpenbareRuimteView(BaseProxyView):
    endpoint_url = settings.BAG_OR_URL
    service_log_id = "openbareruimten"
    query_parameters = qp.OpenbareruimtenQP


class OpenbareRuimteDetailView(BaseProxyView):
    base_url = settings.BAG_OR_URL
    endpoint_url = "{base_url}/{id}"
    service_log_id = "openbareruimten"
    query_parameters = qp.OpenbareruimtenDetailQP


class OpenbareRuimteLvcView(BaseProxyView):
    base_url = settings.BAG_OR_URL
    endpoint_url = "{base_url}/{id}/lvc"
    service_log_id = "openbareruimten"
    query_parameters = qp.OpenbareruimtenLvcQP


class OpenbareRuimteTimeRegistrationView(BaseProxyView):
    base_url = settings.BAG_OR_URL
    endpoint_url = "{base_url}/{id}/{version}/{timestamp}"
    service_log_id = "openbareruimten"
