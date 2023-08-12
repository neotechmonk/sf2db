

from enum import StrEnum


class ConfigFiles(StrEnum):
    CREDENTIALS = '../config/login.yaml'
    OBJECT_MAPPINGS = '../config/object_mappings.json'
    DB_TABLES = '../config/db_tables.json'
    DB_URI = 'sqlite:///example.db'