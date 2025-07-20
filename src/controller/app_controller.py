import inject
from fastapi import APIRouter, status, Response
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
    

@router.get("/{app_id}", response_model=AppDomain, response_model_exclude_none=True)
def get_app(app_id: str):
    app_service = inject.instance(AppService)
    return app_service.get_app(app_id=app_id)


@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_app(app_id: str):
    app_service = inject.instance(AppService)
    app_service.delete_app(app_id=app_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)