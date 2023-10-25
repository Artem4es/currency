import logging
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler

import uvicorn
from fastapi import FastAPI, Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from database import get_async_session
from src.currency_app.dependencies import get_async_client
from src.currency_app.router import router as currency_router
from src.currency_app.service import update_currency_table

settings = Settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):   # можно ли тут depends?
    """Update currency data in DB"""

    async for client in get_async_client():
        async for db_session in get_async_session():
            await update_currency_table(client, db_session)
    # db_session = get_async_session()

    yield


app = FastAPI(name=settings.fastapi_name, debug=settings.fastapi_debug, lifespan=lifespan)
app.include_router(currency_router, tags=["Currency_API"])


def setup_logging() -> None:
    handler = RotatingFileHandler("src/logs/app.log", maxBytes=5000000, backupCount=5)
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