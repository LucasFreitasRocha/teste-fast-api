

from sqlmodel import Session
from src.data.entity.company_entity import CompanyEntity
from src.service.domain.company_domain import CompanyDomain


class CompanyRepository:
    def __init__(self, engine):
        self.engine = engine

    def create_company(self, company: CompanyDomain):
        company_entity = CompanyEntity(name=company.name, description=company.description, document=company.document)
        with Session(self.engine) as session:
            session.add(company_entity)
            session.commit()
            session.refresh(company_entity)
            return company_entity.to_domain()
        
    def get_company_by_id(self, company_id: int):
        with Session(self.engine) as session:
            company_entity = session.get(CompanyEntity, company_id)
            return company_entity.to_domain() if company_entity else None   
        
        
        
        