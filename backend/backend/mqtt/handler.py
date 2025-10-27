import logging
import json
from aiomqtt import Message, Client
from backend.services.order import prepare_food
from backend.config.constants import MQTTTopics
from backend.models.Order import Order


logger = logging.getLogger(__name__)


async def handle_mqtt_message(message: Message, client: Client):
    topic = message.topic.value

    if topic == MQTTTopics.FOOD_ORDERS_NEW:
        await handle_food_order_message(message, client)
    else:
        logger.warning("Received message on unhandled topic: %s", topic)


async def handle_food_order_message(message: Message, client: Client):
    payload_str = message.payload.decode()
    logger.info("Received new food order: %s", payload_str)

    try:
        payload = json.loads(payload_str)
        order = Order(
            **payload
        )  # Assuming payload is already a dict with correct structure
    except Exception:
        logger.exception("Invalid input payload: %s", payload_str)
        return

    logger.info(
        "Processing order - Order Id: %s, Table: %s, Food: %s, Ordered at: %d",
        order.orderId,
        order.tableNumber,
        order.foodName,
        order.orderedAt,
    )

    completed_order = await prepare_food(order)
    response = completed_order.model_dump_json()
    await client.publish(MQTTTopics.FOOD_ORDERS_COMPLETE, response, qos=2)
    logger.info("Food order %s completed and published", completed_order.orderId)
