from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .config import get_settings
from .dependencies import ServiceDep, SettingsDep
from .exceptions import OrderAlreadyCompletedError, OrderNotFoundError
from .routers import orders

app = FastAPI(
    title=get_settings().app_name,
    description="Сервис учёта заказов кофейни: создание, просмотр, изменение и отмена заказов.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Заказы", "description": "Операции с заказами кофейни"},
        {"name": "Сервис", "description": "Информация о приложении"},
    ],
)
app.include_router(orders.router)


@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(request: Request, exc: OrderNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(OrderAlreadyCompletedError)
async def order_completed_handler(request: Request, exc: OrderAlreadyCompletedError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.get("/", tags=["Сервис"], summary="Приветствие сервиса")
async def root(settings: SettingsDep):
    return {"message": f"Добро пожаловать в сервис «{settings.app_name}»!"}


@app.get("/info", tags=["Сервис"], summary="Информация о сервисе")
async def info(settings: SettingsDep, service: ServiceDep):
    return {"app_name": settings.app_name, "orders_count": service.count_orders()}
