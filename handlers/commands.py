from aiogram import Router
from aiogram import filters
from aiogram import  types
from aiogram import F
import random
from handlers.source.texts import start_message,help_text,about_text
from keyboards import inline
from aiogram.types import ReplyKeyboardRemove,FSInputFile, Message, User, Sticker, Contact, Document, PhotoSize
from urllib.parse import urlparse
import re
# import SRC
from handlers.source import texts
from keyboards.inline import escape_keyboard

from keyboards.reply import format_keyboard

command_router = Router()

@command_router.message(filters.Command("start"))
async def handler_start(s: types.Message) -> None:
    photo = FSInputFile("SRC/start2.jpg")
    await s.answer_photo(photo,caption=start_message(s.from_user),reply_markup=inline.start_keyboard, parse_mode="HTML")

@command_router.message(filters.Command("about"))
async def handler_about(a: types.Message) -> None:

    await a.answer(text=about_text,parse_mode="HTML")

@command_router.message(filters.Command("help"))
async def handler_about(h: types.Message) -> None:
    await h.answer(text=help_text, reply_markup=inline.help_keyboard, parse_mode="HTML")


TRIGGER_WORDS = ["здравствуйте", "добрый день", "доброе утро", "добрый вечер", "приветствую", "рад вас видеть", "доброго здоровья", "мое почтение", "привет", "приветик", "здорово", "хай", "хэллоу", "салют", "как дела", "чё как", "дарова", "здарова", "шалом", "привет-привет", "добро пожаловать", "мир вам", "салам алейкум", "namaste", "нихао", "мир дому твоему", "челом бью", "здравия желаю","йо","здравствуй","hi","hello"]
@command_router.message(F.text.lower().in_(TRIGGER_WORDS))
async def handler_hi(text: types.Message) -> None:
    greetings = [
        "👋 Привет! Напиши /start чтобы увидеть мои возможности",
        "Здравствуйте! ✨ Для начала работы введите /start",
        "Привет-привет! 😊 Введите /start для получения инструкций",
        "Рад вас видеть! 🌟 Начните с команды /start",
        "Приветствую! 🎬 Для доступа к функциям введите /start",
        "Доброго времени суток! 💡 Введите /start чтобы продолжить",
        "Привет! 🚀 Используйте /start для просмотра меню",
        "Здарова! 😎 Напиши /start чтобы узнать что я умею",
        "Хай! ⚡ Для старта работы введи /start",
        "Добрый день! 📌 Начните с команды /start",
        "Приветик! 🌈 Введи /start и увидишь все мои фишки",
        "Приветствую вас! 💎 Команда /start откроет главное меню",
        "👋 Дарова! Жми /start для получения информации",
        "Здравствуй! 🎯 Напиши /start чтобы начать работу",
        "Привет! 🔍 Узнай что я умею через команду /start"
    ]
    await text.answer(text=random.choice(greetings))

@command_router.message(F.sticker)
async def handler_sticker(text: types.Message):
    stickers = ["CAACAgIAAxkBAAOzaEwXDe9UAdcrvLIr9ka4tEffeMIAAtRcAAL_l2BKM4F7hnvAn-E2BA","CAACAgIAAxkBAAO1aEwXEEHTnaw_rmqgNbgO6ALrdQ8AAiRaAAJaUGFKk-Tak4_7Tag2BA","CAACAgIAAxkBAAO3aEwXEp_tIKxaSUf94QKUyp7jYsAAApBZAALY1GFKurbeu8UknXE2BA","CAACAgIAAxkBAAO5aEwXEywNfBzU6eNBllgoa-eHy20AAp5YAAIvDGBKCYbdO1qw2zo2BA","CAACAgIAAxkBAAO7aEwXFHrWSB4JjfEoylOpY_XGSBgAAv1dAAL0KWBKsErb7eNo7FI2BA","CAACAgIAAxkBAAO9aEwXFfafmW3z-NmnUwjy6qf9PakAAnlZAAIqaGFKVbQ1ypMu0N42BA","CAACAgIAAxkBAAO_aEwXFlNwZTPPm_8t_1HfZON1tboAAnNaAAJwtWFKW8ChVXuZ3ko2BA","CAACAgIAAxkBAAPBaEwXGOZFYtZg8h3KLDY3wkMKdTwAArpaAALunmhKisyIr6qxwuc2BA","CAACAgIAAxkBAAPDaEwXGZgwT30aF-lkKySVMi9XK2AAAgZZAALjmWBKG5vAPipLfuo2BA","CAACAgIAAxkBAAPFaEwXGtwYuVI0zm23QCMu8-4z4sYAArReAAIdJWhK_oyTwfJtE7s2BA","CAACAgIAAxkBAAPHaEwXG4wJt2yhYe1aA_Prlu2fMegAAp1eAAJrYWBK5gE4XU8C02Q2BA","CAACAgIAAxkBAAPJaEwXG1vJX0t7e5_vwxUYbmrolaoAAjteAAIPwWBKVHlUVG-vuFU2BA","CAACAgIAAxkBAAPLaEwXHAvEQAcUTR-CAAG7kDGbQb3YAAK1WgACAQZgSk5Q2YTbVWboNgQ","CAACAgIAAxkBAAPNaEwXHfroK4aw99GIn_O_sXv9L-cAAgphAAK5RWBKft4qfrpg9RU2BA","CAACAgIAAxkBAAPPaEwXHzG0GotsQ67Z5X1-E-p0BcwAAidtAAOn8Eu99IZh1I0pTzYE","CAACAgIAAxkBAAPRaEwXIHrmuAABAqlTonDm3Xru0dtvAAIGaQACcbTxS2Z3MjBm1jMgNgQ","CAACAgIAAxkBAAPTaEwXIG0cELLv4H2ugctGCdSE1wkAAvNhAAK-HfBLfNUk3DQ-aVk2BA","CAACAgIAAxkBAAPVaEwXIRswTB24wZr0bu-1C3pOqcgAAnt-AAKUT_FLewydwp-iTLY2BA","CAACAgIAAxkBAAPXaEwXIoC_8ZTdMn18mlV77ctnycYAAihsAAJZ0_BL44baC4-Mghc2BA"]
    await text.answer_sticker(random.choice(stickers))

@command_router.message(F.text == "MP3▶️")
async def handler_mp3(text: types.Message):
    text_mp3 = """
    🔄 <b>Конвертирую в MP3...</b>

    Ваш аудиофайл готовится! Обычно это занимает 15-30 секунд.

    📌 <i>Пока ждете:</i>
    • Проверьте громкость на устройстве
    • Убедитесь в стабильном интернет-соединении

    Статус: <code>Извлекаем аудиодорожку...</code>
    """
    await text.answer(text=text_mp3,parse_mode="HTML",reply_markup=ReplyKeyboardRemove())

@command_router.message(F.text == "MP4▶️")
async def handler_mp4(text: types.Message):
    text_mp4 = """
        🔄 <b>Конвертирую в MP4...</b>

        Ваш видеофайл готовится! Обычно это занимает 15-30 секунд.

        📌 <i>Пока ждете:</i>
        • Проверьте громкость на устройстве
        • Убедитесь в стабильном интернет-соединении

        Статус: <code>Извлекаем видеодорожку...</code>
        """
    await text.answer(text=text_mp4,parse_mode="HTML",reply_markup=ReplyKeyboardRemove())



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


@command_router.message(F.text)
async def handle_links(message: types.Message)->None:
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
    await message.answer(text=text_ans,parse_mode="HTML",reply_markup=format_keyboard)

### ЛОГИКА ДЛЯ ПОЛУЧЕНИЯ ID ###

# @command_router.message(content_types=types.ContentType.ANY)
# async def handle_id_request(message: types.Message):
#     response = "🆔 <b>Результат:</b>\n"
#
#     # 1. Обработка юзернеймов (@username)
#     if message.text and message.text.startswith('@'):
#         username = message.text[1:].split()[0]  # Извлекаем юзернейм без @
#         try:
#             user = await message.bot.get_chat(f"@{username}")
#             response += f"• Юзернейм @{username} → <code>user_id: {user.id}</code>\n"
#         except Exception as e:
#             response += f"⚠️ Не удалось найти ID для @{username}\n"
#
#     # 2. Пересланные сообщения
#     elif message.forward_from:
#         user = message.forward_from
#         response += f"• Переслано от → <code>user_id: {user.id}</code>\n"
#         if user.username:
#             response += f"  Юзернейм → @{user.username}\n"
#
#     elif message.forward_from_chat:
#         chat = message.forward_from_chat
#         response += f"• {chat.type.capitalize()} → <code>chat_id: {chat.id}</code>\n"
#         if chat.username:
#             response += f"  Юзернейм → @{chat.username}\n"
#
#     # 3. Медиафайлы
#     elif message.sticker:
#         response += f"• Стикер {message.sticker.emoji} → <code>file_id: {message.sticker.file_id}</code>\n"
#
#     elif message.content_type in ['photo', 'video', 'document']:
#         file_id = {
#             'photo': message.photo[-1].file_id,
#             'video': message.video.file_id,
#             'document': message.document.file_id
#         }[message.content_type]
#         response += f"• {message.content_type.capitalize()} → <code>file_id: {file_id}</code>\n"
#
#     # 4. Информация о текущем чате/пользователе
#     response += f"\n📌 <i>Ваш ID</i> → <code>{message.from_user.id}</code>"
#
#     await message.reply(response, parse_mode="HTML",reply_markup=inline.escape_keyboard)



