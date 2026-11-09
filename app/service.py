from typing import Literal
from .exceptions import OrderAlreadyCompletedError, OrderNotFoundError
from .repository import OrderRepository
from .schemas import Order, OrderCreate, OrderStatus, OrderUpdate

SortBy = Literal["created_at", "drink"]


class OrderService:
    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def create_order(self, data: OrderCreate) -> Order:
        order = Order(id=self._repository.next_id(), **data.model_dump())
        return self._repository.add(order)

    def get_order(self, order_id: int) -> Order:
        order = self._repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order

    def list_orders(self, status: OrderStatus | None = None,
                    limit: int | None = None, offset: int = 0,
                    sort_by: SortBy = "created_at") -> list[Order]:
        orders = self._repository.get_all()
        if status is not None:
            orders = [order for order in orders if order.status == status]
        orders.sort(key=lambda order: getattr(order, sort_by))
        return orders[offset:] if limit is None else orders[offset:offset + limit]

    def count_orders(self) -> int:
        return len(self._repository.get_all())

    def _get_editable_order(self, order_id: int) -> Order:
        order = self.get_order(order_id)
        if order.status == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order_id)
        return order

    def update_order(self, order_id: int, data: OrderUpdate) -> Order:
        self._get_editable_order(order_id)
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        updated = self._repository.update(order_id, changes)
        if updated is None:
            raise OrderNotFoundError(order_id)
        return updated

    def cancel_order(self, order_id: int) -> None:
        self._get_editable_order(order_id)
        if not self._repository.delete(order_id):
            raise OrderNotFoundError(order_id)
