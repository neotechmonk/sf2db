"""
    1. Delete the sqlite database
    2. Setup database tables
    3. Dynamically create DB Tables
    4. Insert data
    5. Read data

"""

import os
from datetime import datetime
from pprint import pprint
from typing import Any, Dict

from cmcs.db.engine import DBSession
from cmcs.db.model_factory import (DBTableDefinition,
                                   create_db_table_definitions,
                                   create_dynamic_db_table)
from cmcs.db.models import DBTable, to_dict
from cmcs.db.setup_tables import (TableAlreadyExistsError,
                                  TableDefinitionJSONData, setup_tables)
from cmcs.util.config import ConfigFiles
from cmcs.util.json_reader import read_json


def define_table_by_name(desired_table_name: str, 
                         table_def_json_data:TableDefinitionJSONData) -> DBTable:
    table_definitions = create_db_table_definitions(table_def_json_data)
    for table_definition in table_definitions:
        if table_definition.table_name == desired_table_name:
            db_table_class = None
            db_table_class = create_dynamic_db_table(table_definition)
            print(db_table_class)
            return db_table_class
    else:
        print(f"Table definition for {desired_table_name} not found.")

def setup_db_tables(db_uri:str, table_def_json_data:TableDefinitionJSONData):
    try: 
        setup_tables(db_uri=db_uri, config_data=table_def_json_data)
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
    # table_definition_config_file = ConfigFiles.DB_TABLES
    table_definition_json = [
            {
                "tablename": "Users",
                "columns": [
                    {
                        "name": "id",
                        "type": "Integer",
                        "primary_key": True
                    },
                    {
                        "name": "name",
                        "type": "String",
                        "length": 50
                    },
                    {
                        "name": "email",
                        "type": "String",
                        "length": 100
                    },
                    {
                        "name": "created_at",
                        "type": "DateTime"
                    },
                    {
                        "name": "is_active",
                        "type": "Boolean"
                    }
                ]
            }
    ]

    DB_URI=ConfigFiles.DB_URI
    #Delete the SQL Lite .DB file
    delete_sqlite_db(DB_URI)

    # Setup database tables
    setup_db_tables(db_uri=DB_URI, 
                    table_def_json_data=table_definition_json )

    # Dynamically define the table class to interact with
    user_table  = define_table_by_name(desired_table_name="Users",
                                       table_def_json_data=table_definition_json)

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
       