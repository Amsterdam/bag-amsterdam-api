from django.conf import settings

from .base import BaseProxyView


class InfoView(BaseProxyView):
    endpoint_url = settings.BAG_INFO_URL
