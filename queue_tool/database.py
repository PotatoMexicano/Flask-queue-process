from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool


class Base(DeclarativeBase):
    pass

__engine = create_engine(
    URL.create(
        database='queue-tool',
        drivername='postgresql',
        host='localhost',
        port=5432,
        username='postgres',
        password='root'
    ),
    echo=False,
    poolclass=QueuePool,
    pool_pre_ping=True,
    pool_recycle=120
)

Session = scoped_session(sessionmaker(__engine))

def create_db():
    Base.metadata.create_all(__engine)
