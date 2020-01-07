#!/usr/bin/env python

import argparse
from .version import __version__


def version():
    return __version__


def parse_args():
    description = "update bitbucket variables with values stored in vault"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-c", "--config", help="config file")
    parser.add_argument("-v", "--version", action="version", version=version())
    return parser.parse_args()
