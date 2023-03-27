''' The database connection '''
__name__      = "database.py"
__author__    = "COUTAND Bastien"
__date__      = "20.10.22"


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config


DATABASE_IP   = config('DATABASE_IP')
DATABASE_PORT = config('DATABASE_PORT')
DATABASE_NAME = config('DATABASE_NAME')

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://app:app@{DATABASE_IP}:{DATABASE_PORT}/{DATABASE_NAME}"

engine       = create_engine(url=SQLALCHEMY_DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()