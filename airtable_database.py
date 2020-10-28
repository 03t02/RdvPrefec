from airtable.airtable import Airtable
from airtable_config import AirtableConfig


class AirtableDatabase:
    __config: AirtableConfig = None

    def __init__(self, config):
        self.__config = config

    def get_table(self, table_name: str):
        return Airtable(
            self.__config.get_base_key(),
            table_name,
            self.__config.get_api_key()
        )