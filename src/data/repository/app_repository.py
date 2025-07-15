

from service.domain.app_domain import AppDomain
from data.entity.app_entity import AppEntity


class AppRepository:
    def __init__(self, db):
        self.db = db
        
    def create_app(self, app: AppDomain):
        app_entity = AppEntity(name=app.name, description=app.description)
        self.db.add(app_entity)
        self.db.commit()
        self.db.refresh(app)
        return app.build(app.name, app.description, app.id)
    
    