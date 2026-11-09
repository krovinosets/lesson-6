from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class DrinkSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


class OrderStatus(str, Enum):
    pending = "pending"
    ready = "ready"
    completed = "completed"


class OrderCreate(BaseModel):
    drink: str = Field(min_length=1, description="Название напитка из меню", examples=["Латте"])
    size: DrinkSize = Field(description="Размер напитка", examples=["medium"])
    quantity: int = Field(gt=0, description="Количество напитков", examples=[2])
    customer_name: str | None = Field(default=None, description="Имя клиента", examples=["Ирина"])


class OrderUpdate(BaseModel):
    drink: str | None = Field(default=None, min_length=1, description="Название напитка из меню", examples=["Капучино"])
    size: DrinkSize | None = Field(default=None, description="Размер напитка", examples=["large"])
    quantity: int | None = Field(default=None, gt=0, description="Количество напитков", examples=[1])
    customer_name: str | None = Field(default=None, description="Имя клиента", examples=["Ирина"])
    status: OrderStatus | None = Field(default=None, description="Статус заказа", examples=["ready"])


class Order(OrderCreate):
    id: int = Field(description="Идентификатор заказа", examples=[1])
    status: OrderStatus = Field(default=OrderStatus.pending, description="Статус заказа")
    created_at: datetime = Field(default_factory=datetime.now, description="Время создания заказа")
