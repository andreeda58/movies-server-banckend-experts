# settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# --------- elegir archivo .env según DJANGO_ENV ----------
DJANGO_ENV = os.getenv("DJANGO_ENV", "dev").lower()  # dev | prod
env_file = BASE_DIR / (".env.prod" if DJANGO_ENV == "prod" else ".env.dev")
load_dotenv(env_file)
# ---------------------------------------------------------

# --- Security / Debug ---
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure")
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

# --- Apps ---
INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "moviesapi", "accounts",
    "rest_framework", "rest_framework.authtoken",
    "corsheaders",
]

# --- Middleware ---
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise se inserta más abajo si aplica
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- Templates ---
from django.conf import global_settings  # opcional, solo para recordar defaults
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

ROOT_URLCONF = "moviesserver.urls"
WSGI_APPLICATION = "moviesserver.wsgi.application"

# --- Database (toma todo del .env elegido) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "postgres"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "CONN_MAX_AGE": 60,
        # Descomenta si tu RDS exige SSL:
        # "OPTIONS": {"sslmode": "require"},
    }
}

# --- i18n ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static & Media (defaults locales) ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- S3 / Storages (solo en prod con USE_S3_STATIC=1) ---
USE_S3_STATIC = os.getenv("USE_S3_STATIC", "0") == "1"
AWS_STORAGE_BUCKET_NAME = (os.getenv("AWS_STORAGE_BUCKET_NAME", "") or "").strip()
AWS_S3_REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "eu-north-1").strip()
HAS_BUCKET = bool(AWS_STORAGE_BUCKET_NAME)

if USE_S3_STATIC and HAS_BUCKET and not DEBUG:
    INSTALLED_APPS.append("storages")

    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

    STORAGES = {
        "default": {  # MEDIA en S3
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {"location": "media", "file_overwrite": False},
        },
        "staticfiles": {  # STATIC en S3
            "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
            "OPTIONS": {"location": "static"},
        },
    }
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
else:
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
    # Si estás en prod SIN S3, sirve estáticos con WhiteNoise
    if not DEBUG:
        MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
        STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- CORS ---
CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:5173", "http://localhost:5173"]
CORS_ALLOW_CREDENTIALS = True

# --- Security behind ALB/Nginx ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
