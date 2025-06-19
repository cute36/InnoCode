import time
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Union
from collections import defaultdict

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.last_time = defaultdict(lambda: 0)

    async def __call__(self, handler, event: Union[Message, CallbackQuery], data):
        user_id = event.from_user.id
        current_time = time.time()

        # Проверяем, не спамит ли пользователь
        if current_time - self.last_time[user_id] < self.delay:
            if isinstance(event, CallbackQuery):
                await event.answer("⏳ Подождите немного перед следующим действием", show_alert=True)
            elif isinstance(event, Message):
                await event.answer("⏳ Подождите немного перед следующим сообщением")
            return  # Прерываем обработку
        else:
            self.last_time[user_id] = current_time  # Обновляем время последнего действия
            return await handler(event, data)  # Пропускаем запрос дальше