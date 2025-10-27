import asyncio
import logging
from backend.mqtt.client import run_async_client
from backend.config.settings import settings


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=settings.log_format,
    )


async def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting MQTT backend service...")

    try:
        await run_async_client()
    except Exception:
        logger.exception("Fatal error in main service")
        raise


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
