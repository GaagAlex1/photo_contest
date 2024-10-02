from database import async_engine
from models.orm import *
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_db_and_tables())
