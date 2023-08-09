"""
    1. Setup database tables
    2. Dynamically create DB Tables
    3. Insert data
"""

import os
from datetime import datetime
from pprint import pprint

from cmcs.db.engine import DBSession
from cmcs.db.model_factory import (DBTableDefinition,
                                   create_db_table_definitions,
                                   create_dynamic_db_table)
from cmcs.db.models import DBTable, to_dict
from cmcs.db.setup_tables import TableAlreadyExistsError, setup_tables
from cmcs.util.config import ConfigFiles
from cmcs.util.json_reader import read_json


def define_table_by_name (desired_table_name : str) -> DBTable:
    table_definitions = create_db_table_definitions(read_json(ConfigFiles.DB_TABLES))
    for table_definition in table_definitions:
        if table_definition.table_name == desired_table_name:
            db_table_class = None
            db_table_class = create_dynamic_db_table(table_definition)
            print(db_table_class)
            return db_table_class
    else:
        print(f"Table definition for {desired_table_name} not found.")

def setup_db_tables(table_config_file : str):
    try: 
        setup_tables(config_file=table_config_file,
                    config_reader=read_json)
    except TableAlreadyExistsError as e: 
        print(f"Table already exist. No new table created {str(e)}")

        import os

def delete_sqlite_db(db_file:str):
    stripped_path = db_file.replace("sqlite:///", "")

    if os.path.exists(stripped_path):
        os.remove(stripped_path)
        print(f"Database file '{stripped_path}' deleted.")
    else:
        print(f"Database file '{stripped_path}' does not exist.")



if __name__ == "__main__":
    table_definition_config_file = ConfigFiles.DB_TABLES
    DB_URI=ConfigFiles.DB_URI
    #Delete the SQL Lite .DB file
    # delete_sqlite_db(DB_URI)

    # Setup database tables
    setup_db_tables(table_config_file=table_definition_config_file)

    # Dynamically define the table class to interact with
    user_table  = define_table_by_name("Users")

    # # User data to be added to the table
    USER_DATA = [

        {
            "id": 232,
            "name": "John",
            "email": "doe@example.com",
            "created_at": "2023-08-01T12:00:00",
            "is_active": True
        },
        {
            "id": 233,
            "name": "Jane",
            "email": "jane@example.com",
            "created_at": "2023-08-02T10:30:00",
            "is_active": False
        },
        {
            "id": 234,
            "name": "Alice",
            "email": "alice@example.com",
            "created_at": "2023-07-30T15:15:00",
            "is_active": True
        },
        {
            "id": 235,
            "name": "Bob",
            "email": "bob@example.com",
            "created_at": "2023-07-28T08:45:00",
            "is_active": False
        },
        {
            "id": 236,
            "name": "Eve",
            "email": "eve@example.com",
            "created_at": "2023-08-03T14:00:00",
            "is_active": True
        }
    ]

    with DBSession(DB_URI) as insert_session:
        for user_data in USER_DATA:
            created_at_str = user_data.pop("created_at")  # Remove created_at from user data
            created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%S")  # Parse created_at string
            
            # Remove the "id" attribute
            stripped_user_data = {key: value for key, value in user_data.items() if key != "id"}
            
            _new_user = user_table(created_at=created_at, **stripped_user_data)  # Create the new user
            insert_session.add(_new_user)
    
    with DBSession(DB_URI) as read_session:
        stored_users = read_session.query(user_table).all()
        for stored_user in stored_users:
            pprint(to_dict(stored_user))
       