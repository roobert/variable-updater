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

setup:
	@dephell deps convert

version: setup
	$(shell echo "__version__ = \"${VERSION}\"" > ${APP}/version.py)

version-patch:
	@poetry version patch
	@(make version)

version-minor:
	@poetry version minor
	@(make version)

version-major:
	@poetry version major
	@(make version)

publish:
	@poetry build
	@poetry publish
