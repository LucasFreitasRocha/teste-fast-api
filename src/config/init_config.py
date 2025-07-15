from data.config.database import db
from data.repository.app_repository import AppRepository
from service.app_service import AppService



app_service = None

def init_config():
    db.create_tables()
    app_repository = AppRepository(db)
    app_service = AppService(app_repository)
    






def get_app_service(repository: AppRepository):
    global app_service
    if app_service is None:
        app_service = AppService(repository)
    return app_service
