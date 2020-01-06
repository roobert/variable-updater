#!/usr/bin/env python

from .cli import parse_args, environment_variables
from .config_file import variables, ConfigFileError
from .vault import Vault
from .bitbucket_requester import BitBucketRequester
from .bitbucket_variable import BitBucketVariable


class ConfigFileVariableError(Exception):
    pass


def variable_updater():
    args = parse_args()
    config = environment_variables()

    vault = Vault(
        server=config.server, username=config.username, password=config.password
    )

    bitbucket_username = vault.read(
        config.bitbucket_key_mount, config.bitbucket_username_key
    )
    bitbucket_password = vault.read(
        config.bitbucket_key_mount, config.bitbucket_password_key
    )

    # NOTE: requires a bitbucket "app password" with edit variables permissions
    requester = BitBucketRequester(
        username=bitbucket_username, password=bitbucket_password,
    )

    for variable in variables(args.config):
        value = vault.read(variable["vault_mount"], variable["value"])

        try:
            variable = BitBucketVariable(
                requester=requester,
                workspace=variable["workspace"],
                repo=variable["repo"],
                key=variable["key"],
                value=value,
            )
        except AttributeError as error:
            raise ConfigFileVariableError(f"key failure for config file: {error}")

        variable.upsert()
