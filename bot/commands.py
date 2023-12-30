from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/start", description="Начать диалог"),
        BotCommand(command="/cancel", description="Вернуться в главное меню"),
        BotCommand(
            command="/data", description="Отправить или обновить данные"
        ),
    ]

    await bot.set_my_commands(main_menu_commands)
