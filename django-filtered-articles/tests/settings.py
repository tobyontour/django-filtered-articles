import os
import sys

# Make sure the app is (at least temporarily) on the import path.
APP_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, APP_DIR)

BASE_DIR=APP_DIR
INSTALLED_APPS= (
    'django-filtered-articles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)
ROOT_URLCONF= 'django-filtered-articles.tests.urls'
DATABASES= {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(APP_DIR, 'db.sqlite3'),
    },
}
MIDDLEWARE= [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
TEMPLATE_DIRS= (
    os.path.join(APP_DIR, 'articles', 'templates'),
)
TEMPLATES= [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(APP_DIR, 'django-filtered-articles', 'templates'),
            os.path.join(APP_DIR, 'django-filtered-articles', 'tests', 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
SITE_ID=1

DEBUG= False

SECRET_KEY='This is not a secret key!'

if os.environ.get("DEBUG_OVERRIDE", "False") == "True":
    ALLOWED_HOSTS = ['127.0.0.1']

    INTERNAL_IPS = [
        # ...
        '127.0.0.1',
        # ...
    ]
    DEBUG=True
    STATIC_URL = '/static/'