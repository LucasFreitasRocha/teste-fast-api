from src.data.config.database import db
from src.data.repository.app_repository import AppRepository
from src.service.app_service import AppService



app_repository = AppRepository(db.engine)
app_service = AppService(app_repository)

def init_config():
    db.create_tables()
