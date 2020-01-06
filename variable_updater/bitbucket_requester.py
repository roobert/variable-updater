#!/usr/bin/env python3

import requests
from dataclasses import dataclass


class BitBucketGetError(Exception):
    pass


@dataclass
class BitBucketRequester:
    username: str
    password: str

    def auth(self):
        return requests.auth.HTTPBasicAuth(self.username, self.password)

    def headers(self):
        return {"Content-Type": "application/json"}

    def get(self, url):
        response = requests.get(url, auth=self.auth(), headers=self.headers())
        response.raise_for_status()
        return response

    def put(self, url, payload):
        return requests.put(url, json=payload, auth=self.auth(), headers=self.headers())

    def post(self, url, payload):
        return requests.post(
            url, json=payload, auth=self.auth(), headers=self.headers()
        )

    def delete(self, url):
        return requests.delete(url, auth=self.auth())
