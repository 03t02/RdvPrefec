import sys

from utils import key_exists, key_not_exists
from constants import TWILO, ACCOUNT_SID, AUTH_TOKEN


class TwiloConfig:
    __account_sid: str = None
    __auth_token: str = None

    def __init__(self, config):
        if key_exists(TWILO, config):
            if key_not_exists(ACCOUNT_SID, config[TWILO]):
                sys.exit('[ERROR]: twilo.account_id is not exist.')
            if key_not_exists(AUTH_TOKEN, config[TWILO]):
                sys.exit('[ERROR]: twilo.auth_token is not exist.')

            self.__account_sid = config[TWILO][ACCOUNT_SID]
            self.__auth_token = config[TWILO][AUTH_TOKEN]

    def get_account_sid(self) -> str:
        return self.__account_sid

    def get_auth_token(self) -> str:
        return self.__auth_token
