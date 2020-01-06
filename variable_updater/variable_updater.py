#!/usr/bin/env python

from .cli import parse_args, environment_variables
from .config_file import variables
from .vault import Vault
from .bitbucket_requester import BitBucketRequester
from .bitbucket_variable import BitBucketVariable


class ConfigFileVariableError(Exception):
    pass


def bitbucket_username(vault, config):
    return vault.read(
        config.bitbucket_key_mount, config.bitbucket_username_key, "value"
    )


def bitbucket_password(vault, config):
    return vault.read(
        config.bitbucket_key_mount, config.bitbucket_password_key, "value"
    )


def bitbucket_requester(vault, config):
    return BitBucketRequester(
        username=bitbucket_username(vault, config),
        password=bitbucket_password(vault, config),
    )


def vault_client(config):
    return Vault(
        server=config.server, username=config.username, password=config.password
    )


def variable_updater():
    args = parse_args()
    config = environment_variables()
    vault = vault_client(config)

    for variable in variables(args.config):
        value = vault.read(
            variable["vault_mount"], variable["vault_path"], variable["vault_key"]
        )

        try:
            variable = BitBucketVariable(
                requester=bitbucket_requester(vault, config),
                workspace=variable["bitbucket_workspace"],
                repo=variable["bitbucket_repo"],
                key=variable["bitbucket_variable"],
                value=value,
            )
        except AttributeError as error:
            raise ConfigFileVariableError(f"key failure for config file: {error}")

        variable.upsert()
