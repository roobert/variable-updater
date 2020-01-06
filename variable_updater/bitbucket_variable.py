#!/usr/bin/env python3

from urllib.parse import urljoin
from dataclasses import dataclass


@dataclass
class BitBucketVariable:
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
        return self.requester.get(self.url())

    def insert(self):
        return self.requester.post(self.url(), self.payload())

    def delete(self):
        return self.requester.delete(self.url(variable=True))

    def update(self):
        return self.requester.put(self.url(variable=True), self.payload())

    def payload(self):
        return {"key": self.key, "value": self.value, "secured": True}
