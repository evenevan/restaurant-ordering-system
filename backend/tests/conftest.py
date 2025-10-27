import pytest
from unittest.mock import AsyncMock, MagicMock
from aiomqtt import Client


@pytest.fixture
def mock_mqtt_client():
    """Mock MQTT client for testing"""
    client = AsyncMock(spec=Client)
    client.publish = AsyncMock()
    client.subscribe = AsyncMock()
    client.subscribeAsync = AsyncMock()
    client.publishAsync = AsyncMock()
    return client


@pytest.fixture
def sample_order_payload():
    return {
        "tableNumber": 1,
        "foodName": "Pizza",
        "orderId": "f3fff827-2416-402c-99dd-a92b80a7f322",
        "orderedAt": 1234567890,
    }


@pytest.fixture
def sample_order_json(sample_order_payload):
    import json

    return json.dumps(sample_order_payload)
