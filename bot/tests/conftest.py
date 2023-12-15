import logging
import os
import warnings

import pytest_asyncio

warnings.filterwarnings("ignore", category=DeprecationWarning)

from dotenv import load_dotenv
from pyrogram import Client

logger = logging.getLogger(__name__)

load_dotenv()

api_id = int(os.getenv("APP_ID"))
api_hash = os.getenv("APP_HASH")


@pytest_asyncio.fixture
async def client():
    async with Client(
        "my_account",
        api_id=api_id,
        api_hash=api_hash,
        test_mode=True,
        in_memory=True,
        phone_number="99966" + "1" + "2023",
        phone_code="1" * 5,
    ) as client:
        yield client
        await client.stop()
