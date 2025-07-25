from src.data.entity.user_app_entity import UserAppEntity
from src.service.domain.user_app.user_app_domain import UserAppDomain
from sqlmodel import Session, select


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

    def get_user_app_by_user_id_and_app_id(self, user_id: str, app_id: str):
        with Session(self.engine) as session:
            user_app_entity = session.exec(
                select(UserAppEntity).where(
                    UserAppEntity.user_id == user_id, UserAppEntity.app_id == app_id
                )
            ).first()
            return user_app_entity.to_domain() if user_app_entity else None
