VIRTUAL_ENV_DIR=venv

test:
	python3 setup.py test

coverage:
	test ! -d $(VIRTUAL_ENV_DIR) && python3 -m venv $(VIRTUAL_ENV_DIR) || true
	$(VIRTUAL_ENV_DIR)/bin/pip install -r requirements-dev.txt
	$(VIRTUAL_ENV_DIR)/bin/coverage run django-filtered-articles/tests/runtests.py
	$(VIRTUAL_ENV_DIR)/bin/coverage html --omit="venv/*"

upgrade-local:
	python3 -m pip install --user --upgrade setuptools wheel twine

.PHONY: build
build:
	python3 setup.py sdist bdist_wheel

upload: build
	python3 -m twine upload --repository testpypi dist/*
