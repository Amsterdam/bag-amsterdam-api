from django.conf import settings

from bag_amsterdam_api import query_parameters as qp

from .base import BaseProxyView


class VerblijfsobjectView(BaseProxyView):
    endpoint_url = settings.BAG_VO_URL
    service_log_id = "verblijfsobjecten"
    query_parameters = qp.VerblijfsobjectenQP


class VerblijfsobjectDetailView(BaseProxyView):
    endpoint_url = f"{settings.BAG_VO_URL}/{{id}}"
    service_log_id = "verblijfsobjecten-detail"
    query_parameters = qp.VerblijfsobjectenDetailQP


class VerblijfsobjectLvcView(BaseProxyView):
    endpoint_url = f"{settings.BAG_VO_URL}/{{id}}/lvc"
    service_log_id = "verblijfsobjecten-lvc"
    query_parameters = qp.VerblijfsobjectenLvcQP


class VerblijfsobjectTimeRegistrationView(BaseProxyView):
    endpoint_url = f"{settings.BAG_VO_URL}/{{id}}/{{version}}/{{timestamp}}"
    service_log_id = "verblijfsobjecten-tmr"
