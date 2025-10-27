from pydantic import BaseModel


class Order(BaseModel):
  tableNumber: int
  foodName: str
  orderId: str
  orderedAt: int
  