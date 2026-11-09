from itertools import count
from typing import Any
from .schemas import Order


class OrderRepository:
    def __init__(self):
        self._orders: list[Order] = []
        self._ids = count(1)

    def next_id(self) -> int:
        return next(self._ids)

    def get_all(self) -> list[Order]:
        return [order.model_copy(deep=True) for order in self._orders]

    def get_by_id(self, order_id: int) -> Order | None:
        for order in self._orders:
            if order.id == order_id:
                return order.model_copy(deep=True)
        return None

    def add(self, order: Order) -> Order:
        self._orders.append(order.model_copy(deep=True))
        return order.model_copy(deep=True)

    def update(self, order_id: int, update_data: dict[str, Any]) -> Order | None:
        for index, order in enumerate(self._orders):
            if order.id == order_id:
                updated = Order.model_validate({**order.model_dump(), **update_data})
                self._orders[index] = updated
                return updated.model_copy(deep=True)
        return None

    def delete(self, order_id: int) -> bool:
        for index, order in enumerate(self._orders):
            if order.id == order_id:
                self._orders.pop(index)
                return True
        return False
