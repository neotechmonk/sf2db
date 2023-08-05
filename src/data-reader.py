from simple_salesforce import Salesforce
from sqlalchemy import (Column, Integer, MetaData, PrimaryKeyConstraint,
                        String, Table, create_engine, select)
from sqlalchemy.orm import declarative_base, sessionmaker

# Define SQLAlchemy connection and session
engine = create_engine('sqlite:///database.db', pool_size=20)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the SQLAlchemy model for the accounts_table
class Account(Base):
    __tablename__ = 'accounts_table'
    Id = Column(String(100), primary_key=True)
    LastName = Column(String(100))
    Industry = Column(String(50))
    City = Column(String(100))

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# Now you can use a select statement to query data from the accounts_table
stmt = select(Account)
result = session.execute(stmt).fetchall()
session.commit()
# Print the results
for row in result:
     # Access individual columns of each row
    print(f"Id: {row.Id}, AccountName: {row.LastName}, IndustryType: {row.IndustryType}, City: {row.City}")
