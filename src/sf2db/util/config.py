

from enum import StrEnum


class ConfigFiles(StrEnum):
    CREDENTIALS = '../config/salesforce_credentatials.yaml'
    SF2DB_MAPPINGS = '../config/salesforce_to_db.json'
    DB_TABLES = '../config/db_tables.json'
    DB_URI = 'sqlite:///example.db'