
import logging.config
from typing import Dict

from sf2db.app.config import Configs
from sf2db.util.json_reader import read_json
from sf2db.util.path import absolute


def load_logger(log_config_file:str, app_name : str) :
    
    config = read_json(log_config_file)
    logging.config.dictConfig(config)

    return logging.getLogger(app_name)

def logger():
    LOG_CONFIG_FILE = absolute(__file__, "../../"+Configs.LOGGER_CONFIG)
    print(LOG_CONFIG_FILE)

    logger = load_logger(log_config_file= LOG_CONFIG_FILE, app_name=Configs.LOGGER_APP_NAME)
   
    return logger

