import datetime
from dataclasses import field
from enum import Enum
from pprint import pprint
from typing import List

from attr import dataclass
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String

from cmcs.db.models import DBTable
from cmcs.util.config import ConfigFiles
from cmcs.util.json_reader import read_json

from .models import to_dict


class SQLAlchemyColumnType(Enum):
    """Mapping between db_tables.json's column types to SQLAlchemy Column types
        E.g. 
        ......
        {
                "name": "email",
                "type": "String",
                "length": 100
            },
        {
            "name": "created_at",
            "type": "DateTime"
        }
            ....
    """
    Integer = Integer
    String = String
    Float = Float
    Boolean = Boolean
    DateTime = DateTime
    

@dataclass
class DBColumnDefinition():
    """Representation of db_tables.json's column definition
        E.g.
            .....
            {
                    "name": "id",
                    "type": "Integer",
                    "primary_key": true
                },
            {
                "name": "name",
                "type": "String",
                "length": 50
            },
            ....
    """
    column_name : str
    column_type:str 
    is_primary_key : SQLAlchemyColumnType
    column_length: int = field(default=None)  # Length is only applicable to sqlalchemy.String


@dataclass
class DBTableDefinition():  
    """Representation of db_tables.json's table definition
    Columns of the tables of type `DBColumnDefinition`
        E.g.
            .....
            {
            "tablename": "users",
            "columns": [
                {
                    "name": "id",
                    "type": "Integer",
                    "primary_key": true
                },
            ....
    """
    table_name : str
    columns: list[DBColumnDefinition]
    


def create_db_table_definition(table_name: str, 
                               columns: List[tuple[str, str, int, bool]]) -> DBTableDefinition:
    db_columns = []

    for column_name, column_type, column_length, is_primary_key in columns:
        
        column_type_enum = getattr(SQLAlchemyColumnType, column_type)
        column_definition = DBColumnDefinition(column_name=column_name,
                                               column_type=column_type_enum,
                                               column_length=column_length,
                                               is_primary_key=is_primary_key)
        db_columns.append(column_definition)

    table_definition = DBTableDefinition(table_name=table_name, columns=db_columns)
    return table_definition


def create_db_table_definitions(definition_file : str) -> List[DBTableDefinition]:

    definition_json = read_json(definition_file)
    

    db_table_definitions = []
    
    for table_def_block in definition_json:
        table_name = table_def_block["tablename"]
        columns = []

        for column_def in table_def_block['columns']:
            column_name = column_def['name']
            column_type = column_def['type']
            column_length = column_def.get('length', None)
            is_primary_key = column_def.get('primary_key', False)

            columns.append((column_name, column_type, column_length, is_primary_key))
           
        table_definition = create_db_table_definition(table_name=table_name, columns=columns)
        # pprint(table_definition)
        db_table_definitions.append(table_definition)

    return db_table_definitions


    
def create_db_table(table_definition:DBTableDefinition)-> DBTable:
    class_attrs = {
        '__tablename__': table_definition.table_name
        }
    
    for column in table_definition.columns:
        if column.column_type == SQLAlchemyColumnType.String:
            class_attrs[column.column_name] = Column(column.column_type.value(column.column_length), 
                                                     primary_key=column.is_primary_key)
        else:
            class_attrs[column.column_name] = Column(column.column_type.value, 
                                                     primary_key=column.is_primary_key)

    dt_table = type(table_definition.table_name, (DBTable,), class_attrs)
    return dt_table



if __name__ == '__main__':
    table_definitions = create_db_table_definitions(definition_file=ConfigFiles.DB_TABLES)
    # print (SQLAlchemyColumnType.Integer.value)
    user_data = {
        "id": 232,
        "name": "John",
        "email": "doe@example.com",
        "created_at": datetime.datetime.now(),
        "is_active": True}
    for definition in table_definitions: 
        db_table = create_db_table(definition)
        print(type(db_table))

        # user = db_table(id = 232,first_name="John", last_name="Doe", email_address="doe@example.com")
        user = db_table(**user_data)
        pprint(to_dict(user))