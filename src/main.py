from sf2db import app
from sf2db.app.app import App
from sf2db.app.config import ConfigFiles
from sf2db.salesforce import SFAdapters
from sf2db.util.path import absolute

if __name__ == "__main__":
    this_file_path  = __file__
                                                   
    SF_CREDENTIALS_PATH = absolute (this_file_path, ConfigFiles.SALESFORCE_CREDENTIALS)
    SF2DB_MAPPINGS_PATH = absolute (this_file_path, ConfigFiles.SF2DB_MAPPINGS)
    DB_TABLE_DEFINITIONS_PATH = absolute (this_file_path, ConfigFiles.DB_TABLES)
    DB_CONFIG_PATH = absolute (this_file_path, ConfigFiles.DB_COFIG)
    SALESFORCE_CLIENT_ADAPTER = SFAdapters.SimpleSalesforceAdapter
   
    app = App(path_db_table_def=DB_TABLE_DEFINITIONS_PATH, 
              path_db_uri=DB_CONFIG_PATH, 
              path_sf_credentials=SF_CREDENTIALS_PATH, 
              path_sf2db_mappings=SF2DB_MAPPINGS_PATH,
              salesforce_client_adapter=SALESFORCE_CLIENT_ADAPTER)
    
    app.run()