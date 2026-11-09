from functools import lru_cache
from typing import Annotated, TypedDict
from fastapi import Depends, HTTPException, Query
from .config import Settings, get_settings
from .repository import OrderRepository
from .service import OrderService

SettingsDep = Annotated[Settings, Depends(get_settings)]


@lru_cache
def get_repository() -> OrderRepository:
    return OrderRepository()


def get_service(repository: Annotated[OrderRepository, Depends(get_repository)]) -> OrderService:
    return OrderService(repository)


ServiceDep = Annotated[OrderService, Depends(get_service)]


class Pagination(TypedDict):
    limit: int
    offset: int


def pagination_params(
    settings: SettingsDep,
    limit: Annotated[int | None, Query(ge=1, description="Размер страницы; по умолчанию DEFAULT_PAGE_SIZE")] = None,
    offset: Annotated[int | None, Query(ge=0, description="Смещение; по умолчанию DEFAULT_OFFSET")] = None,
) -> Pagination:
    actual_limit = settings.default_page_size if limit is None else limit
    if actual_limit > settings.max_page_size:
        raise HTTPException(status_code=422, detail=f"limit не должен превышать {settings.max_page_size}")
    return {"limit": actual_limit, "offset": settings.default_offset if offset is None else offset}


PaginationDep = Annotated[Pagination, Depends(pagination_params)]
