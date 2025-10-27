"""Tests for MQTT handler"""

import pytest
import json
from unittest.mock import MagicMock, patch
from backend.mqtt.handler import handle_mqtt_message, handle_food_order_message
from backend.config.constants import MQTTTopics


@pytest.mark.asyncio
async def test_handle_mqtt_message_food_order(mock_mqtt_client, sample_order_json):
    """Test handling food order message"""
    message = MagicMock()
    message.topic.value = MQTTTopics.FOOD_ORDERS_NEW
    message.payload.decode.return_value = sample_order_json

    with patch("backend.mqtt.handler.handle_food_order_message") as mock_handler:
        await handle_mqtt_message(message, mock_mqtt_client)
        mock_handler.assert_called_once()


@pytest.mark.asyncio
async def test_handle_mqtt_message_unhandled_topic(mock_mqtt_client):
    """Test handling message on unhandled topic"""
    message = MagicMock()
    message.topic.value = "unknown/topic"
    message.payload.decode.return_value = "{}"

    # should log warning but not crash
    await handle_mqtt_message(message, mock_mqtt_client)


@pytest.mark.asyncio
async def test_handle_food_order_message_success(mock_mqtt_client, sample_order_json):
    message = MagicMock()
    message.payload.decode.return_value = sample_order_json

    with patch("backend.mqtt.handler.prepare_food") as mock_prepare:
        from backend.models.CompletedOrder import CompletedOrder

        mock_completed = CompletedOrder(
            tableNumber=1,
            foodName="Pizza",
            orderId="f3fff827-2416-402c-99dd-a92b80a7f322",
            orderedAt=1234567890,
            completedAt=1234567900,
        )
        mock_prepare.return_value = mock_completed

        await handle_food_order_message(message, mock_mqtt_client)

        mock_prepare.assert_called_once()

        mock_mqtt_client.publish.assert_called_once()
        call_args = mock_mqtt_client.publish.call_args
        assert call_args[0][0] == MQTTTopics.FOOD_ORDERS_COMPLETE
        assert "Pizza" in call_args[0][1]


@pytest.mark.asyncio
async def test_handle_food_order_message_invalid_json(mock_mqtt_client):
    """Test handling invalid JSON payload"""
    message = MagicMock()
    message.payload.decode.return_value = "invalid json{{"

    # should not raise error
    await handle_food_order_message(message, mock_mqtt_client)

    mock_mqtt_client.publish.assert_not_called()


@pytest.mark.asyncio
async def test_handle_food_order_message_missing_fields(mock_mqtt_client):
    message = MagicMock()
    message.payload.decode.return_value = json.dumps({"tableNumber": 1})  # no foodName

    await handle_food_order_message(message, mock_mqtt_client)

    mock_mqtt_client.publish.assert_not_called()
