APP=variable_updater
VERSION := $(shell python -c 'import toml; print(toml.load("pyproject.toml")["tool"]["poetry"]["version"])')

install:
	@poetry install

docker:
	docker build . --tag ${APP}

clean:
	@rm -vrf ${APP}.egg-info venv

dev:
	@poetry run ${APP}

venv:
	@virtualenv venv
	@echo "# run:"
	@echo "source venv/bin/activate"

version-patch:
	@poetry version patch
	@dephell deps convert
	$(shell echo "__version__ = \"${VERSION}\"" > ${APP}/version.py)

version-minor:
	@poetry version minor
	@dephell deps convert
	$(shell echo "__version__ = \"${VERSION}\"" > ${APP}/version.py)

version-major:
	@poetry version major
	@dephell deps convert
	$(shell echo "__version__ = \"${VERSION}\"" > ${APP}/version.py)

setup:
	@dephell deps convert

version:
	$(shell echo "__version__ = \"${VERSION}\"" > ${APP}/version.py)

publish: setup version
	@poetry build
	@poetry publish

