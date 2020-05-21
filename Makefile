test:
	python3 setup.py test

upgrade-local:
	python3 -m pip install --user --upgrade setuptools wheel twine

build:
	python3 setup.py sdist bdist_wheel

upload: build
	python3 -m twine upload --repository testpypi dist/*
