import os
from pathlib import Path
from typing import Any

import environ
from pythonjsonlogger import json

env = environ.Env()
_USE_SECRET_STORE = Path("/mnt/secrets-store").exists()

URL = env.str("URL", default="http://localhost:8098/")

# -- Environment

SRC_DIR = Path(__file__).parents[1]

CLOUD_ENV = env.str("CLOUD_ENV", "default").lower()
DEBUG = env.bool("DJANGO_DEBUG", default=(CLOUD_ENV == "default"))
ENVIRONMENT = env.str("ENVIRONMENT", default="dev")

# Whitenoise needs a place to store static files and their gzipped versions.
STATIC_ROOT = env.str("STATIC_ROOT", str(SRC_DIR.parent / "web/static"))
STATIC_URL = env.str("STATIC_URL", "/static/")

# -- Security

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", "insecure")

# -- Application definition

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "bag_amsterdam_api",
]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "authorization_django.authorization_middleware",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
        "django_extensions",
    ]
    MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "bag_amsterdam_api.urls"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(SRC_DIR / "templates")],
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

# -- Services

DATABASES = {}  # "default": env.db_url(default="django.db.backends.sqlite3:///tmp/db.sqlite3")}

# -- Logging


class CustomJsonFormatter(json.JsonFormatter):
    def __init__(self, *args, **kwargs):
        # Make sure some 'extra' fields are not included:
        super().__init__(*args, **kwargs)
        self._skip_fields.update({"request": "request", "taskName": "taskName"})

    def add_fields(self, log_record: dict, record, message_dict: dict):
        # The 'rename_fields' logic fails when fields are missing, this is easier:
        super().add_fields(log_record, record, message_dict)
        # An in-place reordering, sotime/level appear first (easier for docker log scrolling)
        ordered_dict = {
            "time": log_record.pop("asctime", record.asctime),
            "level": log_record.pop("levelname", record.levelname),
            **log_record,
        }
        log_record.clear()
        log_record.update(ordered_dict)


_json_log_formatter = {
    "()": CustomJsonFormatter,
    "format": "%(asctime)s $(levelname)s %(name)s %(message)s",  # parsed as a fields list.
}

DJANGO_LOG_LEVEL = env.str("DJANGO_LOG_LEVEL", "INFO")
LOG_LEVEL = env.str("LOG_LEVEL", "DEBUG" if DEBUG else "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "json": _json_log_formatter,
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "console_print": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "level": DJANGO_LOG_LEVEL,
        "handlers": ["console"],
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": DJANGO_LOG_LEVEL,
            "propagate": False,
        },
        "django.utils.autoreload": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "bag_amsterdam_api": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "apikeyclient": {"handlers": ["console"], "propagate": False},
    },
}

if DEBUG:
    # Print tracebacks without JSON formatting.
    LOGGING["loggers"]["django.request"] = {
        "handlers": ["console_print"],
        "level": "ERROR",
        "propagate": False,
    }

# -- Azure specific settings
if CLOUD_ENV.startswith("azure"):
    from azure.monitor.opentelemetry import configure_azure_monitor
    from opentelemetry.instrumentation.django import DjangoInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.semconv.resource import ResourceAttributes

    # Microsoft recommended abbreviation for Application Insights is `APPI`
    AZURE_APPI_CONNECTION_STRING = env.str("AZURE_APPI_CONNECTION_STRING")

    # Configure OpenTelemetry to use Azure Monitor with the specified connection string
    if AZURE_APPI_CONNECTION_STRING is not None:
        configure_azure_monitor(
            connection_string=AZURE_APPI_CONNECTION_STRING,
            logger_name="root",
            instrumentation_options={
                "azure_sdk": {"enabled": False},
                "django": {"enabled": False},  # Manually done
                "fastapi": {"enabled": False},
                "flask": {"enabled": False},
                "psycopg": {"enabled": False},  # Manually done
                "requests": {"enabled": True},
                "urllib": {"enabled": True},
                "urllib3": {"enabled": True},
            },
            resource=Resource.create({ResourceAttributes.SERVICE_NAME: "bag-amsterdam-api"}),
        )
        print("OpenTelemetry has been enabled")

        def response_hook(span, request, response):
            if (
                span.is_recording()
                and hasattr(request, "get_token_claims")
                and (email := request.get_token_claims.get("email", request.get_token_subject))
            ):
                span.set_attribute("user.AuthenticatedId", email)

        DjangoInstrumentor().instrument(response_hook=response_hook)
        print("Django instrumentor enabled")

        # Psycopg2Instrumentor().instrument(enable_commenter=True, commenter_options={})
        # print("Psycopg instrumentor enabled")

# -- Third party app settings

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)

REST_FRAMEWORK = dict(
    DEFAULT_PARSER_CLASSES=[
        "rest_framework.parsers.JSONParser",
    ],
    DEFAULT_RENDERER_CLASSES=[
        # Removed HTML rendering, Give pure application/problem+json responses instead.
        # The HTML rendering is not needed and conflicts with the exception_handler code.
        "rest_framework.renderers.JSONRenderer",
    ],
    EXCEPTION_HANDLER="bag_amsterdam_api.views.exception_handler",
    UNAUTHENTICATED_USER=None,  # Avoid importing django.contrib.auth.models
    UNAUTHENTICATED_TOKEN=None,
    URL_FORMAT_OVERRIDE="_format",  # use ?_format=.. instead of ?format=..
    DEFAULT_AUTHENTICATION_CLASSES=[],
)

if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(  # ty:ignore[possibly-missing-attribute]
        "rest_framework.renderers.BrowsableAPIRenderer"
    )

DATAPUNT_AUTHZ = {
    # To verify JWT tokens, the PUB_JWKS needs to be set.
    "JWKS": os.getenv("PUB_JWKS"),
    # "ALWAYS_OK": True if DEBUG else False,
    "ALWAYS_OK": False,
    "MIN_INTERVAL_KEYSET_UPDATE": 30 * 60,  # 30 minutes
}

# -- Local app settings

if _USE_SECRET_STORE or CLOUD_ENV.startswith("azure"):
    BAG_API_KEY = Path("/mnt/secrets-store/bag-proxy-key").read_text()
else:
    BAG_API_KEY = env.str("BAG_API_KEY", "")

BAG_URL = env.str(
    "BAG_URL",
    default="",
)
BAG_INFO_URL = env.str(
    "BAG_INFO_URL",
    default=f"{BAG_URL}/info",
)
BAG_AO_URL = env.str("BAG_AO_URL", default=f"{BAG_URL}/adresseerbareobjecten")
BAG_AD_URL = env.str("BAG_AD_URL", default=f"{BAG_URL}/adressen")
BAG_AU_URL = env.str("BAG_AU_URL", default=f"{BAG_URL}/adressenuitgebreid")
BAG_BR_URL = env.str("BAG_BR_URL", default=f"{BAG_URL}/bronhouders")
BAG_LP_URL = env.str("BAG_LP_URL", default=f"{BAG_URL}/ligplaatsen")
BAG_NA_URL = env.str("BAG_NA_URL", default=f"{BAG_URL}/nummeraanduidingen")
BAG_OR_URL = env.str("BAG_OR_URL", default=f"{BAG_URL}/openbareruimten")
BAG_PA_URL = env.str("BAG_PA_URL", default=f"{BAG_URL}/panden")
BAG_SP_URL = env.str("BAG_SP_URL", default=f"{BAG_URL}/standplaatsen")
BAG_VO_URL = env.str("BAG_VO_URL", default=f"{BAG_URL}/verblijfsobjecten")
BAG_WP_URL = env.str("BAG_WP_URL", default=f"{BAG_URL}/woonplaatsen")

# -- Local app settings
BACKEND_API = env.str("BACKEND_API", "mock")
