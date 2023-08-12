import json
import re

from simple_salesforce import Salesforce
from sqlalchemy import (Column, Integer, MetaData, PrimaryKeyConstraint,
                        String, Table, create_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

from sf2db.salesforce_lib.login import login

sf : Salesforce = login()

# Load object-to-table mappings from object_mappings.json
with open('./config/object_mappings.json', 'r') as file:
    object_mappings = json.load(file)["object_mappings"]

# Define SQLAlchemy connection and session
engine = create_engine('sqlite:///database.db', pool_size=20)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Map SQL Server data types to SQLAlchemy data types
sql_to_sqlalchemy_types = {
    "nvarchar": String,
    "integer": Integer,
}
# Loop through the object mappings and fetch data from Salesforce
for obj_mapping in object_mappings:
    salesforce_object = obj_mapping["salesforce_object"]
    sql_table = obj_mapping["sql_table"]
    primary_key = obj_mapping["primary_key"]  # Get the primary key from the object mapping
    column_mappings = obj_mapping["column_mappings"]

    # Dynamically create the table for the Salesforce object
    metadata = MetaData()
    table_columns = []


    # Extract column names from column_mappings
    columns = [field for field, column_mapping in column_mappings.items()]

    # Build the SELECT query dynamically with the columns
    select_query = f"SELECT {', '.join(columns)} FROM {salesforce_object}"

    for field, column_mapping in column_mappings.items():
        # Extract base type and length from the data_type value
        data_type = column_mapping.get("data_type", "nvarchar(255)")
        base_type, length = re.match(r"([a-z]+)(?:\((\d+)\))?", data_type, re.I).groups()
        length = int(length) if length else None

        # Create the column based on the data type
        if base_type in sql_to_sqlalchemy_types:
            column_type = sql_to_sqlalchemy_types[base_type]
            if length:
                table_columns.append(Column(column_mapping.get("sql_column", field), column_type(length)))
            else:
                table_columns.append(Column(column_mapping.get("sql_column", field), column_type))
        else:
            raise ValueError(f"Unknown data type: {base_type}")

    # Find the primary key column
    primary_key_column = None
    for col in table_columns:
        if col.name == primary_key:
            primary_key_column = col
            break

    if primary_key_column is None:
        raise ValueError(f"Primary key '{primary_key}' not found in column mappings.")

    # Add a PrimaryKeyConstraint for the primary key column
    table_columns.append(PrimaryKeyConstraint(primary_key_column))

    # Dynamically create the table and CustomModel for the Salesforce object
    table = Table(sql_table, metadata, *table_columns)

    # Dynamically create the table and CustomModel for the Salesforce object
  
    # Check if the table already exists in the metadata
    if sql_table in metadata.tables:
        # If it exists, use extend_existing=True to redefine the table with new columns
        table = Table(sql_table, metadata, extend_existing=True, *table_columns)
    else:
        # If it doesn't exist, create a new table
        table = Table(sql_table, metadata, *table_columns)

    # Define a custom model for each Salesforce object
    class CustomModel(Base):
        __table__ = table

    # Query data from Salesforce object

    # metadata.create_all(bind=engine)
    query_result = sf.query(select_query)
    

    for record in query_result['records']:
        # Filter out the 'attributes' key from the record dictionary
        filtered_record = {field: value for field, value in record.items() if field != 'attributes'}

        # Map Salesforce field names to SQL Server column names and handle data type conversions
        data = {}
        for field, value in filtered_record.items():
            column_mapping = column_mappings.get(field, {})
            sql_column = column_mapping.get("sql_column", field)

            # Add the column and value to the data dictionary
            data[sql_column] = value

    # Insert data into the SQL Server table using SQLAlchemy
    if data:
        stmt = table.insert().values(**data)        
        session.execute(stmt)
        data = None # reset incase there future tables with no records

# Commit the changes and close the session
session.commit()
session.close()
