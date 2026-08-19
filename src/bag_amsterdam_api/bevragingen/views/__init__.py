"""Access to all BAG views"""

# Split in a package for easier maintenance
from .adres import (
    AdresDetailView,
    AdresHealthView,
    AdresUitgebreidDetailView,
    AdresUitgebreidView,
    AdresView,
)
from .adresobjecten import (
    AdresseerbaarObjectDetailView,
    AdresseerbaarObjectView,
)
from .bronhouder import BronhouderDetailView, BronhouderView
from .index import IndexView
from .info import InfoView
from .ligplaats import LigplaatsDetailView, LigplaatsView
from .nummeraanduiding import (
    NummeraanduidingDetailView,
    NummeraanduidingView,
)
from .openbareruimte import (
    OpenbareRuimteDetailView,
    OpenbareRuimteView,
)
from .pand import PandDetailView, PandView
from .standplaats import (
    StandplaatsDetailView,
    StandplaatsView,
)
from .verblijfsobject import (
    VerblijfsobjectDetailView,
    VerblijfsobjectView,
)
from .woonplaats import WoonplaatsDetailView, WoonplaatsView

__all__ = (
    "IndexView",
    "InfoView",
    "AdresseerbaarObjectView",
    "AdresseerbaarObjectDetailView",
    "AdresHealthView",
    "AdresView",
    "AdresDetailView",
    "AdresUitgebreidView",
    "AdresUitgebreidDetailView",
    "VerblijfsobjectView",
    "VerblijfsobjectDetailView",
    "StandplaatsView",
    "StandplaatsDetailView",
    "OpenbareRuimteView",
    "OpenbareRuimteDetailView",
    "PandView",
    "PandDetailView",
    "NummeraanduidingView",
    "NummeraanduidingDetailView",
    "LigplaatsView",
    "LigplaatsDetailView",
    "WoonplaatsView",
    "WoonplaatsDetailView",
    "BronhouderView",
    "BronhouderDetailView",
)
