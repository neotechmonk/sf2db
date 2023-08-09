from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from cmcs.util.config import ConfigFiles

from .models import Base


class DBSession:
    def __init__(self, db_uri):
        """
        `connection_string` examples for differen physical DBs
            'sqlite:///example.db'
            'mysql+pymysql://username:password@localhost/db_name'
            'postgresql://username:password@localhost/db_name'
            'mssql+pyodbc://username:password@server_name/db_name?driver=SQL+Server'
        """
        self.db_uri = db_uri
        self.engine = None
        self.session = None

    def __enter__(self):
        self.engine = create_engine(self.db_uri)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.commit()
        self.session.close()
        self.engine.dispose()



###
### SAMPLE Table creation 
###
# Base = declarative_base()

# Define the User class representing the 'users' table
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     email = Column(String(100))

# def create_users_table(db_uri):
#     # Create the engine
#     engine = create_engine(db_uri)

#     # Create all tables defined in the metadata, including 'users'
#     Base.metadata.create_all(bind  = engine)


    # Usage example with context manager
# if __name__ == '__main__':
#     DB_URI = ConfigFiles.DB_URI
#     create_users_table(DB_URI)
    
#     with DBSession(DB_URI) as session:
        
#         new_user = User(name='John Doe', email='john@example.com')
#         session.add(new_user)
#         # session.commit()

#         user = session.query(User).filter_by(name='John Doe').first()
#         # session.commit()
#         print(f"{user.id}, {user.email}, {user.email}")



