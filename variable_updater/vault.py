#!/usr/bin/env python

import hvac


class VaultAuthError(Exception):
    pass


class VaultKeyAccessError(Exception):
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

    def read(self, mount, path, key):
        try:
            data = self.vault.secrets.kv.v2.read_secret_version(
                mount_point=mount, path=path
            )

            if not data:
                raise VaultKeyError(f"no data found for: {mount}:{path} - {key}")

            return data["data"]["data"][key]

        except hvac.exceptions.Forbidden as error:
            raise VaultKeyAccessError(
                f"could not read: {mount}:{path} - {key}: {error}"
            )
