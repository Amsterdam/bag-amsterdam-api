from json import loads

import environ

from src.bag_amsterdam_api.settings import *  # noqa: F403
from src.bag_amsterdam_api.settings import LOGGING, Path

env = environ.Env()

# The reason the settings are defined here, is to make them independent
# of the regular project sources. Otherwise, the project needs to have
# knowledge of the test framework.

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Load public/private test key pair.
# This was obtained in the authz project with: jwkgen -create -alg ES256
jwks_key = Path(__file__).parent.parent.joinpath("src", "jwks_test.json").read_text()

DATAPUNT_AUTHZ = {
    "TRUSTED_JWKS": [{"jwks": loads(jwks_key), "claims": {"iss": "iss"}}],
    "ALWAYS_OK": False,
    "MIN_INTERVAL_KEYSET_UPDATE": 30 * 60,  # 30 minutes
}

# Remove propagate=False so caplog can read those messages.
LOGGING = {
    **LOGGING,
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
    "loggers": {
        **{
            name: {
                **conf,
                "propagate": True,
            }
            for name, conf in LOGGING["handlers"].items()
        },
        # Set zeep to INFO because it is very verbose in DEBUG mode
        "zeep": {
            "level": "INFO",
        },
    },
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Prevent tests to crash because of missing staticfiles manifests
WHITENOISE_MANIFEST_STRICT = False

# use different defaults.
# By using a portnumber, the BagClient detects that this is a mock API
BAG_URL = env.str("BAG_URL", default="http://localhost:5010/lvbag/api/individuelebevragingen/v2")
BAG_AD_URL = env.str("BAG_AD_URL", default=f"{BAG_URL}/adressen")
BAG_AO_URL = env.str("BAG_AO_URL", default=f"{BAG_URL}/adresseerbareobjecten")
BAG_LP_URL = env.str("BAG_LP_URL", default=f"{BAG_URL}/ligplaatsen")
