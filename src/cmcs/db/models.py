from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import declarative_base

Base = declarative_base()


def to_dict(obj: Base) -> dict[str, Any]:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class DBTable(Base):
    """Inherited to create DBTable classes of specific types dynaically """
    __abstract__ = True # to avoid creation of objects directly
    __tablename__ = ""
    

# Example usage
# if __name__ == "__main__":
    
#     from sqlalchemy import Column, Integer, String
    
#     class DBCustomer(DBTable):
#         __tablename__ = "customer"
#         id = Column(Integer, primary_key=True, autoincrement=True)
#         first_name = Column(String(250), nullable=False)
#         last_name = Column(String(250), nullable=False)
#         email_address = Column(String(250), nullable=False)
    
#     dbcustomer = DBCustomer(id = 232,first_name="John", last_name="Doe", email_address="doe@example.com")

#     print (to_dict(dbcustomer))