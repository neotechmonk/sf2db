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


class SalesforceAuthententicationError(Exception):
    """Raised when SalesforceAuthenticationFailed is raised of Salesforce.session_id is falsely."""
    pass

SalesforceQueryResult = Dict[str,Dict[str,Any]]

class SFInterface(Protocol):
    def login(self)-> None:
        ...
    
    def query(self, socl_query_str :str)->  List[SalesforceQueryResult]:
        ...