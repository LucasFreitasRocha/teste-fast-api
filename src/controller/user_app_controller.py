import inject
from fastapi import APIRouter, status
from src.service.user_app_service import UserAppService
from src.service.domain.user_app.user_app_request import UserAppRequest
from src.service.domain.user_app.user_app_domain import UserAppDomain

router = APIRouter()


@router.post("", response_model=UserAppDomain, status_code=status.HTTP_201_CREATED, response_model_exclude_none=True)
def create_user_app(user_app: UserAppRequest):
    user_app_service = inject.instance(UserAppService)
    return user_app_service.create_user_app(user_app, False)


