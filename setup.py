import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-filtered-articles-pkg-tobyontour", # Replace with your own username
    version="0.0.2",
    author="Toby Bettridge",
    author_email="toby.bettridge@stubside.com",
    description="A django article app",
    long_description=long_description,
    long_description_content_type="text/restructured_text",
    url="https://github.com/tobyontour/django-filtered-articles",
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Django>=3.0.0',
        'Markdown>=3.2.0',
        'django-model-utils>=4.0.0',
        'docutils>=0.16'
    ],
    test_suite='filtered_articles.tests.runtests.runtests'
)