install:
	@poetry install

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
