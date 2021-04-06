import logging
import os

from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise

log = logging.getLogger("uvicorn")


def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.text_summary"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def generate_schema():
    """`Generate schema` means connect to the database backend
    and create tables according to the specification laid out
    in "app/models/". Below, we can specify which specs to use
    in arg `modules={'models': ['...']}`.

    In our case, app/models/text_summary.py contains a class
    subclassed from tortoise.models.Model. This class has 3
    fields: 'url', 'summary', and 'created_at'. When we call
    Tortoise.init(...), then Tortoise.generate_schemas(), we
    tell tortoise to connect to the db and create a table called
    'textsummary', with the 3 fields (and their data type)
    specifed in text_summary.py.
    """
    log.info("Initializing Tortoise...")

    await Tortoise.init(db_url=os.getenv("DATABASE_URL"), modules={"models": ["models.text_summary"]})
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
