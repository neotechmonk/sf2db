from typing import List, Optional, Tuple


def build_soql_query(object_name: str,
                     columns: List[str] = ["*"],
                     where_clauses: Optional[List[Tuple[str, str, str]]] = None,
                     order_by: Optional[Tuple[str, str]] = None,
                     limit: int = 100) -> str:
    """
    Constructs a generic SELECT SOQL query.
    
    Parameters:
    - object_name (str): The API name of the Salesforce object.
    - columns (List[str]): The columns you want to fetch. Defaults to all (*).
    - where_clauses (Optional[List[Tuple[str, str, str]]]): A list of where clause conditions. Each condition is a tuple of (column, operator, value).
    - order_by (Optional[Tuple[str, str]]): A tuple specifying order by column and direction.
    - limit (int): The maximum number of records to fetch. Default is 100.
    
    Returns:
    - str: The constructed SOQL query string.
    """
    
    # Building SELECT clause
    select_clause = ", ".join(columns)
    
    # Building WHERE clause
    where_clause = ""
    if where_clauses:
        conditions = [f"{column} {operator} '{value}'" for column, operator, value in where_clauses]
        where_clause = f"WHERE {' AND '.join(conditions)} "
    
    # Building ORDER BY clause
    order_by_clause = ""
    if order_by:
        column, direction = order_by
        order_by_clause = f"ORDER BY {column} {direction} "
    
    # Constructing final SOQL query
    soql_query = (f"SELECT {select_clause} FROM {object_name} "
                  f"{where_clause}"
                  f"{order_by_clause}"
                  f"LIMIT {limit}")
    
    return soql_query

# Usage Example
if __name__ == "__main__":
    query = build_soql_query("Account", 
                         columns=["Id", "Name"], 
                         where_clauses=[("LastModifiedDate", ">=", "2023-01-01T00:00:00Z")], 
                         order_by=("LastModifiedDate", "DESC"), 
                         limit=50)
    print(query)
