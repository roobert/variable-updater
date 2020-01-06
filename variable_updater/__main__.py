#!/usr/bin/env python

import sys
from urllib3.exceptions import ProtocolError
from requests.exceptions import ConnectionError, HTTPError, RequestException

from .cli import parse_args, environment_variables, EnvironmentVariableError
from .config_file import ConfigFileError, variables
from .vault import Vault, VaultKeyError, VaultServerError, VaultAuthError
from .bitbucket_requester import BitBucketRequester, BitBucketGetError
from .bitbucket_variable import BitBucketVariable


def main():
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
            raise ConfigFileError(f"key failure for config file: {error}")

        variable.upsert()


if __name__ == "__main__":
    try:
        main()
    except (
        ConfigFileError,
        EnvironmentVariableError,
        AttributeError,
        VaultKeyError,
        VaultServerError,
        VaultAuthError,
        BitBucketGetError,
        ProtocolError,
        ConnectionError,
        HTTPError,
        OSError,
        RequestException,
    ) as error:
        print(f"{type(error)}: {error}")
        sys.exit(1)
