"""
    1. Read the sf to db config
    2. Check if the DB config matches
    3. Construct SOQL
    4. Get data from SF
    5. Wrte data to DB
"""
from typing import Callable, Dict, List

from sf2db.db.model_factory import (generate_db_table,
                                    generate_db_table_definition)
from sf2db.db.models import DBTable
from sf2db.mapping.model_factory import mapping_factory
from sf2db.mapping.models import TableMapping
from sf2db.salesforce_lib import SFAdapters, SFInterface
from sf2db.util import config, json_reader, yaml_reader

# from sf2db.salesforce_lib.SimpleSalesforceAdapter 


JSONConfig = Callable[[str], Dict[str, Dict[str, str]]]
Sf2DB_MappingFactoryFn = Callable[[JSONConfig], TableMapping]

def read_sf_2_db_mapping(mapping_configs : List[JSONConfig], 
                         factory_fn : Sf2DB_MappingFactoryFn)->List[TableMapping]:
    
    mappings : List[TableMapping] = [factory_fn(mapping) for mapping in mapping_configs]
    return mappings

db_table_factory = lambda definition_config: generate_db_table(db_table_definition=generate_db_table_definition(definition_config))


if __name__ == "__main__":
    mapping_configs : List [JSONConfig] = json_reader.read_json(config.ConfigFiles.SF2DB_MAPPINGS)
    # print(mapping_configs)
    db_tables_configs :List[JSONConfig] = json_reader.read_json(config.ConfigFiles.DB_TABLES)
    # print(db_tables_configs)


    # print(salesforce_credentials)
    mappings = read_sf_2_db_mapping(mapping_configs = mapping_configs, factory_fn = mapping_factory)

    salesforce_credentials  = yaml_reader.read_yaml(config.ConfigFiles.CREDENTIALS)
    sales_force_client : SFInterface.SFInterface = SFAdapters.SimpleSalesforceAdapter(salesforce_credentials)
    sales_force_client.login()
    print(sales_force_client.connection.session_id)

    for sf2db_mapping in mappings:
        # print(sf2dbmapping)    
        db_table_config = next((config for config in db_tables_configs if config.get('tablename') == sf2db_mapping.db_table_name), None)
        # print(db_table_definition)
        db_table: DBTable = db_table_factory(db_table_config)
        print (db_table)


    