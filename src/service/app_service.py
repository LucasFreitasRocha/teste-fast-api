from fastapi import HTTPException
from src.data.repository.app_repository import AppRepository
from src.service.company_service import CompanyService
from src.service.domain.app.app_domain import AppDomain
from src.service.domain.app.app_request_domain import AppRequest


class AppService:
    def __init__(self, repository: AppRepository, company_service: CompanyService):
        self.repository = repository
        self.company_service = company_service

    def create_app(self, app_request: AppRequest):
        company = self.company_service.get_company_by_id(app_request.company_id)
        app = AppDomain.build(name= app_request.name, description= app_request.description, 
                              company= company)
        return self.repository.create_app(app)
    
    def get_app(self, app_id: str):
        app = self.repository.get_app(app_id)
        if app is None:
            raise HTTPException(status_code=404, detail="App not found with this id: " + app_id)
        return app
    
    def delete_app(self, app_id: str):
        app = self.get_app(app_id)
        self.repository.delete_app(app_id)