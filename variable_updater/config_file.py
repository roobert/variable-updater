#!/usr/bin/env python

import yaml


class ConfigFileOpenError(Exception):
    pass


def variables(config):
    try:
        with open(config, "r") as data:
            return yaml.safe_load(data)["variables"]
    except Exception as error:
        raise ConfigFileOpenError(f"failed to load config file: {error}")
