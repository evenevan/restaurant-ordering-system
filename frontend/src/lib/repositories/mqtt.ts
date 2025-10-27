import mqtt, { type MqttClient } from "mqtt";
import {
	PUBLIC_MQTT_BROKER_URL,
	PUBLIC_MQTT_CLIENT_ID,
} from "$env/static/public";

let client: MqttClient | null = null;

export const getMqttClient = async (): Promise<MqttClient> => {
	if (client) return client;
	client = await mqtt.connectAsync(PUBLIC_MQTT_BROKER_URL, {
		clean: false,
		clientId: PUBLIC_MQTT_CLIENT_ID,
	});

	client.on("error", (err) => {
		console.error("MQTT Connect Error:", err);
	});

	return client;
};
