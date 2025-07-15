

from src.data.repository.app_repository import AppRepository
from src.service.domain.app_domain import AppDomain


class AppService:
    def __init__(self, repository: AppRepository):
        self.repository = repository

    def create_app(self, name: str, description: str):
        app = AppDomain.build(name, description)
        return self.repository.create_app(app)
    
    