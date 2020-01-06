install:
	@poetry install

docker:
	docker build . --tag variable-updater

clean:
	@rm -vrf variable_updater.egg-info venv

dev-run:
	@poetry run variable-updater --config config.example.yml

setup-convert:
	@dephell deps convert

venv:
	@virtualenv venv
	@echo "# run:"
	@echo "source venv/bin/activate"
