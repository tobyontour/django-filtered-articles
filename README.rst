=================
Filtered Articles
=================

Filtered Articles is a Django app to provide articles with slug-based URLs and
plain text, Markdown, and reStructuredText processing.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "django-filtered-articles" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django-filtered-articles',
    ]

2. Include the articles URLconf in your project urls.py like this::

    path('articles/', include('django-filtered-articles.urls')),

3. Run ``python manage.py migrate`` to create the articles models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create an article (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/articles/new to create an article.

Development
-----------

1. Make sure you have python3 installed.
2. Run the tests::

    make test

3. Check your local environment is up to date::

    make upgrade-local

4. Build the package::

    make build

5. Upload it (assumes you have setup the API key)::

    make upload

See `Packaging Projects <https://packaging.python.org/tutorials/packaging-projects/>`_