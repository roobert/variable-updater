#!/usr/bin/env python

import sys

from urllib3.exceptions import ProtocolError
from requests.exceptions import HTTPError, RequestException

from .cli import EnvironmentVariableError
from .config_file import ConfigFileOpenError
from .vault import VaultKeyError, VaultKeyAccessError, VaultServerError, VaultAuthError
from .bitbucket_requester import BitBucketGetError
from .variable_updater import ConfigFileVariableError, variable_updater


def main():
    try:
        variable_updater()
    except (
        ProtocolError,
        HTTPError,
        RequestException,
        BitBucketGetError,
        ConfigFileOpenError,
        ConfigFileVariableError,
        EnvironmentVariableError,
        VaultKeyError,
        VaultKeyAccessError,
        VaultServerError,
        VaultAuthError,
    ) as error:
        print(f"{error.__class__.__name__}: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
