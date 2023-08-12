
from typing import Dict

from sf2db.mapping.models import ColumnMapping, TableMapping

MappingData = Dict[str, Dict[str, str]]

"""{
        "salesforce-object": "Account",
        "db-table": "User",
          "column-mapping": {
              "Id": "ID",
              "Name": "NAME"
              }
    }
"""


def mapping_factory(mapping: MappingData) -> TableMapping:
    salesforce_object = mapping.get("salesforce-object", "")
    db_table = mapping.get("db-table", "")

    column_mapping = mapping.get("column-mapping", {})
    field_mappings = [ColumnMapping(saleforce_field=key, db_column_name=value) for key, value in column_mapping.items()]

    table_mapping = TableMapping(salesforce_object_name=salesforce_object, db_table_name=db_table, col_mappings=field_mappings)
    
    return table_mapping


if __name__ == "__main__":
    import json
    from pprint import pprint

    json_string = """
    [
      {
          "salesforce-object":"Account",
          "db-table": "User",
          "column-mapping": {
              "Id": "ID",
              "Name": "NAME",
              "PersonEmail": "EMAIL",
              "IsDeleted": "ID_DELETED",
              "CreatedDate": "DATE_CREATED"
          }
      },
      {
          "salesforce-object":"Contact",
          "db-table": "PHONE",
          "column-mapping": {
              "Id": "ID",
              "Phone": "PHONE"
          }
      }
    ]
    """
    mapping_json = json.loads(json_string) 
    table_mappings :[TableMapping] =[]
    for mapping in mapping_json:
        table_mapping = mapping_factory(mapping)
        pprint(table_mapping)
        table_mappings.append(table_mapping)

    """ OUTPUT
        TableMapping(salesforce_object_name='Account', 
                db_table_name='User', 
                col_mappings=[
                    ColumnMapping(saleforce_field='Id', db_column_name='ID'),
                    ColumnMapping(saleforce_field='Name', db_column_name='NAME'),
                    ColumnMapping(saleforce_field='PersonEmail', db_column_name='EMAIL'),
                    ColumnMapping(saleforce_field='IsDeleted', db_column_name='ID_DELETED'),
                    ColumnMapping(saleforce_field='CreatedDate', db_column_name='DATE_CREATED'])
                    
        TableMapping(salesforce_object_name='Contact', 
                db_table_name='PHONE', 
                col_mappings=[
                    ColumnMapping(saleforce_field='Id', db_column_name='ID'),
                    ColumnMapping(saleforce_field='Phone', db_column_name='PHONE')])
    """