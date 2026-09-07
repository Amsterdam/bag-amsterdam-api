from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class PandView(BaseProxyView):
    endpoint_url = settings.BAG_PA_URL
    service_log_id = "panden"
    query_parameters = qp.PandenQP


class PandDetailView(BaseProxyView):
    base_url = settings.BAG_PA_URL
    endpoint_url = "{base_url}/{id}"
    service_log_id = "panden"
    query_parameters = qp.PandenDetailQP


class PandLvcView(BaseProxyView):
    base_url = settings.BAG_PA_URL
    endpoint_url = "{base_url}/{id}/lvc"
    service_log_id = "panden"
    query_parameters = qp.PandenLvcQP


class PandTimeRegistrationView(BaseProxyView):
    base_url = settings.BAG_PA_URL
    endpoint_url = "{base_url}/{id}/{version}/{timestamp}"
    service_log_id = "panden"
