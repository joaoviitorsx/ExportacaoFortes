import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

load_dotenv()

USER = os.getenv("USER_FS")
PASS = os.getenv("PASSWORD_FS")
HOST = os.getenv("HOST_FS")
PORT = os.getenv("PORT_FS", 3306)
NAME = os.getenv("DB_FS")

DATABASE_URL = f"mysql+pymysql://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"

engineFS = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
SessionLocalFS = sessionmaker(autocommit=False, autoflush=False, bind=engineFS)

def getSessionFS():
    return SessionLocalFS()
