from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

import bag_amsterdam_api.bevragingen.urls

from . import views

urlpatterns = [
    path("individuelebevragingen/", include(bag_amsterdam_api.bevragingen.urls)),
    path("health/", include(bag_amsterdam_api.bevragingen.urls.health_urls)),
    path("pulse", views.pulse),
    path("", views.RootView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
