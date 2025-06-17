from aiogram import Router
from aiogram import filters
from aiogram import  types
from aiogram import F
import random
from handlers.source.texts import start_message,help_text,about_text
from keyboards import inline
from functools import wraps
from aiogram.types import ReplyKeyboardRemove,FSInputFile, Message, User, Sticker, Contact, Document, PhotoSize
from urllib.parse import urlparse
import re
from states import Download,ID
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
# import SRC
from handlers.source import texts
from keyboards.inline import escape_keyboard



command_router = Router()



#@command_router.message(filters.Command("start"))
async def handler_start(s: types.Message) -> None:
    photo = FSInputFile("SRC/start2.jpg")
    await s.answer_photo(photo,caption=start_message(s.from_user),reply_markup=inline.start_keyboard, parse_mode="HTML")

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

# @command_router.message(F.text == "MP3▶️",Download.wait_format)
# async def handler_mp3(text: types.Message,state: FSMContext):
#     text_mp3 = """
#     🔄 <b>Конвертирую в MP3...</b>
#
#     Ваш аудиофайл готовится! Обычно это занимает 15-30 секунд.
#
#     📌 <i>Пока ждете:</i>
#     • Проверьте громкость на устройстве
#     • Убедитесь в стабильном интернет-соединении
#
#     Статус: <code>Извлекаем аудиодорожку...</code>
#     """
#     await text.answer(text=text_mp3,parse_mode="HTML",reply_markup=ReplyKeyboardRemove())
#     await state.set_state(Download.wait_file)

# @command_router.message(F.text == "MP4▶️",Download.wait_format)
# async def handler_mp4(text: types.Message,state: FSMContext):
#     text_mp4 = """
#         🔄 <b>Конвертирую в MP4...</b>
#
#         Ваш видеофайл готовится! Обычно это занимает 15-30 секунд.
#
#         📌 <i>Пока ждете:</i>
#         • Проверьте громкость на устройстве
#         • Убедитесь в стабильном интернет-соединении
#
#         Статус: <code>Извлекаем видеодорожку...</code>
#         """
#     await text.answer(text=text_mp4,parse_mode="HTML",reply_markup=ReplyKeyboardRemove())
#     await state.set_state(Download.wait_file)



### ЛОГИКА ПРОВЕРКИ ВАЛИДНОСТИ ССЫЛОК ###


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False

def is_supported_platform(url: str) -> bool:
    supported_domains = [
        'youtube.com',
        'youtu.be',
        'tiktok.com',
        'instagram.com',
        'vk.com',
        'dzen.ru'
        'soundcloud.com'
    ]
    domain = urlparse(url).netloc.lower()
    return any(d in domain for d in supported_domains)


@command_router.message(F.text,Download.wait_link)
async def handle_links(message: types.Message,state: FSMContext)->None:
    user_url = message.text.strip()

    if not is_valid_url(user_url):
        await message.answer(
            "❌ Это не похоже на валидную ссылку. Пример правильного формата:\nhttps://youtube.com/watch?v=...")
        return

    if not is_supported_platform(user_url):
        await message.answer("⚠️ Этот сервис пока не поддерживается. Работаем с:\nYouTube, TikTok, Soundcloud, VK, Instagram ")
        return

    # ЕСЛИ ВАЩЕ ВСЕ КАЙФ
    valid_url = user_url #ГОТОВАЯ ССЫЛКА
    text_ans = """
🔎 <b>Анализирую ссылку...</b>
    <b>Выберите формат:</b>
    - MP3▶️
    - MP4▶️
    """
    await state.set_state(Download.wait_format)
    await message.answer(text=text_ans,parse_mode="HTML",reply_markup=inline.format_keyboard)







