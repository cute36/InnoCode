import time
from aiogram import BaseMiddleware
from aiogram.types import Message
from collections import defaultdict

# Создаём класс промежуточного слоя (middleware), наследуем его от BaseMiddleware
class AntiFloodMiddleware(BaseMiddleware):

    # Конструктор класса, принимаем задержку между сообщениями (по умолчанию 2 секунды)
    def __init__(self, delay: float = 2.0):
        self.delay = delay
        # Словарь, в котором будем хранить время последнего сообщения от каждого пользователя
        # Если пользователя ещё нет в словаре, значение будет 0
        self.last_time = defaultdict(lambda: 0)

    # Метод, который будет вызываться перед каждым хендлером
    async def __call__(self, handler, event: Message, data):
        user_id = event.from_user.id               # Получаем ID пользователя
        current_time = time.time()                 # Текущее время в секундах (float)

        # Если пользователь отправил сообщение раньше, чем прошло delay секунд
        if current_time - self.last_time[user_id] < self.delay:
            # Отвечаем ему, что нужно подождать
            await event.answer("Подожди немного")
            return  # Прерываем обработку — хендлер не будет вызван
        else:
            # Обновляем время последнего сообщения пользователя
            self.last_time[user_id] = current_time
            # Продолжаем обработку — вызываем хендлер
            return await handler(event, data)
