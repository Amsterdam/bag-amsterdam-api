"""Access to all BAG views"""

# viewsets gebruiken ipv views?
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
    AdresseerbaarObjectLvcView,
    AdresseerbaarObjectView,
)
from .bronhouder import (
    BronhouderDetailView,
    BronhouderTimeRegistrationView,
    BronhouderView,
)
from .index import IndexView
from .info import InfoView
from .ligplaats import (
    LigplaatsDetailView,
    LigplaatsLvcView,
    LigplaatsTimeRegistrationView,
    LigplaatsView,
)
from .nummeraanduiding import (
    NummeraanduidingDetailView,
    NummeraanduidingLvcView,
    NummeraanduidingTimeRegistrationView,
    NummeraanduidingView,
)
from .openbareruimte import (
    OpenbareRuimteDetailView,
    OpenbareRuimteLvcView,
    OpenbareRuimteTimeRegistrationView,
    OpenbareRuimteView,
)
from .pand import PandDetailView, PandLvcView, PandTimeRegistrationView, PandView
from .standplaats import (
    StandplaatsDetailView,
    StandplaatsLvcView,
    StandplaatsTimeRegistrationView,
    StandplaatsView,
)
from .verblijfsobject import (
    VerblijfsobjectDetailView,
    VerblijfsobjectLvcView,
    VerblijfsobjectTimeRegistrationView,
    VerblijfsobjectView,
)
from .woonplaats import (
    WoonplaatsDetailView,
    WoonplaatsLvcView,
    WoonplaatsTimeRegistrationView,
    WoonplaatsView,
)

__all__ = (
    "IndexView",
    "InfoView",
    "AdresseerbaarObjectView",
    "AdresseerbaarObjectDetailView",
    "AdresseerbaarObjectLvcView",
    "AdresHealthView",
    "AdresView",
    "AdresDetailView",
    "AdresUitgebreidView",
    "AdresUitgebreidDetailView",
    "VerblijfsobjectView",
    "VerblijfsobjectDetailView",
    "VerblijfsobjectLvcView",
    "VerblijfsobjectTimeRegistrationView",
    "StandplaatsView",
    "StandplaatsDetailView",
    "StandplaatsLvcView",
    "StandplaatsTimeRegistrationView",
    "OpenbareRuimteView",
    "OpenbareRuimteDetailView",
    "OpenbareRuimteLvcView",
    "OpenbareRuimteTimeRegistrationView",
    "PandView",
    "PandDetailView",
    "PandLvcView",
    "PandTimeRegistrationView",
    "NummeraanduidingView",
    "NummeraanduidingDetailView",
    "NummeraanduidingLvcView",
    "NummeraanduidingTimeRegistrationView",
    "LigplaatsView",
    "LigplaatsDetailView",
    "LigplaatsLvcView",
    "LigplaatsTimeRegistrationView",
    "WoonplaatsView",
    "WoonplaatsDetailView",
    "WoonplaatsLvcView",
    "WoonplaatsTimeRegistrationView",
    "BronhouderView",
    "BronhouderDetailView",
    "BronhouderLvcView",
    "BronhouderTimeRegistrationView",
)
