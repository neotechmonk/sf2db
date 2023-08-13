"""
    1. Login to SF
    1. Query Sf
"""

from dataclasses import dataclass, field, fields
from typing import Any, Dict, List, Protocol


class SalesforceCredentialConfigValueError(Exception):
    """Raised when there is a problem instantiating SalesforceCredentials object."""
    pass




@dataclass
class SalesforceCredentials: 
    username:str
    password:str
    security_token:str
    consumer_key:str
    consumer_secret :str
    domain: str = field(default="login")


class SalesforceLoginError(Exception):
    """Raised when SalesforceAuthenticationFailed is raised of Salesforce.session_id is falsely."""
    pass

class SalesforceFetchError(Exception):
    """
    Raised when there is an issue fetching data from Salesforce.
    """
    pass

SalesforceQueryResult = Dict[str,Dict[str,Any]]

class SFInterface(Protocol):
    """
    Represents an interface for interacting with Salesforce.
    Other Adapters must conform to this interface
    """

    def login(self) -> None:
        """
        Authenticate with Salesforce.
        This method should handle the authentication process with Salesforce.
        
        Raises:
            SalesforceLoginError: If there is an issue during the login process.
        """
        ...

    def query(self, socl_query_str: str) -> List[SalesforceQueryResult]:
        """
        Execute a SOQL query on Salesforce.
        
        Args:
            socl_query_str (str): The SOQL query string to execute.
            
        Returns:
            List[SalesforceQueryResult]: A list of query results.
            
        Raises:
            SalesforceFetchError: If there is an issue fetching data from Salesforce.
        """
        ...