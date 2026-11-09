from typing import Annotated
from fastapi import APIRouter, Query, Response, status
from ..dependencies import PaginationDep, ServiceDep
from ..schemas import Order, OrderCreate, OrderStatus, OrderUpdate
from ..service import SortBy

router = APIRouter(prefix="/orders", tags=["Заказы"])
NOT_FOUND = {404: {"description": "Заказ не найден"}}
EDIT_ERRORS = {**NOT_FOUND, 409: {"description": "Заказ уже выполнен"}}


@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED, summary="Создать заказ")
async def create_order(data: OrderCreate, service: ServiceDep) -> Order:
    return service.create_order(data)


@router.get("", response_model=list[Order], summary="Получить список заказов")
async def list_orders(
    service: ServiceDep,
    pagination: PaginationDep,
    status: Annotated[OrderStatus | None, Query(description="Фильтр по статусу")] = None,
    sort_by: Annotated[SortBy, Query(description="Поле сортировки по возрастанию")] = "created_at",
) -> list[Order]:
    return service.list_orders(status=status, sort_by=sort_by, **pagination)


@router.get("/{order_id}", response_model=Order, summary="Получить заказ по идентификатору", responses=NOT_FOUND)
async def get_order(order_id: int, service: ServiceDep) -> Order:
    return service.get_order(order_id)


@router.patch("/{order_id}", response_model=Order, summary="Частично обновить заказ", responses=EDIT_ERRORS)
async def update_order(order_id: int, data: OrderUpdate, service: ServiceDep) -> Order:
    return service.update_order(order_id, data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
               summary="Отменить заказ", responses=EDIT_ERRORS)
async def cancel_order(order_id: int, service: ServiceDep) -> Response:
    service.cancel_order(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
