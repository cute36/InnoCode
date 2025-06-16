from aiogram import  types
import aiogram
from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
import random
from keyboards import inline
from keyboards import reply
from handlers.source.texts import start_message,download_prompts,get_id_prompts,help_text,about_text
from keyboards.inline import escape_keyboard, start_keyboard, escape_keyboard_caption
from aiogram.types import FSInputFile
from states import Download,ID


callback_router = Router()


@callback_router.callback_query(F.data == "download_pressed")
async def handle_download(callback: aiogram.types.CallbackQuery,state: FSMContext):
    await callback.answer("Обрабатывается...")
    await callback.message.delete()
    photo = FSInputFile("SRC/download4.png")
    await callback.message.answer_photo(photo,caption=download_prompts,parse_mode="HTML",reply_markup=escape_keyboard_caption)
    await state.set_state(Download.wait_link)


@callback_router.callback_query(F.data == "id_pressed")
async def handle_id(callback: aiogram.types.CallbackQuery,state: FSMContext):
    await callback.answer("Обрабатывается...")
    await callback.message.delete()
    await callback.message.answer(text=get_id_prompts,parse_mode="HTML",reply_markup=escape_keyboard)
    await state.set_state(ID.wait_id)

@callback_router.callback_query(F.data == "escape_pressed")
async def handle_cancel(callback: aiogram.types.CallbackQuery,state: FSMContext):
    await callback.answer("Возвращаю...")
    await callback.message.edit_text(text=start_message(callback.from_user),parse_mode="HTML",reply_markup=start_keyboard)
    await state.clear()
@callback_router.callback_query(F.data == "escape_caption_pressed")
async def handle_caption_cancel(callback: aiogram.types.CallbackQuery,state:FSMContext):
    await callback.answer("Возвращаю...")
    await callback.message.delete()
    photo = FSInputFile("SRC/start2.jpg")
    await callback.message.answer_photo(photo,caption=start_message(callback.from_user), parse_mode="HTML",reply_markup=start_keyboard)
    await state.clear()


@callback_router.callback_query(F.data == "help_pressed")
async def handle_help(callback: aiogram.types.CallbackQuery):
    await callback.answer("Обрабатывается...")
    await callback.message.delete()
    await callback.message.answer(text=help_text,parse_mode="HTML",reply_markup=inline.escape_keyboard)

@callback_router.callback_query(F.data == "about_pressed")
async def handle_about(callback: aiogram.types.CallbackQuery):
    await callback.answer("Обрабатывается...")
    await callback.message.delete()
    await callback.message.answer(text=about_text,parse_mode="HTML",reply_markup=escape_keyboard)

@callback_router.callback_query(F.data == "mp3",Download.wait_format)
async def handler_mp3(callback: aiogram.types.CallbackQuery,state: FSMContext):
    text_mp3 = """
    🔄 <b>Конвертирую в MP3...</b>

    Ваш аудиофайл готовится! Обычно это занимает 15-30 секунд.

    📌 <i>Пока ждете:</i>
    • Проверьте громкость на устройстве
    • Убедитесь в стабильном интернет-соединении

    Статус: <code>Извлекаем аудиодорожку...</code>
    """
    await callback.answer("Готовлю файл...")
    await callback.message.answer(text=text_mp3,parse_mode="HTML")
    await state.set_state(Download.wait_file)

@callback_router.callback_query(F.data == "mp4",Download.wait_format)
async def handler_mp4(callback: aiogram.types.CallbackQuery,state: FSMContext):
    text_mp4 = """
        🔄 <b>Конвертирую в MP4...</b>

        Ваш видеофайл готовится! Обычно это занимает 15-30 секунд.

        📌 <i>Пока ждете:</i>
        • Проверьте громкость на устройстве
        • Убедитесь в стабильном интернет-соединении

        Статус: <code>Извлекаем видеодорожку...</code>
        """
    await callback.answer("Готовлю файл...")
    await callback.message.answer(text=text_mp4, parse_mode="HTML")
    await state.set_state(Download.wait_file)
