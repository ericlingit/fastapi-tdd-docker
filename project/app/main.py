import logging

from fastapi import FastAPI

from app.api import ping, summary
from app.db import init_db


log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(summary.router, prefix="/summary", tags=["summary"])

    return application


app = create_application()


@app.on_event("startup")
async def startup():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown():
    log.info("Shutting down...")
