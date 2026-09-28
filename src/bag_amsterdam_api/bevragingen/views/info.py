from django.conf import settings

from .base import BaseProxyView


class InfoHealthView(BaseProxyView):
    authentication_classes = []
    needed_scopes = set()
    endpoint_url = settings.BAG_INFO_URL
