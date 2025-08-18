from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()


class Config:
    # Database config
    USER = os.getenv("user")
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Como USER, PASSWORD, etc. no están en el scope global, usamos Config atributos explícitamente:
Config.SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{Config.USER}:{Config.PASSWORD}@{Config.HOST}:{Config.PORT}/{Config.DBNAME}?sslmode=require"

# Create the SQLAlchemy engine (optional if you're using Flask SQLAlchemy)
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)


try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")
