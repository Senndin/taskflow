"""
Local development settings.
Uses SQLite by default (easy start), DEBUG=True.
"""

import dj_database_url
from decouple import config

from .base import *  # noqa: F401, F403

DEBUG = True

# In development any host is fine
ALLOWED_HOSTS = ["*"]

# ---------------------------------------------------------------------------
# DATABASE — SQLite for local development (no Docker required)
# Switch to PostgreSQL by setting DATABASE_URL in .env
# ---------------------------------------------------------------------------
_db_url = config("DATABASE_URL", default=f"sqlite:///{ BASE_DIR / 'db.sqlite3' }")  # noqa: F405
DATABASES = {"default": dj_database_url.parse(_db_url, conn_max_age=600)}

# ---------------------------------------------------------------------------
# django-debug-toolbar — N+1 query inspection
# ---------------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE  # noqa: F405
INTERNAL_IPS = ["127.0.0.1"]

# ---------------------------------------------------------------------------
# Email — print to console in dev
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
