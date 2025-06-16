from aiogram import Dispatcher, Bot
from config import TOKEN
import asyncio

from handlers.callbacks import callback_router
from handlers.commands import command_router
from handlers.subscription import router,SubscriptionMiddleware



dp = Dispatcher()
dp.message.middleware(SubscriptionMiddleware())
dp.callback_query.middleware(SubscriptionMiddleware())

dp.include_router(command_router)
dp.include_router(callback_router)
dp.include_router(router)

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
