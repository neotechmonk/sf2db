from sqlite3 import IntegrityError

from sqlalchemy.engine import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from .models import Base


class DatabaseInitializationError(Exception):
    """Raised when isssues are encountered with creating DB Engine or creating a session ."""
    pass
class DatabaseOperationError(Exception):
    """Raised when isssues are encountered committing or rolling back the transaction ."""
    pass
class DuplicateRecordError(Exception):
    """Raised when duplicate records are encountered during transaction commit or rollback."""
    pass

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

    def __enter__(self):
        try : 
            self.engine = create_engine(self.db_uri)

            Base.metadata.create_all(bind=self.engine)
            
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            return self.session
        
        except (SQLAlchemyError, TimeoutError) as e:
            raise DatabaseInitializationError(f"An error occurred while initializing the database and creating a session object: {e}")
        except Exception as e:
            raise DatabaseInitializationError(f"An unexpected error occurred when initialising the  database  : {e}")

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is None:
                try: 
                    self.session.commit()
                except IntegrityError as e:  
                    raise DuplicateRecordError("Error inserting records. Record wit primary key already exists", e)      
            else:
                self.session.rollback()
       
        except SQLAlchemyError as e:
            raise DatabaseOperationError("An error occurred during database operation", e)
        finally:
            self.session.close()
            self.engine.dispose()