#!/usr/bin/env python

import sys

from urllib3.exceptions import ProtocolError
from requests.exceptions import ConnectionError, HTTPError, RequestException

from .cli import EnvironmentVariableError
from .config_file import ConfigFileOpenError
from .vault import VaultKeyError, VaultServerError, VaultAuthError
from .bitbucket_requester import BitBucketGetError
from .variable_updater import variable_updater, ConfigFileVariableError


def main():
    try:
        variable_updater()
    except (
        ConfigFileOpenError,
        ConfigFileVariableError,
        EnvironmentVariableError,
        VaultKeyError,
        VaultServerError,
        VaultAuthError,
        BitBucketGetError,
        ProtocolError,
        ConnectionError,
        HTTPError,
        RequestException,
    ) as error:
        print(f"{error.__class__.__name__}: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
