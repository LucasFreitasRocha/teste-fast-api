from src.data.config.database import db


def init_config():
    db.create_tables()
    
