
from sf2db import app
from sf2db.app.app import App
from sf2db.app.config import ConfigFiles
from sf2db.salesforce import SFAdapters

if __name__ == "__main__":
    SF_CREDENTIALS = ConfigFiles.SALESFORCE_CREDENTIALS
    SF2DB_MAPPINGS = ConfigFiles.SF2DB_MAPPINGS
    DB_TABLE_DEFINITIONS = ConfigFiles.DB_TABLES
    DR_URI = ConfigFiles.DB_URI
    SALESFORCE_CLIENT_ADAPTER = SFAdapters.SimpleSalesforceAdapter
    
    app = App(path_db_table_def=DB_TABLE_DEFINITIONS, 
              path_db_uri=DR_URI, 
              path_sf_credentials=SF_CREDENTIALS, 
              path_sf2db_mappings=SF2DB_MAPPINGS,
              salesforce_client_adapter=SALESFORCE_CLIENT_ADAPTER)
    
    app.run()