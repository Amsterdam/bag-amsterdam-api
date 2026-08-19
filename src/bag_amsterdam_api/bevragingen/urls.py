from django.urls import path
from django.views.generic import RedirectView

from bag_amsterdam_api.bevragingen import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="bag-index")),
    path("v1", views.IndexView.as_view(), name="bag-index"),
    # API's
    path(
        "v1/adresseerbareobjecten",
        views.AdresseerbaarObjectView.as_view(),
        name="bag-adresobjecten",
    ),
    path("v1/adressen", views.AdresView.as_view(), name="bag-adressen"),
    path(
        "v1/adressenuitgebreid",
        views.AdresUitgebreidView.as_view(),
        name="bag-adresuitgebreid",
    ),
    path("v1/info", views.InfoView.as_view(), name="bag-info"),
    path("v1/bronhouders", views.BronhouderView.as_view(), name="bag-bronhouders"),
    path("v1/ligplaatsen", views.LigplaatsView.as_view(), name="bag-ligplaatsen"),
    path(
        "v1/nummeraanduidingen",
        views.NummeraanduidingView.as_view(),
        name="bag-nummeraanduidingen",
    ),
    path(
        "v1/openbareruimten",
        views.OpenbareRuimteView.as_view(),
        name="bag-openbareruimten",
    ),
    path("v1/panden", views.PandView.as_view(), name="bag-panden"),
    path(
        "v1/standplaatsen",
        views.StandplaatsView.as_view(),
        name="bag-standplaatsen",
    ),
    path(
        "v1/verblijfsobjecten",
        views.VerblijfsobjectView.as_view(),
        name="bag-verblijfsobjecten",
    ),
    path("v1/woonplaatsen", views.WoonplaatsView.as_view(), name="bag-woonplaatsen"),
]

health_urls = [
    # Healthchecks
    path("adressen", views.AdresHealthView, name="bag-adres-health"),
]
