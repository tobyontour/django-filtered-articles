

DEBUG=True
USE_TZ=True
DATABASES={
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}
ROOT_URLCONF="tests.urls"
INSTALLED_APPS=[
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django-filtered-articles",
]
SITE_ID=1
NOSE_ARGS=['-s']
FIXTURE_DIRS=['tests/fixtures']
SECRET_KEY='This is not a secret'