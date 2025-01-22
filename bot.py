import django_setup
import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram_bot.handlers import start, phone_handler, gift_handler, balance_handler, advancement_handler, back

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    """Запуск процесса поллинга новых апдейтов"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    dp.include_routers(start.router)
    dp.include_routers(phone_handler.router)
    dp.include_routers(gift_handler.router)
    dp.include_routers(balance_handler.router)
    dp.include_routers(advancement_handler.router)
    dp.include_routers(back.router)



    asyncio.run(main())
