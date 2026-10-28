from app.schemas.company import CompanySearchResponse
from app.services.company_resolver import resolver, CompanyResolver, COMPANY_DATABASE


def search_companies(query: str) -> CompanySearchResponse:
    """
    Search and resolve companies deterministically using CompanyResolver.
    """
    return resolver.resolve(query)


__all__ = ["search_companies", "resolver", "CompanyResolver", "COMPANY_DATABASE"]
