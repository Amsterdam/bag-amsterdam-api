from django.urls import path
from django.views.generic import RedirectView

from bag_amsterdam_api.bevragingen import views

# urls in sub urls packen?

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="bag-index")),
    path("v1", views.IndexView.as_view(), name="bag-index"),
    # API's
    path(
        "v1/adresseerbareobjecten",
        views.AdresseerbaarObjectView.as_view(),
        name="bag-adresobjecten",
    ),
    path(
        "v1/adresseerbareobjecten/<str:id>",
        views.AdresseerbaarObjectDetailView.as_view(),
        name="bag-adresobjecten-detail",
    ),
    path(
        "v1/adresseerbareobjecten/<str:id>/lvc",
        views.AdresseerbaarObjectLvcView.as_view(),
        name="bag-adresobjecten-lvc",
    ),
    path("adressen", views.AdresView.as_view(), name="bag-adressen"),
    path(
        "adressen/<str:id>",
        views.AdresDetailView.as_view(),
        name="bag-adressen-detail",
    ),
    path(
        "v1/adressenuitgebreid",
        views.AdresUitgebreidView.as_view(),
        name="bag-adresuitgebreid",
    ),
    path(
        "v1/adressenuitgebreid/<str:id>",
        views.AdresUitgebreidDetailView.as_view(),
        name="bag-adressenuitgebreid-detail",
    ),
    path("v1/info", views.InfoView.as_view(), name="bag-info"),
    path("v1/bronhouders", views.BronhouderView.as_view(), name="bag-bronhouders"),
    path(
        "v1/bronhouders/<str:id>",
        views.BronhouderDetailView.as_view(),
        name="bag-bronhouders-detail",
    ),
    path(
        "v1/bronhouders/<str:id>/<str:version>/<str:timestamp>",
        views.BronhouderTimeRegistrationView.as_view(),
        name="bag-bronhouders-tsr",
    ),
    path("v1/ligplaatsen", views.LigplaatsView.as_view(), name="bag-ligplaatsen"),
    path(
        "v1/ligplaatsen/<str:id>",
        views.LigplaatsDetailView.as_view(),
        name="bag-ligplaatsen-detail",
    ),
    path(
        "v1/ligplaatsen/<str:id>/lvc",
        views.LigplaatsLvcView.as_view(),
        name="bag-ligplaatsen-lvc",
    ),
    path(
        "v1/ligplaatsen/<str:id>/<str:version>/<str:timestamp>",
        views.LigplaatsTimeRegistrationView.as_view(),
        name="bag-ligplaatsen-tsr",
    ),
    path(
        "v1/nummeraanduidingen",
        views.NummeraanduidingView.as_view(),
        name="bag-nummeraanduidingen",
    ),
    path(
        "v1/nummeraanduidingen/<str:id>",
        views.NummeraanduidingDetailView.as_view(),
        name="bag-nummeraanduidingen-detail",
    ),
    path(
        "v1/nummeraanduidingen/<str:id>/lvc",
        views.NummeraanduidingLvcView.as_view(),
        name="bag-nummeraanduidingen-lvc",
    ),
    path(
        "v1/nummeraanduidingen/<str:id>/<str:version>/<str:timestamp>",
        views.NummeraanduidingTimeRegistrationView.as_view(),
        name="bag-nummeraanduidingen-tsr",
    ),
    path(
        "v1/openbareruimten",
        views.OpenbareRuimteView.as_view(),
        name="bag-openbareruimten",
    ),
    path(
        "v1/openbareruimten/<str:id>",
        views.OpenbareRuimteDetailView.as_view(),
        name="bag-openbareruimten-detail",
    ),
    path(
        "v1/openbareruimten/<str:id>/lvc",
        views.OpenbareRuimteLvcView.as_view(),
        name="bag-openbareruimten-lvc",
    ),
    path(
        "v1/openbareruimten/<str:id>/<str:version>/<str:timestamp>",
        views.OpenbareRuimteTimeRegistrationView.as_view(),
        name="bag-openbareruimten-tsr",
    ),
    path("v1/panden", views.PandView.as_view(), name="bag-panden"),
    path("v1/panden/<str:id>", views.PandDetailView.as_view(), name="bag-panden-detail"),
    path("v1/panden/<str:id>/lvc", views.PandLvcView.as_view(), name="bag-panden-lvc"),
    path(
        "v1/panden/<str:id>/<str:version>/<str:timestamp>",
        views.PandTimeRegistrationView.as_view(),
        name="bag-panden-tsr",
    ),
    path(
        "v1/standplaatsen",
        views.StandplaatsView.as_view(),
        name="bag-standplaatsen",
    ),
    path(
        "v1/standplaatsen/<str:id>",
        views.StandplaatsDetailView.as_view(),
        name="bag-standplaatsen-detail",
    ),
    path(
        "v1/standplaatsen/<str:id>/lvc",
        views.StandplaatsLvcView.as_view(),
        name="bag-standplaatsen-lvc",
    ),
    path(
        "v1/standplaatsen/<str:id>/<str:version>/<str:timestamp>",
        views.StandplaatsTimeRegistrationView.as_view(),
        name="bag-standplaatsen-tsr",
    ),
    path(
        "v1/verblijfsobjecten",
        views.VerblijfsobjectView.as_view(),
        name="bag-verblijfsobjecten",
    ),
    path(
        "v1/verblijfsobjecten/<str:id>",
        views.VerblijfsobjectDetailView.as_view(),
        name="bag-verblijfsobjecten-detail",
    ),
    path(
        "v1/verblijfsobjecten/<str:id>/lvc",
        views.VerblijfsobjectLvcView.as_view(),
        name="bag-verblijfsobjecten-lvc",
    ),
    path(
        "v1/verblijfsobjecten/<str:id>/<str:version>/<str:timestamp>",
        views.VerblijfsobjectTimeRegistrationView.as_view(),
        name="bag-verblijfsobjecten-tsr",
    ),
    path("v1/woonplaatsen", views.WoonplaatsView.as_view(), name="bag-woonplaatsen"),
    path(
        "v1/woonplaatsen/<str:id>",
        views.WoonplaatsDetailView.as_view(),
        name="bag-woonplaatsen-detail",
    ),
    path(
        "v1/woonplaatsen/<str:id>/lvc",
        views.WoonplaatsLvcView.as_view(),
        name="bag-woonplaatsen-lvc",
    ),
    path(
        "v1/woonplaatsen/<str:id>/<str:version>/<str:timestamp>",
        views.WoonplaatsTimeRegistrationView.as_view(),
        name="bag-woonplaatsen-tsr",
    ),
]

health_urls = [
    # Healthchecks
    path("adressen", views.AdresHealthView, name="bag-adres-health"),
]
