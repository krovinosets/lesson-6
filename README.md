# ДЗ 6. Учёт заказов кофейни

Python 3.10+. Реализованы основная часть и бонус: PaginationDep, ограничения limit и сортировка в сервисе.

## Запуск

Из корня распакованного проекта:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Скопируйте `.env.example` в `.env`, при необходимости измените настройки.

```bash
fastapi dev app/main.py
```

Документация: http://127.0.0.1:8000/docs

## Самопроверка без HTTP и FastAPI

В Python-консоли из корня проекта:

```python
from app.repository import OrderRepository
from app.service import OrderService
from app.schemas import OrderCreate, OrderUpdate
from app.exceptions import OrderAlreadyCompletedError, OrderNotFoundError

service = OrderService(OrderRepository())
order = service.create_order(OrderCreate(drink="Латте", size="medium", quantity=2))
service.update_order(order.id, OrderUpdate(status="completed"))
for operation in (
    lambda: service.update_order(order.id, OrderUpdate(customer_name="Ирина")),
    lambda: service.update_order(order.id, OrderUpdate(status="pending")),
    lambda: service.update_order(order.id, OrderUpdate()),
    lambda: service.cancel_order(order.id),
):
    try:
        operation()
    except OrderAlreadyCompletedError as exc:
        print(exc)
    else:
        raise AssertionError("Выполненный заказ нельзя менять или отменять")

try:
    service.get_order(999)
except OrderNotFoundError as exc:
    print(exc)
```

## Самопроверка через /docs

1. POST /orders: создайте заказ; ожидается 201, pending, id и created_at.
2. PATCH /orders/{order_id}: передайте только quantity; остальные поля не меняются.
3. PATCH: установите completed. Сам переход разрешён.
4. PATCH выполненного заказа (включая пустой объект или смену статуса) и DELETE: ожидается 409 с detail.
5. GET/PATCH/DELETE отсутствующего заказа: ожидается 404 с detail.
6. DELETE невыполненного заказа: 204 без тела; следующий созданный id не повторяет удалённый.
7. GET /orders: проверьте status, sort_by=drink, limit и offset. Сначала фильтр, затем сортировка, затем срез.
8. Неположительный limit, отрицательный offset и limit выше MAX_PAGE_SIZE: 422.
9. GET /info: orders_count соответствует количеству всех сохранённых заказов.

Архитектура APIRouter и относительные импорты соответствуют документации:
https://fastapi.tiangolo.com/tutorial/bigger-applications/
