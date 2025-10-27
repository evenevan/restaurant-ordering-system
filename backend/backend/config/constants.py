from enum import Enum


class MQTTTopics(str, Enum):
    FOOD_ORDERS_NEW = "efa34/food/orders/new"
    FOOD_ORDERS_COMPLETE = "efa34/food/orders/complete"
