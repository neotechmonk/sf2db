from pprint import pprint
from typing import Any, Dict, List

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker

from sf2db.util.config import ConfigFiles
from sf2db.util.json_reader import read_json

from .model_factory import (DBTableDefinition, generate_db_table,
                            generate_db_table_definition)
from .models import Base, DBTable


class TableAlreadyExistsError(Exception):
    """Raised when new table is attempted to be created while there is already one in existence."""
    pass

TableDefinitionJSONData =  Dict[str, Dict[str, Any]]

def setup_tables(db_uri : str, config_data : TableDefinitionJSONData):
    table_definitions :list[DBTableDefinition] = generate_db_table_definition(config_data)

    tables : List = []

    engine = create_engine(db_uri)    
    for definition in table_definitions:
        db_table = generate_db_table(definition)
        tables.append(db_table)
        try: 
            Base.metadata.create_all(bind  = engine)
        except InvalidRequestError as e : # TODO: this error is too generic
            raise TableAlreadyExistsError(f"Table {definition.table_name} cannot be created. Table with same name already exists - {str(e)}")
        finally:
            Base.metadata.clear()
       

    

# if __name__ == "__main__":


#     from sqlalchemy import Column, Integer, String

#     from cmcs.db.engine import DBSession

#     # class User(Base):
#     #     __tablename__ = 'users'
#     #     id = Column(Integer, primary_key=True)
#     #     name = Column(String(50))
#     #     email = Column(String(100))

#     DB_URI = ConfigFiles.DB_URI
    
#     try: 
#         setup_tables(config_file=ConfigFiles.DB_TABLES,
#                     config_reader=read_json)
#     except TableAlreadyExistsError as e: 
#         print(f"ERRORED {str(e)}")
#     finally: 
#          # Define the User class representing the 'users' table
   
        
#         with DBSession(DB_URI) as session:
            
#             new_user = DBTable(name='Jane Smith', email='jane@example.com')
#             session.add(new_user)

#             # user = session.query(User).filter_by(name='John Doe').first()
#             # print(f"{user.id}, {user.email}, {user.email}")


   
