"""
Production settings.
DEBUG=False, whitenoise for static, PostgreSQL via DATABASE_URL.
"""

import dj_database_url
from decouple import Csv, config

from .base import *  # noqa: F401, F403

DEBUG = False

# ---------------------------------------------------------------------------
# HOSTS — set ALLOWED_HOSTS=yourdomain.com in production .env
# ---------------------------------------------------------------------------
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# ---------------------------------------------------------------------------
# DATABASE — PostgreSQL in production
# ---------------------------------------------------------------------------
DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=config("DB_SSL_REQUIRE", default=True, cast=bool),
    )
}

# ---------------------------------------------------------------------------
# STATIC — whitenoise serves compressed files from STATIC_ROOT
# (already configured in base.py via CompressedManifestStaticFilesStorage)
# Run `python manage.py collectstatic --no-input` before starting gunicorn.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# SECURITY
# ---------------------------------------------------------------------------
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# ---------------------------------------------------------------------------
# LOGGING — errors to stderr, picked up by Docker / platform logs
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

# ---------------------------------------------------------------------------
# Email — configure via env in production
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@taskflow.app")
