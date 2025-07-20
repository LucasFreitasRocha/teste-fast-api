from src.data.entity.user_app_entity import UserAppEntity
from src.service.domain.user_app.user_app_domain import UserAppDomain
from sqlmodel import Session


class UserAppRepository:
    def __init__(self, engine):
        self.engine = engine

    def create_user_app(self, user_app: UserAppDomain):
        user_app_entity = UserAppEntity(
            user_id=user_app.user.id,
            app_id=user_app.app.id,
            password=user_app.password
        )
        with Session(self.engine) as session:
            session.add(user_app_entity)
            session.commit()
            session.refresh(user_app_entity)
            return user_app_entity.to_domain()
        
    def get_user_app(self, user_app_id: str):
        with Session(self.engine) as session:
            user_app_entity = session.get(UserAppEntity, user_app_id)
            return user_app_entity.to_domain() if user_app_entity else None
        
