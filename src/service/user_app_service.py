from fastapi import HTTPException
from src.data.repository.user_app_repository import UserAppRepository
from src.service.domain.user_app.user_app_request import UserAppRequest
from src.service.user_service import UserService
from src.service.app_service import AppService
from src.service.domain.user_app.user_app_domain import UserAppDomain
from src.service.domain.user.user_domain import UserDomain


class UserAppService:
    def __init__(
        self,
        repository: UserAppRepository,
        user_service: UserService,
        app_service: AppService,
    ):
        self.repository = repository
        self.user_service = user_service
        self.app_service = app_service

    def create_user_app(self, user_app: UserAppRequest):
        user = self.user_service.get_user_by_email(user_app.email)
        if user is not None:
            self.searchInApp(user.user_id, user_app.app_id)
        else:
          user = self.user_service.create_user(UserDomain.build(name=user_app.name, email=user_app.email, phone=user_app.phone))
        app = self.app_service.get_app(user_app.app_id)
        return self.repository.create_user_app(
            UserAppDomain.build(user, app, user_app.password)
        )

    def searchInApp(self, user_id: str, app_id: str):
        user_app = self.repository.get_user_app(user_id, app_id)
        if user_app is not None:
            raise HTTPException(
                status_code=400, detail="User already exists in this app"
            )
