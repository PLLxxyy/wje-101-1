import asyncio
import logging

from app.database import engine
from app.utils.migrations import run_migrations

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


if __name__ == "__main__":
    asyncio.run(run_migrations(engine))
    print("Migrations completed successfully.")
