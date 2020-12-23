import json

from hvac import Client
from retry import retry
import logging


class TokenClient(Client):
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token

    @retry(
        (FileNotFoundError, ConnectionError),
        tries=10,
        delay=1,
        backoff=2,
        logger=logging.getLogger(__name__),
    )
    @classmethod
    def try_token_path(cls, path):
        token = cls.parse_token(path)
        return cls(token)

    @staticmethod
    def parse_token(path):
        with open(path) as stream:
            return json.loads(stream.read())["token"]
