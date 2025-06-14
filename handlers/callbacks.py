from aiogram import  types
import aiogram
from aiogram import Router
from aiogram import F
import random
from keyboards import inline
from keyboards import reply


callback_router = Router()

download_prompts ="""
📥 <b>Инструкция по загрузке:</b>
1. Отправьте ссылку на видео
2. Выберите формат:
   - MP4 (видео)
   - MP3 (аудио)
3. Получите файл за 15-60 сек.

<i>Примеры поддерживаемых ссылок:</i>
youtube.com/watch?v=...
tiktok.com/@user/video/..."""

get_id_prompts ="""
    📌 <b>Определю ID для:</b>
    → Пользователей (@nickname)
    → Стикеров (отправьте любой)
    → Чатов (пересланое сообщение)
    → Медиа (фото/видео/файлы)
    
    <i>Пример результата:</i>
    <code>тип файла: -100123456789</code>"""




@callback_router.callback_query(F.data == "download_pressed")
async def handle_download(callback: aiogram.types.CallbackQuery):
    await callback.answer("Обрабатывается...")
    await callback.message.answer(text=download_prompts,parse_mode="HTML")


@callback_router.callback_query(F.data == "id_pressed")
async def handle_id(callback: aiogram.types.CallbackQuery):
    await callback.answer("Обрабатывается...")
    await callback.message.answer(text=get_id_prompts,parse_mode="HTML")

@callback_router.callback_query(F.data == "escape_pressed")
async def handle_cancel(callback: aiogram.types.CallbackQuery):
    await callback.answer("Обрабатывается...")
