
from sf2db import app
from sf2db.app.app import App
from sf2db.app.config import Configs
from sf2db.salesforce import SFAdapters
from sf2db.util.logging import logger
from sf2db.util.path import absolute

if __name__ == "__main__":
    log = logger()
    log.info("Starting app")  
    
    this_file_path  = __file__

    # LOGGER_CONFIG_PATH = absolute (this_file_path, Configs.LOGGER_CONFIG)

    # log = load_logger(log_config_file=LOGGER_CONFIG_PATH, app_name=Configs.LOGGER_APP_NAME)

  
    # log.debug("Loaded logger; Loading other config")                        
    SF_CREDENTIALS_PATH = absolute (this_file_path, Configs.SALESFORCE_CREDENTIALS)
    SF2DB_MAPPINGS_PATH = absolute (this_file_path, Configs.SF2DB_MAPPINGS)
    DB_TABLE_DEFINITIONS_PATH = absolute (this_file_path, Configs.DB_TABLES)
    DB_CONFIG_PATH = absolute (this_file_path, Configs.DB_COFIG)
    SALESFORCE_CLIENT_ADAPTER = SFAdapters.SimpleSalesforceAdapter
   
    log.debug("Instantiating src.sf2db.app.App")  

    app = App(path_db_table_def=DB_TABLE_DEFINITIONS_PATH, 
              path_db_uri=DB_CONFIG_PATH, 
              path_sf_credentials=SF_CREDENTIALS_PATH, 
              path_sf2db_mappings=SF2DB_MAPPINGS_PATH,
              salesforce_client_adapter=SALESFORCE_CLIENT_ADAPTER)
    
    app.run()

    log.info("Stopping app")  