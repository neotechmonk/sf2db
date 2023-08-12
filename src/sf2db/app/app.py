"""
    1. Read the sf to db config
    2. Check if the DB config matches
    3. Construct SOQL
    4. Get data from SF
    5. Wrte data to DB
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from pprint import pprint
from typing import Callable, Dict, List

from sf2db.db.model_factory import (DBTableDefinition, generate_db_table,
                                    generate_db_table_definition)
from sf2db.db.models import DBTable
from sf2db.db.session import DBSession
from sf2db.mapping.model_factory import mapping_factory
from sf2db.mapping.models import TableMapping
from sf2db.mapping.sf_to_db_converter import convert
from sf2db.salesforce_lib import SFAdapters, SFInterface, soql
from sf2db.util import config, json_reader, yaml_reader
from sf2db.util.config import ConfigFiles

# from sf2db.salesforce_lib.SimpleSalesforceAdapter 


class App:
    def __init__(self,
                 path_sf_credentials: str,
                 path_sf2db_mappings: str,
                 path_db_table_def: str,
                 path_db_uri: str
                 ) -> None:
        self._path_sf_credentials = path_sf_credentials
        self._path_sf2db_mappings = path_sf2db_mappings
        self._path_db_table_def = path_db_table_def
        self._path_db_uri = path_db_uri

        self.db_session = DBSession(db_uri=self._path_db_uri)

        # Placehodlers of configs
        self.sf2db_mappings : List [TableMapping]
        self.db_tables : List[DBTable]

    def _load_sf2db_mappings(self):
        _config_data = json_reader.read_json(self._path_sf2db_mappings)
        self.sf2db_mappings = [mapping_factory (mapping = _cd) for _cd in _config_data]

    def _generate_db_tables(self):
        _config_data = json_reader.read_json(self._path_db_table_def)
        _db_table_defs :List [DBTableDefinition] = [generate_db_table_definition(definition_config= _cd) for _cd in _config_data]
        self.db_tables = [generate_db_table (db_table_definition=_t_def) for _t_def in _db_table_defs]

    def run(self):
       self._load_sf2db_mappings()
       self._generate_db_tables()

JSONConfig = Callable[[str], Dict[str, Dict[str, str]]]
Sf2DB_MappingFactoryFn = Callable[[JSONConfig], TableMapping]

def read_sf_2_db_mapping(mapping_configs : List[JSONConfig], 
                         factory_fn : Sf2DB_MappingFactoryFn)->List[TableMapping]:
    
    mappings : List[TableMapping] = [factory_fn(mapping) for mapping in mapping_configs]
    return mappings

db_table_factory = lambda definition_config: generate_db_table(db_table_definition=generate_db_table_definition(definition_config))


def func_main():

    mapping_configs : List [JSONConfig] = json_reader.read_json(config.ConfigFiles.SF2DB_MAPPINGS)
    # print(mapping_configs)
    db_tables_configs :List[JSONConfig] = json_reader.read_json(config.ConfigFiles.DB_TABLES)
    # print(db_tables_configs)


    # print(salesforce_credentials)
    mappings = read_sf_2_db_mapping(mapping_configs = mapping_configs, factory_fn = mapping_factory)

    salesforce_credentials  = yaml_reader.read_yaml(config.ConfigFiles.CREDENTIALS)
    sales_force_client : SFInterface.SFInterface = SFAdapters.SimpleSalesforceAdapter(salesforce_credentials)
    sales_force_client.login()
    # print(sales_force_client.connection.session_id)

    for sf2db_mapping in mappings:
        # print(sf2dbmapping)    
        db_table_config = next((config for config in db_tables_configs if config.get('tablename') == sf2db_mapping.db_table_name), None)
        # print(db_table_config)
        db_table: DBTable = db_table_factory(db_table_config)
        # print (db_table)
        soql_query= soql.build_soql_query(object_name =sf2db_mapping.salesforce_object_name, columns = [sf_fields.saleforce_field for sf_fields in sf2db_mapping.col_mappings])
        # print(soql)
        query_result = sales_force_client.query(soql_query)
        
        with DBSession(db_uri=config.ConfigFiles.DB_URI) as db_session: 
            for record in query_result:
                # Filter out the 'attributes' key from the record dictionary
                # filtered_record = {field: value for field, value in record.items() if field != 'attributes'}
                print(record)
                
                db_data = convert(sf_data=record, 
                                  salesforce_fields=[sf_fields.saleforce_field for sf_fields in sf2db_mapping.col_mappings],
                                  db_columns=[db_columns.db_column_name for db_columns in sf2db_mapping.col_mappings])
                

                print(db_data)
                db_record = db_table(**db_data)
                db_session.add(db_record)

if __name__ == "__main__":
    SF_CREDENTIALS = ConfigFiles.CREDENTIALS
    SF2DB_MAPPINGS = ConfigFiles.SF2DB_MAPPINGS
    DB_TABLE_DEFINITIONS = ConfigFiles.DB_TABLES
    DR_URI = ConfigFiles.DB_URI

    app = App(path_db_table_def=DB_TABLE_DEFINITIONS, 
              path_db_uri=DR_URI, 
              path_sf_credentials=SF_CREDENTIALS, 
              path_sf2db_mappings=SF2DB_MAPPINGS)
    
    app.run()
    print(app.db_tables)