import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

# Carregar .env do executável PyInstaller ou do ambiente de desenvolvimento
if getattr(sys, 'frozen', False):
    # Executável PyInstaller - buscar no diretório temporário extraído
    base_path = sys._MEIPASS
    env_path = os.path.join(base_path, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()  # Fallback
else:
    # Desenvolvimento
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
