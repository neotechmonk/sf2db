import datetime
from dataclasses import dataclass, field
from enum import Enum
from pprint import pprint
from typing import Any, Callable, List

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String

from cmcs.util.config import ConfigFiles
from cmcs.util.json_reader import read_json

from .models import DBTable, to_dict


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
    is_primary_key : bool =field(default=False)
    column_length: int = field(default=None)  # Length is only applicable to `sqlalchemy.String`


@dataclass
class DBTableDefinition():  
    """Representation of db_tables.json's table definition
    Limitation : does not support relationship between tables
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


JSONTableDefinition = Callable[[str], List[dict[str, Any]]]
def create_db_table_definitions(table_definition_data: JSONTableDefinition) -> List[DBTableDefinition]:

    db_table_definitions = []
    
    for table_def_block in table_definition_data:
        columns = [
            DBColumnDefinition(
                column_name=column_def['name'],
                column_type=column_def.get('type'),
                column_length=column_def.get('length'),
                is_primary_key=column_def.get('primary_key', False)
            )
            for column_def in table_def_block['columns']
        ]
        
        table_definition = DBTableDefinition(table_name=table_def_block["tablename"], columns=columns)
        db_table_definitions.append(table_definition)

    return db_table_definitions


    
def create_dynamic_db_table(db_table_definition:DBTableDefinition)-> DBTable:
    class_attrs = {'__tablename__': db_table_definition.table_name}
    
    for column in db_table_definition.columns:

        _col_type = getattr(SQLAlchemyColumnType, column.column_type)
        # SQLAlchemyColumnType.String requires in Column
        
        if _col_type == SQLAlchemyColumnType.String:
            class_attrs[column.column_name] = Column(_col_type.value(column.column_length), 
                                                     primary_key=column.is_primary_key)
        else:
            class_attrs[column.column_name] = Column(_col_type.value, 
                                                     primary_key=column.is_primary_key)

    dt_table = type(db_table_definition.table_name, (DBTable,), class_attrs)
    return dt_table



if __name__ == '__main__':
    table_definitions = create_db_table_definitions(read_json(ConfigFiles.DB_TABLES))
    # print (SQLAlchemyColumnType.Integer.value)
    user_data = {
        "id": 232,
        "name": "John",
        "email": "doe@example.com",
        "created_at": datetime.datetime.now(),
        "is_active": True}
    for definition in table_definitions: 
        db_table = create_dynamic_db_table(definition)
        print(type(db_table))

        # user = db_table(id = 232,first_name="John", last_name="Doe", email_address="doe@example.com")
        user = db_table(**user_data)
        pprint(to_dict(user))