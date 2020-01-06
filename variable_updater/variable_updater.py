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


def bitbucket_requester_client(vault, config):
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
    bitbucket_requester = bitbucket_requester_client(vault, config)

    for variable in variables(args.config):
        try:
            vault_mount = variable["vault_mount"]
            vault_path = variable["vault_path"]
            vault_key = variable["vault_key"]
            bitbucket_workspace = variable["bitbucket_workspace"]
            bitbucket_repo = variable["bitbucket_repo"]
            bitbucket_key = variable["bitbucket_variable"]
        except KeyError as error:
            raise ConfigFileVariableError(
                f"missing required key from config file variable mapping: {error}"
            )

        print(f"vault read: {vault_mount}:{vault_path} - {vault_key}")
        value = vault.read(vault_mount, vault_path, vault_key)

        print(
            f"bitbucket write: {bitbucket_workspace}/{bitbucket_repo} - {bitbucket_key}"
        )

        BitBucketVariable(
            requester=bitbucket_requester,
            workspace=bitbucket_workspace,
            repo=bitbucket_repo,
            key=bitbucket_key,
            value=value,
        ).upsert()
