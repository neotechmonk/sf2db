from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

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

    def __enter__(self):
        self.engine = create_engine(self.db_uri)

        Base.metadata.create_all(bind=self.engine)
        
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
            try:
                if exc_type is None:
                    self.session.commit()
                else:
                    self.session.rollback()
            finally: # ?: overkill? already automatic behaviour?
                self.session.close()
                self.engine.dispose()
