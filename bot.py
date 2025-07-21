from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

import handlers

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)