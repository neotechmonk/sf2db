import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from dateutil import parser


def convert_datetime(func):
    """ 
    Utility function to convert SF Date Time to Datetime compatible with SQL Alchemy
    
    Only operations on Param, `sf_data`
    """
    datetime_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{4}$')
    
    def wrapper(sf_data, *args, **kwargs):
        converted_data = {
            key: parser.parse(value).replace(tzinfo=timezone.utc)
                   if isinstance(value, str) and datetime_pattern.match(value)
                   else value
            for key, value in sf_data.items()
        }
        return func(converted_data, *args, **kwargs)
    return wrapper

@convert_datetime
def convert(sf_data: Dict[str, str], 
            salesforce_fields: List[str], 
            db_columns: List[str]) -> Dict[str, Any]:
    coverted_data =   {db_column: sf_data.get(sf_field) for sf_field, db_column in zip(salesforce_fields, db_columns)}
    # print(coverted_data)
    return coverted_data





# Example usage
# if __name__ == '__main__':
#     sf_data = {
#         'Id': '0019j000008WrENAA0',
#         'Name': 'Sauce',
#         'PersonEmail': None,
#         'IsDeleted': False,
#         'CreatedDate': '2023-07-11T09:08:46.000+0000'
#     }

#     salesforce_fields = ['Id', 'Name', 'PersonEmail', 'IsDeleted', 'CreatedDate']
#     db_columns = ['ID', 'PRODUCT_NAME', 'EMAIL', 'IS_DELETED', 'DATE_CREATED']

#     converted_result = convert(sf_data, salesforce_fields, db_columns)
#     print (f"Before conversion \n",
#            f"{sf_data}",
#            f"\n -----------------")
    
#     print (f"After conversion \n",
#            f"{converted_result}",
#            f"\n -----------------")
    