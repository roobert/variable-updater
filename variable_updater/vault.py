#!/usr/bin/env python

import hvac


class VaultAuthError(Exception):
    pass


class VaultServerError(Exception):
    pass


class VaultKeyError(Exception):
    pass


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
                raise VaultAuthError("failed to authenticate with vault server!")

            return vault

        except hvac.exceptions.InvalidRequest as error:
            raise VaultServerError(f"failed to connect to vault server: {error}")

    def read(self, mount, key):
        try:
            print(f"==> vault read: {key}")
            data = self.vault.secrets.kv.v2.read_secret_version(
                mount_point=mount, path=key
            )

            if not data:
                raise VaultKeyError(f"no data found for key: {key}")

            # NOTE: our key values are always under the key named "value"
            return data["data"]["data"]["value"]

        except hvac.exceptions.Forbidden as error:
            raise VaultKeyError(f"could not read key '{key}': {error}")
