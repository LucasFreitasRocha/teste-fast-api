

from sqlmodel import Session
from src.service.domain.app_domain import AppDomain
from src.data.entity.app_entity import AppEntity


class AppRepository:
    def __init__(self, engine):
        self.engine = engine  # engine, não uma conexão direta

    def create_app(self, app: AppDomain):
        app_entity = AppEntity(name=app.name, description=app.description)
        with Session(self.engine) as session:
            session.add(app_entity)
            session.commit()
            session.refresh(app_entity)
            # Retorne um domínio com o id do entity criado
            return AppDomain.build(app_entity.name, app_entity.description, app_entity.id)
    
    