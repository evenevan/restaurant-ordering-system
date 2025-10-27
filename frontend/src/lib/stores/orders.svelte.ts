import { getMqttClient } from "$lib/repositories/mqtt";
import { MQTT_TOPICS } from "$lib/constants";

export interface Order {
	tableNumber: number;
	foodName: string;
	orderedAt: number;
	orderId: string;
	completedAt?: number;
}

class OrderStore {
	orders = $state<Order[]>([]);

	async init() {
		const client = await getMqttClient();
		await client.subscribeAsync(MQTT_TOPICS.FOOD_ORDERS_COMPLETE, {
			qos: 2,
		});

		client.on("message", (topic, payload) => {
			if (topic !== MQTT_TOPICS.FOOD_ORDERS_COMPLETE) {
				console.warn("Ignoring message on unknown topic:", topic);
				return;
			}

			const completedOrder = this.verifyOrderPayload(payload.toString());
			if (!completedOrder) {
				console.warn("Received invalid order payload:", payload.toString());
				return;
			}

			let placedOrder = this.orders.find(
				(o) => o.orderId === completedOrder.orderId,
			);
			if (!placedOrder) {
				console.warn(
					"Received completion for unknown order ID:",
					completedOrder.orderId,
				);
				return;
			}

			placedOrder.completedAt = completedOrder.completedAt;
			console.log("Order completed:", placedOrder.foodName);
		});
	}

	private verifyOrderPayload(payload: string): Order | null {
		try {
			const parsed = JSON.parse(payload);
			if (
				typeof parsed.tableNumber === "number" &&
				typeof parsed.foodName === "string" &&
				typeof parsed.orderedAt === "number" &&
				typeof parsed.orderId === "string" &&
				typeof parsed.completedAt === "number"
			) {
				return parsed as Order;
			}
			return null;
		} catch {
			return null;
		}
	}

	private async publish(topic: string, message: string) {
		const client = await getMqttClient();
		await client.publishAsync(topic, message, { qos: 2 });
	}

	async orderFood(table: number, food: string) {
		const order: Order = {
			tableNumber: table,
			foodName: food,
			orderedAt: Date.now(),
			orderId: crypto.randomUUID(),
		};
		this.orders.push(order);
		await this.publish(MQTT_TOPICS.FOOD_ORDERS_NEW, JSON.stringify(order));
	}

	async disconnect() {
		const client = await getMqttClient();
		await client.endAsync();
	}
}

export const orderStore = new OrderStore();
