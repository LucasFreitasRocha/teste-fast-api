import inject
from fastapi import APIRouter, status
from src.service.app_service import AppService
from src.service.domain.app.app_domain import AppDomain
from src.service.domain.app.app_request_domain import AppRequest


router = APIRouter()


@router.post("", response_model=AppDomain, status_code=status.HTTP_201_CREATED, response_model_exclude_none=True)
def create_app(app: AppRequest):
    app_service = inject.instance(AppService)
    return app_service.create_app(
        app_request=app
    )
