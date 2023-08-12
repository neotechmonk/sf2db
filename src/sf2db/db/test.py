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

from sf2db.db.model_factory import (DBTableDefinition, generate_db_table,
                                    generate_db_table_definition)
from sf2db.db.models import DBTable, to_dict
from sf2db.db.session import DBSession
from sf2db.db.setup_tables import (TableAlreadyExistsError,
                                   TableDefinitionJSONData, setup_tables)
from sf2db.util.config import ConfigFiles
from sf2db.util.json_reader import read_json


def define_table_by_name(desired_table_name: str, 
                         table_def_json_data:TableDefinitionJSONData) -> DBTable:
    table_definitions = generate_db_table_definition(table_def_json_data)
    for table_definition in table_definitions:
        if table_definition.table_name == desired_table_name:
            return generate_db_table(table_definition)
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


# # User data to be added to the table
USER_DATA = [
    {
        "Id": "232",
        "Name": "John",
        "PersonEmail": None,
        "CreatedDate": "2023-08-01T12:00:00",
        "IsDeleted": True
    },
    {
        "Id": "233",
        "Name": "Jane",
        "PersonEmail": "jane@example.com",
        "CreatedDate": "2023-08-02T10:30:00",
        "IsDeleted": False
    },
    {
        "Id": "234",
        "Name": "Alice",
        "PersonEmail": "alice@example.com",
        "CreatedDate": "2023-07-30T15:15:00",
        "IsDeleted": True
    },
    {
        "Id": "235",
        "Name": "Bob",
        "PersonEmail": "bob@example.com",
        "CreatedDate": "2023-07-28T08:45:00",
        "IsDeleted": False
    },
    {
        "Id": "236",
        "Name": "Eve",
        "PersonEmail": "eve@example.com",
        "CreatedDate": "2023-08-03T14:00:00",
        "IsDeleted": True
    }
]


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
    # delete_sqlite_db(DB_URI)

    # Setup database tables - no need to separately do this as SQL Alchmey takes care of this automatically
    # setup_db_tables(db_uri=DB_URI, 
    #                 table_def_json_data=table_definition_json )

    # Dynamically define the table class to interact with
    user_table  = define_table_by_name(desired_table_name="Users",
                                       table_def_json_data=table_definition_json)

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
       