from dataclasses import dataclass, field

import yaml
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceAuthenticationFailed

CONFIG_FILE :str = './config/login.yaml'

# Custom errors
class ConfigFileNotFoundError(Exception):
    """Raised when the configuration file is not found."""
    pass

class ConfigParseError(Exception):
    """Raised when there's an error parsing the configuration file."""
    pass

class ConfigValueError(Exception):
    """Raised when there's an error parsing the configuration file."""
    pass

class AuthententicationFailedError(Exception):
    """Raised when SalesforceAuthenticationFailed is raised of Salesforce.session_id is falsely."""
    pass

@dataclass
class SalesforceConfig: 
    username:str
    password:str
    security_token:str
    consumer_key:str
    consumer_secret :str
    is_prod: bool = field(default=False)

    @property
    def domain(self) -> str:
        return 'login' if self.is_prod else 'test'
    
    def __post_init__(self):
        for attr, value in self.__dict__.items():
            if value is None:
                raise ConfigValueError(f"credential attribute '{attr}' should not be empty!")

# Load Salesforce credentials from login.yaml
def read_config(file: str = CONFIG_FILE) -> SalesforceConfig:
    try:
        with open(file, 'r') as f:
            credentials = yaml.safe_load(f)
        return SalesforceConfig(**credentials)
    except FileNotFoundError:
        raise ConfigFileNotFoundError(f"The configuration file {file} was not found.")
    except yaml.YAMLError as e:
        raise ConfigParseError(f"Error parsing the YAML file: {str(e)}")

def login( credentials : SalesforceConfig) -> Salesforce:
    try:
        sf =   Salesforce(
            username=credentials.username,
            password=credentials.password,
            security_token=credentials.security_token,
            consumer_key=credentials.consumer_key,
            consumer_secret=credentials.consumer_secret,
            domain=credentials.domain)

        if not sf.session_id: 
            raise AuthententicationFailedError("Authentication failed: No session id returned")

        return sf
    except SalesforceAuthenticationFailed as e:
        raise AuthententicationFailedError(f"Authentication failed: {str(e)}")


# For diagnostics in production 
if __name__ == "__main__":
    credentials : SalesforceConfig  = read_config(CONFIG_FILE)
    sf :Salesforce  = login(credentials)
    print("Logged into Salesforce")

    for attr_name, attr_value in vars(sf).items():
        print(f"{attr_name} : {attr_value}")

