

from typing import Any, List

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated


# Custom validation errors
class NoStringAttributeValidationError(Exception):
    """Raised when new table is attempted to be created while there is already one in existence."""
    pass

class EmptyListValidationError(Exception):
    """Raised when new table is attempted to be created while there is already one in existence."""
    pass

# Validation helpers
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

ColMap_List = Annotated[List[ColumnMapping], AfterValidator(list_of_columns_validator)]

class TableMapping(BaseModel):
    salesforce_object_name: String_Attr
    db_table_name: String_Attr
    col_mappings: ColMap_List

