from sqlalchemy import create_engine, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # engine is used to connect to database

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    ) # a session needs to be created 

Base = declarative_base()

def get_db():
    db = SessionLocal()     # creates a session to connect to the database
    try:
        yield db
    finally:
        db.close()          # closes connection when done