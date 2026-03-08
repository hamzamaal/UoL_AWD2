"""Django settings for the MindLMS project.

These settings are intended for local development and coursework use.
Production deployments should use environment variables for secrets and
apply stricter security and host configuration.
"""

from pathlib import Path


# Base directory of the project.
BASE_DIR = Path(__file__).resolve().parent.parent


# Security settings for development only.
SECRET_KEY = "bob"
DEBUG = True
ALLOWED_HOSTS = ["*"]


# Installed Django, third-party, and local applications.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "crispy_forms",
    "crispy_bootstrap5",
    "rest_framework",
    "core.apps.CoreConfig",
    "accounts.apps.AccountsConfig",
    "forum.apps.ForumConfig",
    "donate.apps.DonateConfig",
    "courses.apps.CoursesConfig",
    "quiz.apps.QuizConfig",
    "feedback.apps.FeedbackConfig",
    "instructors.apps.InstructorsConfig",
    "quizapi.apps.QuizapiConfig",
]


# Middleware stack for request and response processing.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "MindLMS.urls"


# Template engine settings.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# WSGI and ASGI entry points.
WSGI_APPLICATION = "MindLMS.wsgi.application"
ASGI_APPLICATION = "MindLMS.asgi.application"


# Database configuration.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation rules.
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


# Internationalization and timezone settings.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"

USE_I18N = True
USE_TZ = True


# Static and media file settings.
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Crispy Forms configuration.
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# Authentication redirect settings.
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "login"


# Default model primary key type.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Allow pages to be embedded in frames where required by the application.
X_FRAME_OPTIONS = "ALLOWALL"


# In-memory channel layer is sufficient for development and local testing.
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}