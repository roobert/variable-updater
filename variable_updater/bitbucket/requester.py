#!/usr/bin/env python3

import json
import requests
import logging
from urllib.parse import urljoin
from dataclasses import dataclass

logging.basicConfig(
    format="%(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


@dataclass
class Requester:
    username: str
    password: str

    def auth(self):
        return requests.auth.HTTPBasicAuth(self.username, self.password)

    def headers(self):
        return {"Content-Type": "application/json"}

    def get(self, url):
        response = requests.get(url, auth=self.auth(), headers=self.headers())
        if response.status_code != 200:
            logger.critical(f"error: {response.status_code}")
            exit(1)
        return response

    def put(self, url, payload):
        return requests.put(url, json=payload, auth=self.auth(), headers=self.headers())

    def post(self, url, payload):
        return requests.post(
            url, json=payload, auth=self.auth(), headers=self.headers()
        )

    def delete(self, url):
        return requests.delete(url, auth=self.auth())
