from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class VerblijfsobjectView(BaseProxyView):
    endpoint_url = settings.BAG_VO_URL
    service_log_id = "verblijfsobjecten"
    query_parameters = qp.VerblijfsobjectenQP


class VerblijfsobjectDetailView(BaseProxyView):
    base_url = settings.BAG_VO_URL
    endpoint_url = "{base_url}/{id}"
    service_log_id = "verblijfsobjecten"
    query_parameters = qp.VerblijfsobjectenDetailQP


class VerblijfsobjectLvcView(BaseProxyView):
    base_url = settings.BAG_VO_URL
    endpoint_url = "{base_url}/{id}/lvc"
    service_log_id = "verblijfsobjecten"
    query_parameters = qp.VerblijfsobjectenLvcQP


class VerblijfsobjectTimeRegistrationView(BaseProxyView):
    base_url = settings.BAG_VO_URL
    endpoint_url = "{base_url}/{id}/{version}/{timestamp}"
    service_log_id = "verblijfsobjecten"
