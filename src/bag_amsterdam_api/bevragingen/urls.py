from django.urls import path
from django.views.generic import RedirectView

from bag_amsterdam_api.bevragingen import views

address_object_patterns = [
    path(
        "v2/adresseerbareobjecten",
        views.AdresseerbaarObjectView.as_view(),
        name="bag-adresobjecten",
    ),
    path(
        "v2/adresseerbareobjecten/<str:id>",
        views.AdresseerbaarObjectDetailView.as_view(),
        name="bag-adresobjecten-detail",
    ),
    path(
        "v2/adresseerbareobjecten/<str:id>/lvc",
        views.AdresseerbaarObjectLvcView.as_view(),
        name="bag-adresobjecten-lvc",
    ),
]

address_patterns = [
    path("v2/adressen", views.AdresView.as_view(), name="bag-adressen"),
    path(
        "v2/adressen/<str:id>",
        views.AdresDetailView.as_view(),
        name="bag-adressen-detail",
    ),
    path(
        "v2/adressenuitgebreid",
        views.AdresUitgebreidView.as_view(),
        name="bag-adresuitgebreid",
    ),
    path(
        "v2/adressenuitgebreid/<str:id>",
        views.AdresUitgebreidDetailView.as_view(),
        name="bag-adressenuitgebreid-detail",
    ),
]

bronhouders_patterns = [
    path("v2/bronhouders", views.BronhouderView.as_view(), name="bag-bronhouders"),
    path(
        "v2/bronhouders/<str:id>",
        views.BronhouderDetailView.as_view(),
        name="bag-bronhouders-detail",
    ),
    path(
        "v2/bronhouders/<str:id>/<str:version>/<str:timestamp>",
        views.BronhouderTimeRegistrationView.as_view(),
        name="bag-bronhouders-tsr",
    ),
]

ligplaatsen_patterns = [
    path("v2/ligplaatsen", views.LigplaatsView.as_view(), name="bag-ligplaatsen"),
    path(
        "v2/ligplaatsen/<str:id>",
        views.LigplaatsDetailView.as_view(),
        name="bag-ligplaatsen-detail",
    ),
    path(
        "v2/ligplaatsen/<str:id>/lvc",
        views.LigplaatsLvcView.as_view(),
        name="bag-ligplaatsen-lvc",
    ),
    path(
        "v2/ligplaatsen/<str:id>/<str:version>/<str:timestamp>",
        views.LigplaatsTimeRegistrationView.as_view(),
        name="bag-ligplaatsen-tsr",
    ),
]

nummeraanduiding_patterns = [
    path(
        "v2/nummeraanduidingen",
        views.NummeraanduidingView.as_view(),
        name="bag-nummeraanduidingen",
    ),
    path(
        "v2/nummeraanduidingen/<str:id>",
        views.NummeraanduidingDetailView.as_view(),
        name="bag-nummeraanduidingen-detail",
    ),
    path(
        "v2/nummeraanduidingen/<str:id>/lvc",
        views.NummeraanduidingLvcView.as_view(),
        name="bag-nummeraanduidingen-lvc",
    ),
    path(
        "v2/nummeraanduidingen/<str:id>/<str:version>/<str:timestamp>",
        views.NummeraanduidingTimeRegistrationView.as_view(),
        name="bag-nummeraanduidingen-tsr",
    ),
]

openbareruimten_patterns = [
    path(
        "v2/openbareruimten",
        views.OpenbareRuimteView.as_view(),
        name="bag-openbareruimten",
    ),
    path(
        "v2/openbareruimten/<str:id>",
        views.OpenbareRuimteDetailView.as_view(),
        name="bag-openbareruimten-detail",
    ),
    path(
        "v2/openbareruimten/<str:id>/lvc",
        views.OpenbareRuimteLvcView.as_view(),
        name="bag-openbareruimten-lvc",
    ),
    path(
        "v2/openbareruimten/<str:id>/<str:version>/<str:timestamp>",
        views.OpenbareRuimteTimeRegistrationView.as_view(),
        name="bag-openbareruimten-tsr",
    ),
]

panden_patterns = [
    path("v2/panden", views.PandView.as_view(), name="bag-panden"),
    path("v2/panden/<str:id>", views.PandDetailView.as_view(), name="bag-panden-detail"),
    path("v2/panden/<str:id>/lvc", views.PandLvcView.as_view(), name="bag-panden-lvc"),
    path(
        "v2/panden/<str:id>/<str:version>/<str:timestamp>",
        views.PandTimeRegistrationView.as_view(),
        name="bag-panden-tsr",
    ),
]

standplaatsen_patterns = [
    path(
        "v2/standplaatsen",
        views.StandplaatsView.as_view(),
        name="bag-standplaatsen",
    ),
    path(
        "v2/standplaatsen/<str:id>",
        views.StandplaatsDetailView.as_view(),
        name="bag-standplaatsen-detail",
    ),
    path(
        "v2/standplaatsen/<str:id>/lvc",
        views.StandplaatsLvcView.as_view(),
        name="bag-standplaatsen-lvc",
    ),
    path(
        "v2/standplaatsen/<str:id>/<str:version>/<str:timestamp>",
        views.StandplaatsTimeRegistrationView.as_view(),
        name="bag-standplaatsen-tsr",
    ),
]

verblijfsobject_patterns = [
    path(
        "v2/verblijfsobjecten",
        views.VerblijfsobjectView.as_view(),
        name="bag-verblijfsobjecten",
    ),
    path(
        "v2/verblijfsobjecten/<str:id>",
        views.VerblijfsobjectDetailView.as_view(),
        name="bag-verblijfsobjecten-detail",
    ),
    path(
        "v2/verblijfsobjecten/<str:id>/lvc",
        views.VerblijfsobjectLvcView.as_view(),
        name="bag-verblijfsobjecten-lvc",
    ),
    path(
        "v2/verblijfsobjecten/<str:id>/<str:version>/<str:timestamp>",
        views.VerblijfsobjectTimeRegistrationView.as_view(),
        name="bag-verblijfsobjecten-tsr",
    ),
]

woonplaats_patterns = [
    path("v2/woonplaatsen", views.WoonplaatsView.as_view(), name="bag-woonplaatsen"),
    path(
        "v2/woonplaatsen/<str:id>",
        views.WoonplaatsDetailView.as_view(),
        name="bag-woonplaatsen-detail",
    ),
    path(
        "v2/woonplaatsen/<str:id>/lvc",
        views.WoonplaatsLvcView.as_view(),
        name="bag-woonplaatsen-lvc",
    ),
    path(
        "v2/woonplaatsen/<str:id>/<str:version>/<str:timestamp>",
        views.WoonplaatsTimeRegistrationView.as_view(),
        name="bag-woonplaatsen-tsr",
    ),
]

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="bag-index")),
    path("v2", views.IndexView.as_view(), name="bag-index"),
    path("v2/info", views.InfoView.as_view(), name="bag-info"),
    *address_object_patterns,
    *address_patterns,
    *bronhouders_patterns,
    *ligplaatsen_patterns,
    *nummeraanduiding_patterns,
    *openbareruimten_patterns,
    *panden_patterns,
    *standplaatsen_patterns,
    *verblijfsobject_patterns,
    *woonplaats_patterns,
]

health_urls = [
    # Healthcheck
    path("adressen", views.AdresHealthView.as_view(), name="bag-adressen-health"),
]
