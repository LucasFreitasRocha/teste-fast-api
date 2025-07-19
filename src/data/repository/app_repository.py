from sqlmodel import Session
from src.data.entity.app_entity import AppEntity
from src.service.domain.app.app_domain import AppDomain



class AppRepository:
    def __init__(self, engine):
        self.engine = engine  # engine, não uma conexão direta

    def create_app(self, app: AppDomain):
        if app.company is None or app.company.id is None:
            raise ValueError("Empresa não informada ou sem ID")
        app_entity = AppEntity(
            name=app.name,
            description=app.description,
            company_id=app.company.id,
        )
        with Session(self.engine) as session:
            session.add(app_entity)
            session.commit()
            session.refresh(app_entity)
            return AppDomain.build(
                app_entity.name,
                app_entity.description,
                app_entity.company.to_domain(),
                app_entity.id,
            )
