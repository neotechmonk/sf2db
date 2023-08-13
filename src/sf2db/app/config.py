
from enum import StrEnum


class Configs(StrEnum):
    SALESFORCE_CREDENTIALS = '../config/salesforce_credentatials.yaml'
    SF2DB_MAPPINGS = '../config/salesforce_to_db.json'
    DB_TABLES = '../config/db_tables.json'
    DB_COFIG = '../config/db_config.yaml'
    LOGGER_CONFIG = '../config/logger_config.json'
    LOGGER_APP_NAME = "sf2db-logger"