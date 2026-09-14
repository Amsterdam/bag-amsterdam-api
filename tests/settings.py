import environ

from src.bag_amsterdam_api.settings import *  # noqa: F403
from src.bag_amsterdam_api.settings import LOGGING

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
BAG_AD_URL = env.str("BAG_ADRESSEN_URL", default=f"{BAG_URL}/adressen")
BAG_WP_URL = env.str("BAG_ADRESSEN_URL", default=f"{BAG_URL}/woonplaatsen")
