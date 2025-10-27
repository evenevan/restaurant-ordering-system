import mqtt, { type MqttClient } from "mqtt";
import {
	PUBLIC_MQTT_BROKER_URL,
} from "$env/static/public";

let client: MqttClient | null = null;

export const getMqttClient = async (): Promise<MqttClient> => {
	console.log("Getting MQTT client...");

	if (client && client.connected) {
		console.log("Reusing existing connected client");
		return client;
	}

	if (client) {
		console.log("Cleaning up disconnected client");
		client.removeAllListeners();
		try {
			await client.endAsync(true); // Force end
		} catch (err) {
			console.warn("Error ending client:", err);
		}
		client = null;
	}

	console.log("Creating new MQTT client");
	client = await mqtt.connectAsync(PUBLIC_MQTT_BROKER_URL, {
		clean: true,
		keepalive: 60,
		reconnectPeriod: 1000,
		connectTimeout: 30000,
		resubscribe: false,
	});

	client.on("error", (err) => {
		console.error("MQTT Connect Error:", err);
	});

	client.on("disconnect", (packet) => {
		console.warn("MQTT Disconnected:", packet);
	});

	client.on("reconnect", () => {
		console.log("MQTT Reconnecting...");
	});

	client.on("close", () => {
		console.log("MQTT Connection Closed");
	});

	client.on("connect", (connack) => {
		console.log("MQTT Connected:", connack);
	});

	client.on("offline", () => {
		console.warn("MQTT Client is Offline");
	});

	client.on("end", () => {
		console.log("MQTT Client Ended");
		client = null;
	});

	return client;
};
