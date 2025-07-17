

from src.service.domain.company_domain import CompanyDomain


class CompanyValidator:
    def validate_company(self, company: CompanyDomain):
        if not company.name:
            raise ValueError("Company name is required")
        if not company.description:
            raise ValueError("Company description is required")
        if not company.document:
            raise ValueError("Company document is required")
        return company