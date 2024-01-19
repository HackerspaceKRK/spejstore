import os


def env(name, default=None):
    return os.getenv("SPEJSTORE_" + name, default)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, "build_static")
PROD = os.getenv("SPEJSTORE_ENV") == "prod"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", "#hjthi7_udsyt*9eeyb&nwgw5x=%pk_lnz3+u2tg9@=w3p1m*k")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not PROD

ALLOWED_HOSTS = env(
    "ALLOWED_HOSTS",
    "devinventory,inventory.waw.hackerspace.pl,inventory.hackerspace.pl,i,inventory"
    + (",127.0.0.1,locahost,*" if not PROD else ""),
).split(",")
LOGIN_REDIRECT_URL = "/admin/"

CSRF_TRUSTED_ORIGINS = env("HOST", "https://inventory.hackerspace.pl").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "storages",  # django-storages s3boto support
    "social_django",
    "tree",
    "django_select2",
    "rest_framework",
    "rest_framework.authtoken",
    "django_markdown2",
    "storage",
    "django_admin_hstore_widget",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "storage.middleware.is_authorized_or_in_lan_middleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "spejstore.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates/"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "spejstore.wsgi.application"

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "NAME": env("DB_NAME", "postgres"),
        "USER": env("DB_USER", "postgres"),
        "PASSWORD": env("DB_PASSWORD", None),
        "HOST": env("DB_HOST", "127.0.0.1"),
        "PORT": env("DB_PORT", 5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


AUTHENTICATION_BACKENDS = (
    "auth.backend.HSWawOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "auth.pipeline.associate_by_personal_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "auth.pipeline.staff_me_up",
)

# Determines the storage type for Django static files and media.
FILE_STORAGE_TYPE = env("FILE_STORAGE_TYPE", "filesystem")

# Make sure we check for correct file storage type
if not (FILE_STORAGE_TYPE == "filesystem" or FILE_STORAGE_TYPE == "s3"):
    raise Exception("SPEJSTORE_FILE_STORAGE_TYPE must be 'filesystem' or 's3' ")

if FILE_STORAGE_TYPE == "filesystem":
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.10/howto/static-files/

    STATIC_URL = "/static/"
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

    MEDIA_URL = "/media/"
    MEDIA_ROOT = env("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))

elif FILE_STORAGE_TYPE == "s3":
    S3_BUCKET_NAME = env("S3_BUCKET_NAME", "inventory")
    S3_ENDPOINT_URL = env("S3_ENDPOINT_URL", "https://object.ceph-eu.hswaw.net")
    S3_DOMAIN_NAME = env("S3_DOMAIN_NAME", "object.ceph-eu.hswaw.net")
    S3_ACCESS_KEY = env("S3_ACCESS_KEY", "")
    S3_SECRET_KEY = env("S3_SECRET_KEY", "=")

    S3_STATIC_LOCATION = "static"
    S3_MEDIA_LOCATION = "media"

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "access_key": S3_ACCESS_KEY,
                "secret_key": S3_SECRET_KEY,
                "endpoint_url": S3_ENDPOINT_URL,
                "bucket_name": S3_BUCKET_NAME,
                "default_acl": "public-read",
                "location": S3_MEDIA_LOCATION,
                "custom_domain": f"{S3_DOMAIN_NAME}/{S3_BUCKET_NAME}",
                "file_overwrite": False,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "access_key": S3_ACCESS_KEY,
                "secret_key": S3_SECRET_KEY,
                "endpoint_url": S3_ENDPOINT_URL,
                "bucket_name": S3_BUCKET_NAME,
                "default_acl": "public-read",
                "location": S3_STATIC_LOCATION,
                "custom_domain": f"{S3_DOMAIN_NAME}/{S3_BUCKET_NAME}",
            },
        },
    }
    bucket_domain_name = f"{S3_ENDPOINT_URL}/{S3_BUCKET_NAME}"
    STATIC_URL = f"{bucket_domain_name}/{S3_STATIC_LOCATION}/"
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

    MEDIA_URL = "/media/"
    STATIC_URL = f"{bucket_domain_name}/{S3_MEDIA_LOCATION}/"
    MEDIA_ROOT = env("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


REQUIRE_AUTH = env("REQUIRE_AUTH", "true")
if REQUIRE_AUTH == "true":
    REQUIRE_AUTH = True
elif REQUIRE_AUTH == "false":
    REQUIRE_AUTH = False

# REST Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
        if REQUIRE_AUTH
        else "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "storage.authentication.LanAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}

SOCIAL_AUTH_HSWAW_KEY = env("CLIENT_ID")
SOCIAL_AUTH_HSWAW_SECRET = env("SECRET")
SOCIAL_AUTH_REDIRECT_IS_HTTPS = env("OAUTH_REDIRECT_IS_HTTPS", "true") == "true"

SOCIAL_AUTH_JSONFIELD_ENABLED = True

LABEL_API = env("LABEL_API", "http://label.waw.hackerspace.pl:4567")
LOGIN_URL = "/admin/login/"
# Local LAN address space
LAN_ALLOWED_ADDRESS_SPACE = env("LAN_ALLOWED_ADDRESS_SPACE", "")
