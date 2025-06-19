from aiogram import Dispatcher, Bot
from config import TOKEN
import asyncio
from admin_middleware import AdminMiddleware
from antispam_middleware import AntiFloodMiddleware
from handlers.callbacks import callback_router
from handlers.commands import command_router
from handlers.subscription import router,SubscriptionMiddleware



dp = Dispatcher()

dp.message.middleware(AntiFloodMiddleware(delay=2.0))



dp.message.middleware(SubscriptionMiddleware())
dp.callback_query.middleware(SubscriptionMiddleware())

dp.message.middleware(AdminMiddleware())
dp.callback_query.middleware(AdminMiddleware())

dp.include_router(command_router)
dp.include_router(callback_router)
dp.include_router(router)

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
