from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from decouple import config

class Base(DeclarativeBase):
    pass

__engine = create_engine(
    URL.create(
        drivername='postgresql',
        host=config('DB_HOST'),
        port=config('DB_PORT'),
        database=config('DATABASE'),
        username=config('DB_USER'),
        password=config('DB_PASSWD'),
    ),
    echo=False,
    poolclass=QueuePool,
    pool_pre_ping=True,
    pool_recycle=120
)

Session = scoped_session(sessionmaker(__engine))

def create_db():
    Base.metadata.create_all(__engine)
