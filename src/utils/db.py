from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utils.settings import settings

Base = declarative_base()

def create_database():
    db_url = settings.DB_CONNECTION
    db_name = db_url.split("/")[-1]

    server_url = db_url.rsplit("/", 1)[0] + "/"

    server_engine = create_engine(server_url)

    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))

create_database()

engine = create_engine(settings.DB_CONNECTION)

LocalSession = sessionmaker(bind=engine)

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()
