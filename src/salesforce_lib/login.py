from dataclasses import dataclass, field, fields
from typing import Dict

from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceAuthenticationFailed

from src.util.config import ConfigFiles
from src.util.file_reader import read_yaml


class ConfigValueError(Exception):
    """Raised when there is a problem instantiating SalesforceCredentials object."""
    pass

@dataclass
class SalesforceCredentials: 
    username:str
    password:str
    security_token:str
    consumer_key:str
    consumer_secret :str
    is_prod: bool = field(default=False, metadata={"exclude": True})

    @property
    def domain(self) -> str:
        return 'login' if self.is_prod else 'test'
    
    def __post_init__(self):
        for attr, value in self.__dict__.items():
            if value is None:
                raise ConfigValueError(f"Credential attribute '{attr}' should not be empty!")
      
    def asdict(self) -> dict:
        """Utility to get a dict of attributes that aren't excluded + properties."""
        _dict = {}

        # Adding non-excluded fields
        for field_info in fields(type(self)):
            if not (field_info.metadata and field_info.metadata.get("exclude")):
                _dict[field_info.name] = getattr(self, field_info.name)

        # Dynamically adding all properties
        for attr_name, attr_value in type(self).__dict__.items():
            if isinstance(attr_value, property):
                _dict[attr_name] = getattr(self, attr_name)

        return _dict

# Load Salesforce credentials from dict of credentials
def get_credentials(data : Dict[str, str]) -> SalesforceCredentials:
    try:
        credential = SalesforceCredentials(**data)
    except (TypeError, ValueError) as e:
        raise ConfigValueError(f"Issue creating  SalesforceCredentials object: {str(e)}")
    return credential


class AuthententicationFailedError(Exception):
    """Raised when SalesforceAuthenticationFailed is raised of Salesforce.session_id is falsely."""
    pass

def _login( credentials : SalesforceCredentials) -> Salesforce:
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

def login()-> Salesforce: 
    yaml_data=  read_yaml(ConfigFiles.CREDENTIALS)
    credential_data = get_credentials(yaml_data)
    return _login(credential_data)
    
    

# For diagnostics in production 
if __name__ == "__main__":
    sf :Salesforce  = login()
    print("Logged into Salesforce")

    for attr_name, attr_value in vars(sf).items():
        print(f"{attr_name} : {attr_value}")

