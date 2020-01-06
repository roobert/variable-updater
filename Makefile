APP=variable_updater
VERSION := $(shell python -c 'import toml; print(toml.load("pyproject.toml")["tool"]["poetry"]["version"])')

install:
	@poetry install

docker:
	docker build . --tag ${APP}

clean:
	@rm -vrf ${APP}.egg-info venv

dev-run:
	@poetry run ${APP}

venv:
	@virtualenv venv
	@echo "# run:"
	@echo "source venv/bin/activate"

version-bump-patch:
	@poetry version patch
	@dephell deps convert
	$(shell echo "__version__ = \"${VERSION}\"" > ${APP}/version.py)

version-bump-minor:
	@poetry version minor
	@dephell deps convert
	$(shell echo "__version__ = \"${VERSION}\"" > ${APP}/version.py)

version-bump-major:
	@poetry version major
	@dephell deps convert
	$(shell echo "__version__ = \"${VERSION}\"" > ${APP}/version.py)

setup-convert:
	@dephell deps convert

version:
	$(shell echo "__version__ = \"${VERSION}\"" > ${APP}/version.py)

publish: setup-convert version-update
	@poetry build
	@poetry publish

