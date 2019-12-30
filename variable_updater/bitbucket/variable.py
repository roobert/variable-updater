#!/usr/bin/env python3

import json
import requests
import logging
from time import sleep
from urllib.parse import urljoin
from dataclasses import dataclass

logging.basicConfig(
    format="%(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@dataclass
class Variable:
    requester: str
    workspace: str
    repo: str
    key: str
    value: str

    def url(self, variable=None):
        if variable:
            path = f"/2.0/repositories/{self.workspace}/{self.repo}/pipelines_config/variables/{self.uuid()}"
        else:
            path = f"/2.0/repositories/{self.workspace}/{self.repo}/pipelines_config/variables/"
        return urljoin("https://api.bitbucket.org/", path)

    def uuid(self):
        for value in self.select().json().get("values", []):
            if value["key"] == self.key:
                return value["uuid"]
        return None

    def upsert(self):
        if self.uuid():
            self.update()
        else:
            self.insert()

    def select(self):
        logger.info(f"selecting key: {self.workspace}/{self.repo}:{self.key}")
        return self.requester.get(self.url())

    def insert(self):
        logger.info(f"inserting key: {self.workspace}/{self.repo}:{self.key}")
        return self.requester.post(self.url(), self.payload())

    def delete(self):
        logger.info(f"deleting key: {self.workspace}/{self.repo}:{self.key}")
        return self.requester.delete(self.url(variable=True))

    def update(self):
        logger.info(f"updating key: {self.workspace}/{self.repo}:{self.key}")
        return self.requester.put(self.url(variable=True), self.payload())

    def payload(self):
        return {"key": self.key, "value": self.value, "secured": True}
