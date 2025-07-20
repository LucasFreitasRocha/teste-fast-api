from src.data.entity.user_entity import UserEntity
from src.service.domain.user.user_domain import UserDomain
from sqlmodel import Session, select


class UserRepository:
    def __init__(self, engine):
        self.engine = engine

    def create_user(self, user: UserDomain):
        user_entity = UserEntity(
            name=user.name,
            email=user.email,
            phone=user.phone
        )
        with Session(self.engine) as session:
            session.add(user_entity)
            session.commit()
            session.refresh(user_entity)
            return user_entity.to_domain()
        
    def get_user(self, user_id: str):
        with Session(self.engine) as session:
            user = session.get(UserEntity, user_id)
            return user.to_domain() if user else None
        
    def get_user_by_email(self, email: str):
        with Session(self.engine) as session:
            user = session.exec(select(UserEntity).where(UserEntity.email == email)).first()
            return user.to_domain() if user else None
        
    def delete_user(self, user: UserDomain):
        with Session(self.engine) as session:
            session.delete(user)
            session.commit()
    