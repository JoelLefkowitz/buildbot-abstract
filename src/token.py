import json
import logging

import requests
from hvac import Client
from retry import retry

logger = logging.getLogger(__name__)
exceptions = (FileNotFoundError, requests.exceptions.ConnectionError)
soft_retry = retry(exceptions, tries=10, delay=1, backoff=2, logger=logger)


class TokenClient(Client):
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token

    @soft_retry
    def list(self, path):
        return super().__init__(path)

    @soft_retry
    def write(self, path, wrap_ttl=None, **kwargs):
        return super().__init__(path, wrap_ttl, **kwargs)

    @classmethod
    @soft_retry
    def try_token_path(cls, path):
        token = cls.parse_token(path)
        return cls(token)

    @staticmethod
    def parse_token(path):
        with open(path) as stream:
            token = json.loads(stream.read())["token"]
            return token["auth"]["client_token"]
