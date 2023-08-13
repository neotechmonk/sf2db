
from dataclasses import dataclass, field
from typing import Any, Callable, List, Tuple, Type

import sqlalchemy

from .models import DBTable


# region Utility function => SQLAlchemy Type
class SQLAlchemyTypeError(Exception):
    """Raised when Column does not match a permitted `sqlalchemy` type."""
    pass


ALLOWED_SQLALCHEMY_TYPES: Tuple[Type, ...] = (
                                  sqlalchemy.Integer,
                                  sqlalchemy.String,
                                  sqlalchemy.Float,
                                  sqlalchemy.Boolean,
                                  sqlalchemy.DateTime)

def get_sqlalchemy_type(type_name: str)-> ALLOWED_SQLALCHEMY_TYPES:
    """"""

    sqlalchemy_type = getattr(sqlalchemy, type_name, None)

    if sqlalchemy_type is None :
        raise SQLAlchemyTypeError(f"SQLAlchemy type can not be None")
    elif sqlalchemy_type not in ALLOWED_SQLALCHEMY_TYPES:
        valid_types = ", ".join([allowed_type.__name__ for allowed_type in ALLOWED_SQLALCHEMY_TYPES])
        raise SQLAlchemyTypeError(f"SQLAlchemy type '{type_name}' must be one of {valid_types}")

    return sqlalchemy_type

# endregion

# region Dynamic definition of SQL Tables
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


class TableDefinitionGenerationError(Exception):
    """
    Raised when there is an error during the generation of a DBTableDefinition.
    This exception indicates issues related to generating table definitions.
    """

JSONTableConfig = Callable[[str], List[dict[str, Any]]]
def generate_db_table_definition(definition_config: JSONTableConfig) -> DBTableDefinition:
    try:
        columns = [
            DBColumnDefinition(
                column_name=column_def['name'],
                column_type=column_def.get('type'),
                column_length=column_def.get('length'),
                is_primary_key=column_def.get('primary_key', False)
            )
            for column_def in definition_config['columns']
        ]

        table_definition = DBTableDefinition(table_name=definition_config["tablename"], columns=columns)

        return table_definition
    except (KeyError, AttributeError, TypeError, ValueError) as e:
        raise TableDefinitionGenerationError(f"Error generating table definition :  {str(e)}")

    
# endregion

class DBTableGenerationError(Exception):
    """
    Raised when there is an error during the dynamic generation of a DBTable's sub Classes.
    """
# region Create SQL Tables dynamically based on DBTableDefinition
def generate_db_table(db_table_definition:DBTableDefinition)-> DBTable:
    class_attrs = {'__tablename__': db_table_definition.table_name}
    try: 
        for column in db_table_definition.columns:
            sqlalchemy_col_type = get_sqlalchemy_type (type_name = column.column_type )
        
            # SQLAlchemyColumnType.String requires in Column
            if isinstance(sqlalchemy_col_type, sqlalchemy.String):
                class_attrs[column.column_name] = sqlalchemy.Column(sqlalchemy_col_type(column.column_length),
                                                        primary_key=column.is_primary_key)
            else:
                class_attrs[column.column_name] = sqlalchemy.Column(sqlalchemy_col_type,
                                                        primary_key=column.is_primary_key)

        dt_table = type(db_table_definition.table_name, (DBTable,), class_attrs)
        return dt_table
    except Exception as e:
        raise DBTableGenerationError(f"Error generating subclass of `DBTable` for table {db_table_definition.table_name}") from e 
# endregion


# if __name__ == '__main__':

    # from sf2db.util.config import ConfigFiles
    # from sf2db.util.json_reader import read_json
#     table_definitions = create_db_table_definitions(read_json(ConfigFiles.DB_TABLES))
#     user_data = {
#         "id": 232,
#         "name": "John",
#         "email": "doe@example.com",
#         "created_at": datetime.datetime.now(),
#         "is_active": True}
#     for definition in table_definitions:
#         db_table = create_dynamic_db_table(definition)
#         print(type(db_table))
#         user = db_table(**user_data)
#         pprint(to_dict(user))
