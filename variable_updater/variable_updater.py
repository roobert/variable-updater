#!/usr/bin/env python

import os
import sys
import argparse
import yaml
import hvac

from variable_updater.bitbucket.variable import Variable
from variable_updater.bitbucket.requester import Requester

# logging.basicConfig(
#    format="%(levelname)s - %(message)s",
#    datefmt="%m/%d/%Y %I:%M:%S %p",
#    level=logging.INFO,
# )
# logger = logging.getLogger(__name__)

DESCRIPTION = "update bitbucket variables with values stored in vault"


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument("-c", "--config", help="config file")

    return parser.parse_args()


def variables(config):
    try:
        with open(config, "r") as data:
            return yaml.safe_load(data)["variables"]

    except:
        print("error: failed to load config file!")


class Vault:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.vault = self.client()

    def client(self):
        try:
            vault = hvac.Client(url=self.server)
            vault.auth_userpass(self.username, self.password)

            if not vault.is_authenticated():
                print("error: failed to authenticate with vault server!")
                sys.exit(1)

            return vault

        except hvac.exceptions.InvalidRequest as error:
            print(f"error: failed to connect to vault server: {error}")
            sys.exit(1)

    def read(self, mount, key):
        try:
            print(f"==> vault read: {key}")
            data = self.vault.secrets.kv.v2.read_secret_version(
                mount_point=mount, path=key
            )

            if not data:
                print(f"warning: no data found for key: {key}")
                return None

            # NOTE: our key values are always under the key named "value"
            return data["data"]["data"]["value"]

        except hvac.exceptions.Forbidden as error:
            print(f"error: could not read key '{key}': {error}")
            sys.exit(1)


def main():
    args = parse_args()

    try:
        vault_server = os.environ["VAULT_ADDR"]
        vault_username = os.environ["VAULT_USERNAME"]
        vault_password = os.environ["VAULT_PASSWORD"]
        vault_bitbucket_key_mount  = os.environ["VAULT_BITBUCKET_KEY_MOUNT"]
        vault_bitbucket_username_key = os.environ["VAULT_BITBUCKET_USERNAME_KEY"]
        vault_bitbucket_password_key = os.environ["VAULT_BITBUCKET_PASSWORD_KEY"]
    except KeyError as error:
        print(f"error: failure reading environment variable: {error}")
        sys.exit(1)

    vault = Vault(server=vault_server, username=vault_username, password=vault_password)

    bitbucket_username = vault.read(
        vault_bucket_key_mount, vault_bitbucket_username_key
    )
    bitbucket_password = vault.read(
        vault_bucket_key_mount, vault_bitbucket_password_key
    )

    # NOTE: generate an "app password" with edit variables permissions
    requester = Requester(username=bitbucket_username, password=bitbucket_password,)

    for variable in variables(args.config):
        value = vault.read(variable["vault_mount"], variable["value"])

        try:
            variable = Variable(
                requester=requester,
                workspace=variable["workspace"],
                repo=variable["repo"],
                key=variable["key"],
                value=value,
            )
        except AttributeError as error:
            print(f"error: key failure for config file: {error}")

        variable.upsert()


if __name__ == "__main__":
    main()
