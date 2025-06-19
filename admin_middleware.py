from aiogram import types
from aiogram import BaseMiddleware
from config import ADMIN_IDS


class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.Message | types.CallbackQuery, data):
        # Получаем список команд, требующих админских прав
        admin_commands = {'/stats'}  # Добавьте сюда другие админские команды

        # Проверяем только команды из admin_commands
        if isinstance(event, types.Message) and event.text:
            command = event.text.split()[0].lower()
            if command in admin_commands:
                if event.from_user.id not in ADMIN_IDS:
                    await event.answer("❌ Эта команда доступна только администраторам")
                    return

        return await handler(event, data)