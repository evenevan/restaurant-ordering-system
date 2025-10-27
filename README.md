# Restaurant Ordering System

An instance is live on [https://osensa.evanfeng.dev/](https://osensa.evanfeng.dev/).

## Local Setup

Note: although this was written on Windows, this should work for macOS and Linux as well.

### Env Configuration

On the frontend and backend, copy over .env.example into .env. By default, `test.mosquitto.org` is used as the broker for MQTT over Websocket though other brokers work too.

### Backend

The backend uses the `aiomqtt` library for MQTT and uses Poetry to manage dependencies. To install Poetry, you can follow their [install guide here](https://python-poetry.org/docs/#installation).

Then, from within `backend`:

```
poetry install
poetry run python -m backend
```

### Frontend

The frontend uses SvelteKit along with `shadcn` and `TailwindCSS`.

With a recent Node.js install (LTS is known working) and `npm`, from within `frontend`, run:

```
npm i
npm run dev
```

## Deployment

### Backend

The backend can be containerized via the included Dockerfile. For the live demo, an instance of the container is running on my server. As the backend connects to the broker, the backend is not directly exposed via any ports.

### Frontend

The frontend can be built as a static site with:

```
cd frontend
npm run build
```

The live demo is hosted through Cloudflare Pages.

## Flow

With the frontend loaded, you will be able to click on the Order Food button for any table. When pressed, a dialog will open requesting the food name. Once submitted, the pending order will show on the respective table.

Once ready, the frontend will receive the completed order, which is used to update the order from pending to received.

Tables can order at the same time, but the chef in the back can only prepare one item at a time.

## MQTT Overview

When an order is made, an event is sent to the backend containing this schema:

```ts
interface Order {
	tableNumber: number;
	foodName: string;
	orderedAt: number;
	orderId: string;
}
```

The backend will process the event and returns an object that is the same as the Order except for the addition of a `completedAt` field.

## Testing

The backend has `pytest` for unit level testing. These can be run by first navigating into `backend` and then:

```
poetry run pytest
```

The frontend contains a (basic) e2e testing suite through Cypress that ensures ordering food works. Before running this, you need to have the frontend and backend running locally. The frontend should be running on `http://localhost:3000`. The Cypress tests can be run with the following:

1. Run `npm run cy:open`
2. Select E2E Testing
3. Select any of the browsers available
4. Click on the `order.cy.ts` test

## Security

MQTT is configured for TLS on both connections to the MQTT broker. Payloads from the broker are validated on both ends to assure conformance to the schema.
