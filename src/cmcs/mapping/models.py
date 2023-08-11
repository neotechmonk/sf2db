
from typing import Any, Dict, List

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated


class NoStringAttributeValidationError(Exception):
    """Raised when new table is attempted to be created while there is already one in existence."""
    pass

class EmptyListValidationError(Exception):
    """Raised when new table is attempted to be created while there is already one in existence."""
    pass

def string_attribute_validator(name: Any) -> str:
    if not all([isinstance(name, str), name is not None, name != ""]):
        raise NoStringAttributeValidationError(f"Field must be a non-empty string. Value provided => {name if name else '<empty>'}")
    return name

def list_of_columns_validator(cols :List[Any]) -> str:
    if not cols:
        raise EmptyListValidationError(f"At least one field to column mapping must be specified")
    return cols


String_Attr = Annotated[Any, AfterValidator(string_attribute_validator)]

class ColumnMapping(BaseModel):
    saleforce_field: String_Attr
    db_column_name: String_Attr


class TableMapping(BaseModel):
    salesforce_object_name: String_Attr
    db_table_name: String_Attr
    col_mappings: Annotated[List[ColumnMapping], AfterValidator(list_of_columns_validator)]


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