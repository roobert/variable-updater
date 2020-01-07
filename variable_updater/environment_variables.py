#!/usr/bin/env python

import os
from collections import namedtuple


class EnvironmentVariableError(Exception):
    pass


def environment_variables():
    config = namedtuple(
        "Config",
        "server username password bitbucket_key_mount bitbucket_username_key bitbucket_password_key",
    )

    try:
        config.server = os.environ["VAULT_ADDR"]
        config.username = os.environ["VAULT_USERNAME"]
        config.password = os.environ["VAULT_PASSWORD"]
        config.bitbucket_key_mount = os.environ["VAULT_BITBUCKET_KEY_MOUNT"]
        config.bitbucket_username_key = os.environ["VAULT_BITBUCKET_USERNAME_KEY"]
        config.bitbucket_password_key = os.environ["VAULT_BITBUCKET_PASSWORD_KEY"]
        return config
    except KeyError as error:
        raise EnvironmentVariableError(f"failure reading environment variable: {error}")
