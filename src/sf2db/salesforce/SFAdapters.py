from typing import Dict, List

from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceAuthenticationFailed

from sf2db.salesforce.SFInterface import (SalesforceCredentialConfigValueError,
                                          SalesforceCredentials,
                                          SalesforceFetchError,
                                          SalesforceLoginError,
                                          SalesforceQueryResult)


def get_credentials(data : Dict[str, str]) -> SalesforceCredentials:
    try:
        credential = SalesforceCredentials(**data)
    except (TypeError, ValueError) as e:
        raise SalesforceCredentialConfigValueError(f"Issue creating  SalesforceCredentials object: {str(e)}")
    return credential

class SimpleSalesforceAdapter:

    def __init__(self, credential_data: Dict[str, str]):
        self.connection = None
        self.credentials = get_credentials(credential_data)

    def login(self) -> None:
        try:
            sf =   Salesforce(
                username=self.credentials.username,
                password=self.credentials.password,
                security_token=self.credentials.security_token,
                consumer_key=self.credentials.consumer_key,
                consumer_secret=self.credentials.consumer_secret,
                domain=self.credentials.domain)

            if not sf.session_id: 
                raise SalesforceLoginError("Authentication failed: No session id returned")

            self.connection =  sf
        except SalesforceAuthenticationFailed as e:
            raise SalesforceLoginError(f"Authentication failed: {str(e)}")

    def query(self, socl_query_str: str) ->List[SalesforceQueryResult]:
        if not self.connection:
            raise SalesforceLoginError("You need to login before querying")
        try : 
            response = self.connection.query_all(query=socl_query_str)
        except SalesforceFetchError as e:
            raise SalesforceFetchError(f"Error fetching data from salesforce using SOQL query")
        records = response.get("records", [])

        # Filter out the 'attributes' key from each record
        # `attributes` key describes the ObjectName
        filtered_response = [
            {field: value for field, value in record.items() if field != 'attributes'}
            for record in records
            ]
        
        return filtered_response
    
    

        {field: value for field, value in record.items() if field != 'attributes'}