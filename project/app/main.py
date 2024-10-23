from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.auth.config import firebase_init
from app.config import Settings, get_settings
from app.db import config
from app.routers import api
import logging

logger = logging.getLogger(__name__)

app = FastAPI()


@asynccontextmanager
async def get_db(app: FastAPI):

    # Connect to Firebase...
    await firebase_init()

    # Get DB Secrets...
    settings = get_settings()
    db_uri = settings.db_uri
    db_name = settings.db_name

    # Connect to Database...
    await config.init_db(db_uri, db_name)
    print("Connected to database")
    yield


description = "Launch App APIs for Aquesa"

app = FastAPI(
    title="Aquesa Launch App APIs",
    summary="Provides APIs for Managing Users and Aquesa Customers",
    description=description,
    version="1.0.0",
    lifespan=get_db,
)


app.include_router(
    api.router,
    prefix="/api",
)


@app.get("/", tags=["Server Health"])
async def root(settings: Settings = Depends(get_settings)):
    return {
        "message": "Aquesa Launch App APIs",
        "environment": settings.environment,
        "testing": settings.testing,
    }


@app.get("/health", tags=["Server Health"])
async def health():
    return {"ping": True}
