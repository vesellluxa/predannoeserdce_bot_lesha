import pytest
from pyrogram import Client


@pytest.mark.asyncio
async def test_echo(client: Client):
    await client.send_message("NewHeartBot", "Pew Pew")
    chat = await client.get_chat("@NewHeartBot")
    hist = client.get_chat_history(chat.id, 1)
    async for message in hist:
        assert message.text == "Pew Pew"


@pytest.mark.asyncio
async def test_help(client: Client):
    await client.send_message("NewHeartBot", "/help")
    chat = await client.get_chat("@NewHeartBot")
    hist = client.get_chat_history(chat.id, 1)
    async for message in hist:
        assert message.text == "Тут будет инструкция по использованию бота"
