import sys

from utils import key_exists, key_not_exists
from constants import AIRTABLE, ACCOUNT_SID, AUTH_TOKEN


class AirtableConfig:
    __account_sid: str = None
    __auth_token: str = None
    __base_key: str = None
    __api_key: str = None

    def __init__(self, config):
        if key_exists('airtable', config):
            if key_not_exists(ACCOUNT_SID, config[AIRTABLE]):
                sys.exit('[ERROR]: airtable.account_id is not exist.')
            if key_not_exists(AUTH_TOKEN, config[AIRTABLE]):
                sys.exit('[ERROR]: airtable.auth_token is not exist.')

            self.__account_sid = config[AIRTABLE][ACCOUNT_SID]
            self.__auth_token = config[AIRTABLE][AUTH_TOKEN]

    def get_account_sid(self) -> str:
        return self.__account_sid

    def get_auth_token(self) -> str:
        return self.__auth_token

    def get_base_key(self) -> str:
        return self.__base_key

    def get_api_key(self) -> str:
        return self.__api_key
