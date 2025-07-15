import os
from typing import Optional
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.engine import Engine

load_dotenv()

class DatabaseConnection:
    _instance: Optional['DatabaseConnection'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'engine'):
            self.DB_HOST = os.getenv("DB_HOST", "localhost")
            self.DB_PORT = os.getenv("DB_PORT", "5433")
            self.DB_USER = os.getenv("DB_USER", "root")
            self.DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
            self.DB_NAME = os.getenv("DB_NAME", "fastapi_db")

            self.DATABASE_URL = (
                f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )

            self.engine = create_engine(
                self.DATABASE_URL,
                echo=True,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10
            )

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return Session(self.engine)
        
    def get_connection(self) -> Engine:
        return self.engine

db = DatabaseConnection() 