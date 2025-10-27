import logging
from random import randint
import asyncio
from backend.models.Order import Order
from backend.models.CompletedOrder import CompletedOrder
import datetime

logger = logging.getLogger(__name__)


async def prepare_food(order: Order):
    preparation_time = randint(5, 15)
    logger.info(
        "Preparing food '%s' for table %d - estimated time: %d seconds",
        order.foodName,
        order.tableNumber,
        preparation_time,
    )
    await asyncio.sleep(preparation_time)
    logger.info("Food '%s' is ready for table %d!", order.foodName, order.tableNumber)

    completion_unix_time = int(datetime.datetime.now().timestamp()) * 1000
    completed_order = CompletedOrder(
        **order.model_dump(), completedAt=completion_unix_time
    )
    return completed_order
