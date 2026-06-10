import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

logger = logging.getLogger(__name__)


async def run_migrations(engine: AsyncEngine) -> None:
    logger.info("Checking database migrations...")
    await _add_recipe_bean_id_column(engine)
    logger.info("Migrations completed.")


async def _add_recipe_bean_id_column(engine: AsyncEngine) -> None:
    async with engine.connect() as conn:
        result = await conn.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'brew_recipes' AND column_name = 'bean_id'
                """
            )
        )
        column_exists = result.scalar_one_or_none() is not None

        if column_exists:
            logger.info("Column 'brew_recipes.bean_id' already exists, skipping.")
            return

        logger.info("Adding column 'brew_recipes.bean_id' with foreign key to 'coffee_beans.id'...")

        await conn.execute(
            text(
                """
                ALTER TABLE brew_recipes
                ADD COLUMN bean_id INTEGER
                """
            )
        )

        await conn.execute(
            text(
                """
                ALTER TABLE brew_recipes
                ADD CONSTRAINT brew_recipes_bean_id_fkey
                FOREIGN KEY (bean_id) REFERENCES coffee_beans(id)
                ON DELETE SET NULL
                """
            )
        )

        await conn.execute(
            text(
                """
                CREATE INDEX ix_brew_recipes_bean_id
                ON brew_recipes(bean_id)
                """
            )
        )

        await conn.commit()
        logger.info("Column 'brew_recipes.bean_id' added successfully.")
