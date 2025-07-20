from fastapi import HTTPException
from src.data.repository.user_repository import UserRepository
from src.service.domain.user.user_domain import UserDomain


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: UserDomain):
        return self.repository.create_user(user)
    
    def get_user(self, user_id: str):
        user = self.repository.get_user(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found with this id: " + user_id)
        return user
    def get_user_by_email(self, email: str):
        return self.repository.get_user_by_email(email)
        
    
    def delete_user(self, user_id: str):
        user = self.get_user(user_id)
        self.repository.delete_user(user)