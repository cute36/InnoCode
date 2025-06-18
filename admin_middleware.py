from aiogram import types
from config import ADMIN_IDS


class AdminMiddleware:
    async def __call__(self, handler, event: types.Message | types.CallbackQuery, data):
        if not isinstance(event, (types.Message, types.CallbackQuery)):
            return await handler(event, data)

        user_id = event.from_user.id
        if user_id not in ADMIN_IDS:
            if isinstance(event, types.CallbackQuery):
                await event.answer("❌ Доступ запрещен!", show_alert=True)
            else:
                await event.answer("❌ У вас нет прав доступа")
            return

        return await handler(event, data)