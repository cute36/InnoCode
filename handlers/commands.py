from aiogram import Router
from aiogram import filters
from aiogram import  types
from aiogram import F
import random
from handlers.source.texts import help_text,about_text
from keyboards import inline
from aiogram.types import FSInputFile
from urllib.parse import urlparse
from states import Download
from aiogram.fsm.context import FSMContext
from downloader import download_audio
import os
from keyboards.inline import escape_keyboard, escape_keyboard_caption
from config import ADMIN_IDS
from id_database import show_all_users
from aiogram.filters import Command




command_router = Router()


@command_router.message(Command("stats"), F.from_user.id.in_(ADMIN_IDS))
async def admin_stats(message: types.Message):
    try:
        # Получаем статистику из БД
        stats = show_all_users(return_string=True)

        # Форматируем ответ
        response = (
            "📊 <b>Статистика бота</b>\n"
            "------------------------\n"
            f"{stats}\n"
            f"👑 Админов: {len(ADMIN_IDS)}\n"
            "------------------------\n"
            "ℹ️ Полный дамп БД во вложении"
        )

        # Создаем временный файл с базой
        with open("users_db_dump.txt", "w", encoding="utf-8") as f:
            f.write(stats)

        # Отправляем сообщение с файлом
        await message.answer_document(
            document=types.FSInputFile("users_db_dump.txt"),
            caption=response,
            parse_mode="HTML",
            reply_markup=escape_keyboard_caption
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")
    finally:
        if os.path.exists("users_db_dump.txt"):
            os.remove("users_db_dump.txt")

@command_router.message(filters.Command("about"))
async def handler_about(a: types.Message,state: FSMContext) -> None:
    await a.answer(text=about_text,parse_mode="HTML")
    await state.clear()

@command_router.message(filters.Command("help"))
async def handler_about(h: types.Message,state: FSMContext) -> None:
    await h.answer(text=help_text, reply_markup=inline.help_keyboard, parse_mode="HTML")
    await state.clear()

#@command_router.message(F.sticker)
async def handler_sticker(text: types.Message):
    stickers = ["CAACAgIAAxkBAAOzaEwXDe9UAdcrvLIr9ka4tEffeMIAAtRcAAL_l2BKM4F7hnvAn-E2BA","CAACAgIAAxkBAAO1aEwXEEHTnaw_rmqgNbgO6ALrdQ8AAiRaAAJaUGFKk-Tak4_7Tag2BA","CAACAgIAAxkBAAO3aEwXEp_tIKxaSUf94QKUyp7jYsAAApBZAALY1GFKurbeu8UknXE2BA","CAACAgIAAxkBAAO5aEwXEywNfBzU6eNBllgoa-eHy20AAp5YAAIvDGBKCYbdO1qw2zo2BA","CAACAgIAAxkBAAO7aEwXFHrWSB4JjfEoylOpY_XGSBgAAv1dAAL0KWBKsErb7eNo7FI2BA","CAACAgIAAxkBAAO9aEwXFfafmW3z-NmnUwjy6qf9PakAAnlZAAIqaGFKVbQ1ypMu0N42BA","CAACAgIAAxkBAAO_aEwXFlNwZTPPm_8t_1HfZON1tboAAnNaAAJwtWFKW8ChVXuZ3ko2BA","CAACAgIAAxkBAAPBaEwXGOZFYtZg8h3KLDY3wkMKdTwAArpaAALunmhKisyIr6qxwuc2BA","CAACAgIAAxkBAAPDaEwXGZgwT30aF-lkKySVMi9XK2AAAgZZAALjmWBKG5vAPipLfuo2BA","CAACAgIAAxkBAAPFaEwXGtwYuVI0zm23QCMu8-4z4sYAArReAAIdJWhK_oyTwfJtE7s2BA","CAACAgIAAxkBAAPHaEwXG4wJt2yhYe1aA_Prlu2fMegAAp1eAAJrYWBK5gE4XU8C02Q2BA","CAACAgIAAxkBAAPJaEwXG1vJX0t7e5_vwxUYbmrolaoAAjteAAIPwWBKVHlUVG-vuFU2BA","CAACAgIAAxkBAAPLaEwXHAvEQAcUTR-CAAG7kDGbQb3YAAK1WgACAQZgSk5Q2YTbVWboNgQ","CAACAgIAAxkBAAPNaEwXHfroK4aw99GIn_O_sXv9L-cAAgphAAK5RWBKft4qfrpg9RU2BA","CAACAgIAAxkBAAPPaEwXHzG0GotsQ67Z5X1-E-p0BcwAAidtAAOn8Eu99IZh1I0pTzYE","CAACAgIAAxkBAAPRaEwXIHrmuAABAqlTonDm3Xru0dtvAAIGaQACcbTxS2Z3MjBm1jMgNgQ","CAACAgIAAxkBAAPTaEwXIG0cELLv4H2ugctGCdSE1wkAAvNhAAK-HfBLfNUk3DQ-aVk2BA","CAACAgIAAxkBAAPVaEwXIRswTB24wZr0bu-1C3pOqcgAAnt-AAKUT_FLewydwp-iTLY2BA","CAACAgIAAxkBAAPXaEwXIoC_8ZTdMn18mlV77ctnycYAAihsAAJZ0_BL44baC4-Mghc2BA"]
    await text.answer_sticker(random.choice(stickers))



### ЛОГИКА ПРОВЕРКИ ВАЛИДНОСТИ ССЫЛОК ###


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False

def is_supported_platform(url: str) -> bool:
    supported_domains = [
        'soundcloud.com'
    ]
    domain = urlparse(url).netloc.lower()
    return any(d in domain for d in supported_domains)


@command_router.message(F.text, Download.wait_link)
async def handle_links(message: types.Message, state: FSMContext) -> None:
    user_url = message.text.strip()

    if not is_valid_url(user_url):
        await message.answer(
            "❌ Это не похоже на валидную ссылку. Пример правильного формата:\nhttps://soundcloud.com/...")
        return

    if not is_supported_platform(user_url):
        await message.answer("⚠️ Этот сервис пока не поддерживается. Работаем с SoundCloud.")
        return

    # Уведомление о начале загрузки
    text_ans = """
    🔎 <b>Загружаю аудио...</b>

    ⏳ Это может занять от 15 секунд до 2 минут
    ⌛ Пожалуйста, подождите...
    """
    processing_msg = await message.answer(text=text_ans, parse_mode="HTML",reply_markup=escape_keyboard)

    # Загружаем аудио
    audio_path = await download_audio(user_url, message.from_user.id)

    if audio_path:
        # Отправляем аудио пользователю
        audio_file = FSInputFile(audio_path)
        await message.answer_audio(audio_file, reply_markup=inline.escape_keyboard_caption)

        # Удаляем временный файл после отправки
        try:
            os.remove(audio_path)
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")
    else:
        await message.answer("❌ Не удалось загрузить аудио. Попробуйте другую ссылку.",reply_markup=escape_keyboard)

    # Удаляем сообщение о загрузке
    await processing_msg.delete()







