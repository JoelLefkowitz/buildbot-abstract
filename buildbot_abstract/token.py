import json
import logging

import requests
from hvac import Client
from retry import retry

logger = logging.getLogger(__name__)
exceptions = (FileNotFoundError, requests.exceptions.ConnectionError)
soft_retry = retry(
    exceptions, tries=10, delay=1, backoff=2, logger=logger
)


class TokenClient(Client):
    def __init__(self, url, token, *args, **kwargs):
        super().__init__(url, *args, **kwargs)
        self.token = token

    @soft_retry
    def list(self, path):
        return super().list(path)

    @soft_retry
    def write(self, path, secret, wrap_ttl=None, **kwargs):
        return super().write(
            path, secret=secret, wrap_ttl=wrap_ttl, **kwargs
        )

    @classmethod
    @soft_retry
    def try_token_path(cls, url, path):
        token = cls.parse_token(path)
        return cls(url, token)

    @staticmethod
    def parse_token(path):
        with open(path) as stream:
            token = json.loads(stream.read())["token"]
            return token["auth"]["client_token"]
