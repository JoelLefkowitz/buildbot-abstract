import json
import logging

from hvac import Client
from retry import retry


class TokenClient(Client):
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token

    @classmethod
    @retry(
        (FileNotFoundError, ConnectionError),
        tries=10,
        delay=1,
        backoff=2,
        logger=logging.getLogger(__name__),
    )
    def try_token_path(cls, path):
        token = cls.parse_token(path)
        return cls(token)

    @staticmethod
    def parse_token(path):
        with open(path) as stream:
            token = json.loads(stream.read())["token"]
            return token["auth"]["client_token"]