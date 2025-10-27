import pytest
import asyncio
from unittest.mock import patch
from backend.services.order import prepare_food
from backend.models.Order import Order
from backend.models.CompletedOrder import CompletedOrder


@pytest.mark.asyncio
async def test_prepare_food_returns_completed_order():
    order = Order(
        tableNumber=1,
        foodName="Pizza",
        orderId="f3fff827-2416-402c-99dd-a92b80a7f322",
        orderedAt=1234567890,
    )
    
    with patch("backend.services.order.randint", return_value=1):
        completed = await prepare_food(order)
    
    assert isinstance(completed, CompletedOrder)
    assert completed.tableNumber == order.tableNumber
    assert completed.foodName == order.foodName
    assert completed.orderId == order.orderId
    assert completed.orderedAt == order.orderedAt
    assert hasattr(completed, "completedAt")
    assert completed.completedAt > 0


@pytest.mark.asyncio
async def test_prepare_food_timing():
    order = Order(
        tableNumber=2,
        foodName="Burger",
        orderId="f3fff827-2416-402c-99dd-a92b80a7f322",
        orderedAt=1234567890,
    )
    
    with patch("backend.services.order.randint", return_value=1):
        start_time = asyncio.get_event_loop().time()
        await prepare_food(order)
        end_time = asyncio.get_event_loop().time()
        
        assert end_time - start_time >= 0.9
