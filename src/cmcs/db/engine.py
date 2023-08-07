from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# from .models import Base
Base = declarative_base()

engine: Engine | None = None
session = sessionmaker()


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
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(engine)
        # self.Session = sessionmaker(bind=self.engine)

    def __enter__(self):
        self.session = self.Session()
        self.session.bind = self.engine
        # self.session = sessionmaker(bind=self.engine)
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

# Usage example with context manager
if __name__ == '__main__':
    from sqlalchemy import Column, Integer, MetaData, String

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))
        email = Column(String(100))



    def create_table_if_not_exists(engine, table):
        metadata = MetaData()
        metadata.bind = engine
        metadata.reflect(bind=engine)
        if not engine.dialect.has_table(engine, table.__tablename__):
            Base.metadata.create_all(bind=engine, tables=[table.__table__])


    with DBSession('sqlite:///example.db') as session:
        create_table_if_not_exists(session.get_bind(), User)
        new_user = User(name='John Doe', email='john@example.com')
        session.add(new_user)
        # session.commit()

        # user = session.query(User).filter_by(name='John Doe').first()
        # print(user.email)



