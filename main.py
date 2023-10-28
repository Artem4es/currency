import logging
from logging.handlers import RotatingFileHandler

import uvicorn
from fastapi import FastAPI

from config import Settings
from src.currency_app.routers import router as currency_router
from src.currency_app.utils import lifespan

settings = Settings()
logger = logging.getLogger(__name__)


app = FastAPI(name=settings.fastapi_name, debug=settings.fastapi_debug, lifespan=lifespan)
app.include_router(currency_router, tags=["Currency_API"])


def setup_logging() -> None:
    handler = RotatingFileHandler("./src/currency_app/logs/app.log", maxBytes=5000000, backupCount=5)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[handler],
        encoding="utf-8",
    )


if __name__ == "__main__":
    try:
        setup_logging()
        logger.info("FAST Api app has been started...")
        uvicorn.run(app=app, host=settings.fastapi_host, port=settings.fastapi_port)

    except Exception as e:
        logger.error(e, exc_info=True)
        raise e

    finally:
        logger.info("FAST Api app has been STOPPED.")
