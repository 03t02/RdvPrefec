import sys

from utils import key_exists, key_not_exists
from constants import AIRTABLE, BASE_KEY, API_KEY


class AirtableConfig:
    __base_key: str = None
    __api_key: str = None

    def __init__(self, config):
        if key_exists('airtable', config):
            if key_not_exists(BASE_KEY, config[AIRTABLE]):
                sys.exit('[ERROR]: airtable.base_key is not exist.')
            if key_not_exists(API_KEY, config[AIRTABLE]):
                sys.exit('[ERROR]: airtable.api_key is not exist.')

            self.__base_key = config[AIRTABLE][BASE_KEY]
            self.__api_key = config[AIRTABLE][API_KEY]

    def get_base_key(self) -> str:
        return self.__base_key

    def get_api_key(self) -> str:
        return self.__api_key
