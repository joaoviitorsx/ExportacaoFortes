import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

load_dotenv()

USER = os.getenv("USER_ICMS")
PASS = os.getenv("PASSWORD_ICMS")
HOST = os.getenv("HOST_ICMS")
PORT = os.getenv("PORT_ICMS", 3306)
NAME = os.getenv("DB_ICMS")

DATABASE_URL = f"mysql+pymysql://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"

engineICMS = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
SessionLocalICMS = sessionmaker(autocommit=False, autoflush=False, bind=engineICMS)

def getSessionICMS():
    return SessionLocalICMS()
