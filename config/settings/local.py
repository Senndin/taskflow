"""
Local development settings.
Uses SQLite by default (easy start), DEBUG=True.
"""

from .base import *  # noqa: F401, F403

DEBUG = True

# In development any host is fine
ALLOWED_HOSTS = ["*"]

# ---------------------------------------------------------------------------
# DATABASE — SQLite for local development (no Docker required)
# Switch to PostgreSQL by setting DATABASE_URL in .env
# ---------------------------------------------------------------------------
import dj_database_url
from decouple import config

_db_url = config("DATABASE_URL", default=f"sqlite:///{ BASE_DIR / 'db.sqlite3' }")  # noqa: F405
DATABASES = {"default": dj_database_url.parse(_db_url, conn_max_age=600)}

# ---------------------------------------------------------------------------
# django-debug-toolbar (optional, install separately if needed)
# ---------------------------------------------------------------------------
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
# INTERNAL_IPS = ["127.0.0.1"]

# ---------------------------------------------------------------------------
# Email — print to console in dev
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
