#This file mainly exists to allow python setup.py test to work.
import os
import sys

# Make sure the app is (at least temporarily) on the import path.
APP_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, APP_DIR)

SETTINGS_DICT = {
    'BASE_DIR': APP_DIR,
    'INSTALLED_APPS': (
        'django-filtered-articles',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
    ),
    'ROOT_URLCONF': 'django-filtered-articles.tests.urls',
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(APP_DIR, 'db.sqlite3'),
        },
    },
    'MIDDLEWARE': [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    'TEMPLATE_DIRS': (
        os.path.join(APP_DIR, 'articles', 'templates'),
    ),
    'TEMPLATES': [
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
    ],
    'SITE_ID': 1,

    'DEBUG': False
}

def runtests():
    from django.conf import settings
    settings.configure(**SETTINGS_DICT)
    # os.environ['DJANGO_SETTINGS_MODULE'] = 'django-filtered-articles.tests.test_settings'
    import django
    if hasattr(django, 'setup'):
        django.setup()

    # Now we instantiate a test runner...
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)

    # And then we run tests and return the results.
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['django-filtered-articles.tests'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()