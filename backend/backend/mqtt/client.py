import logging
import asyncio
from aiomqtt import Client, TLSParameters, MqttError
from backend.mqtt.handler import handle_mqtt_message
from backend.config.constants import MQTTTopics, MQTT_RECONNECT_INTERVAL
from backend.config.settings import settings

logger = logging.getLogger(__name__)


async def run_async_client():
    while True:
        try:
            await use_client()
        except MqttError as e:
            logger.exception(e)
            logger.error(
                "MQTT connection error: %s. Reconnecting in %d seconds...",
                e,
                MQTT_RECONNECT_INTERVAL,
            )
            await asyncio.sleep(MQTT_RECONNECT_INTERVAL)
        except Exception:
            logger.exception(
                "Unexpected error in MQTT client. Reconnecting in %d seconds...",
                MQTT_RECONNECT_INTERVAL,
            )
            await asyncio.sleep(MQTT_RECONNECT_INTERVAL)


async def use_client():
    logger.info(
        "Connecting to MQTT broker at %s:%d%s",
        settings.mqtt_broker_url,
        settings.mqtt_broker_port,
        settings.mqtt_broker_path,
    )
    async with Client(
        settings.mqtt_broker_url,
        port=settings.mqtt_broker_port,
        identifier=settings.mqtt_client_id,
        websocket_path=settings.mqtt_broker_path,
        clean_session=True,
        transport='websockets',
        tls_params=TLSParameters(),
        keepalive=60,
    ) as client:
        logger.info(
            "MQTT client connected successfully (Client ID: %s)",
            settings.mqtt_client_id,
        )
        await client.subscribe(MQTTTopics.FOOD_ORDERS_NEW)
        logger.info("Subscribed to topic: %s", MQTTTopics.FOOD_ORDERS_NEW)

        async for message in client.messages:
            logger.debug("Received message on topic: %s", message.topic.value)
            await handle_mqtt_message(message, client)
