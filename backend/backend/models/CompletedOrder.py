from .Order import Order


class CompletedOrder(Order):
    completedAt: int
