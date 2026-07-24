
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    """
    FastAPI dependency. Opens a DB session for one request and
    always closes it afterwards, even if something goes wrong.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
