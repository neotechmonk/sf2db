
from typing import List

from sf2db.db.model_factory import (generate_db_table,
                                    generate_db_table_definition)
from sf2db.db.models import DBTable
from sf2db.db.session import DBSession
from sf2db.mapping.model_factory import mapping_factory
from sf2db.mapping.models import TableMapping
from sf2db.salesforce import SFInterface, soql
from sf2db.util import json_reader, yaml_reader
from sf2db.util.sf_to_db_converter import convert


class App:
    def __init__(self,
                 path_sf_credentials: str,
                 path_sf2db_mappings: str,
                 path_db_table_def: str,
                 path_db_uri: str,
                 salesforce_client_adapter : SFInterface
                 ) -> None:
        self._path_sf_credentials = path_sf_credentials
        self._path_sf2db_mappings = path_sf2db_mappings
        self._path_db_table_def = path_db_table_def
        self._path_db_uri = path_db_uri


        self._sf_adapter = salesforce_client_adapter

        self.db_session = DBSession(db_uri=self._path_db_uri)
        self.sf_client :SFInterface = None

        # Placehodlers of configs
        self.sf2db_mappings : List [TableMapping]
        self.db_tables : List[DBTable]


    def _load_sf2db_mappings(self):
        """ Saves all mappings of Salesforce objects to DB Tables from `salesforce_to_db.json` """
        _config_data = json_reader.read_json(self._path_sf2db_mappings)
        self.sf2db_mappings = [mapping_factory (mapping = _cd) for _cd in _config_data]

    def _generate_db_tables(self):
        """ Generates SQLAlchemy.Base classes based on definitions in `salesforce_to_db.json`"""
        _config_data = json_reader.read_json(self._path_db_table_def)
        db_factory_fn = lambda definition_config: generate_db_table(db_table_definition=generate_db_table_definition(definition_config))
        self.db_tables = [db_factory_fn (definition_config=_t_def) for _t_def in _config_data]

    def _create_salesforce_connection(self):
        """ Logins to Salesforce using client adapter `self._sf_adapter`.
            `self._sf_adapter` confines to `SFInterface`
        """
        _credential_data = yaml_reader.read_yaml(self._path_sf_credentials)
        self.sf_client = self._sf_adapter(_credential_data)
        self.sf_client.login()
    
    def _persist_salesforce_to_db(self, mapping: TableMapping) -> None:
        """ Main function that downloads data for given `TableMapping` entry 
            in `salesforce_to_db.json`and saves in the database

            Key functions include:

            1. Creating the SOQL query string
            2. Fetching the data from Salesforce
            3. Coverting Salesforce results to be compatible with DBTable 
            4. Bulk inserts
        """
        # Extract field/column names
        _sf_object_fields = [sf_fields.saleforce_field for sf_fields in mapping.col_mappings]
        _db_table_columns =[db_columns.db_column_name for db_columns in mapping.col_mappings]

        # Find the matching DB table
        db_table: DBTable = next(
                            (dbt for dbt in self.db_tables 
                                  if dbt.__tablename__ == mapping.db_table_name), 
                                  None) 
        # Build SOQL query
        # TODO : make it a helper function of TableMapping ?
        soql_query = soql.build_soql_query(
            object_name=mapping.salesforce_object_name,
            columns=_sf_object_fields)
        
        # Fetch Salesforce results
        sf_results = self.sf_client.query(soql_query)

        # Prepare records for DB insertion
        db_records = [
        db_table(**convert(
            sf_data=record,
            salesforce_fields=_sf_object_fields,
            db_columns=_db_table_columns
        ))
        for record in sf_results]

        # Bulk insert records into the database
        with self.db_session as db_session:
            db_session.add_all(db_records)
     

    def run(self):
        """Run the data synchronization process.

            This method orchestrates the process of synchronizing data from Salesforce to the database.
            It loads mapping configurations, generates database tables, creates a Salesforce client,
            and then iterates through each mapping to persist data.

            This method encapsulates the complete data synchronization process.
        """
        self._load_sf2db_mappings()
        self._generate_db_tables()
        self._create_salesforce_connection()

        for mapping in self.sf2db_mappings:
            self._persist_salesforce_to_db(mapping = mapping)
