import inject
from fastapi import APIRouter
from src.service.app_service import AppService
from src.service.domain.app.app_request_domain import AppRequest


router = APIRouter()


@router.post("")
def create_app(app: AppRequest):
    app_service = inject.instance(AppService)
    return app_service.create_app(
        app_request=app
    )
