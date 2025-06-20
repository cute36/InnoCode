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
from constants import USER_AGENTS
import yt_dlp



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

##РАБОЧИЙ ХЭНДЛ
#@command_router.message(F.text, Download.wait_link)
#async def handle_links(message: types.Message, state: FSMContext) -> None:
    # user_url = message.text.strip()
    #
    # if not is_valid_url(user_url):
    #     await message.answer(
    #         "❌ Это не похоже на валидную ссылку. Пример правильного формата:\nhttps://soundcloud.com/...")
    #     return
    #
    # if not is_supported_platform(user_url):
    #     await message.answer("⚠️ Этот сервис пока не поддерживается. Работаем с SoundCloud.")
    #     return
    #
    # # Уведомление о начале загрузки
    # text_ans = """
    # 🔎 <b>Загружаю аудио...</b>
    #
    # ⏳ Это может занять от 15 секунд до 2 минут
    # ⌛ Пожалуйста, подождите...
    # """
    # processing_msg = await message.answer(text=text_ans, parse_mode="HTML",reply_markup=escape_keyboard)
    #
    # # Загружаем аудио
    # audio_path = await download_audio(user_url, message.from_user.id)
    #
    # if audio_path:
    #     # Отправляем аудио пользователю
    #     audio_file = FSInputFile(audio_path)
    #     await message.answer_audio(audio_file, reply_markup=inline.escape_keyboard_caption)
    #
    #     # Удаляем временный файл после отправки
    #     try:
    #         os.remove(audio_path)
    #     except Exception as e:
    #         print(f"Ошибка при удалении файла: {e}")
    # else:
    #     await message.answer("❌ Не удалось загрузить аудио. Попробуйте другую ссылку.",reply_markup=escape_keyboard)
    #
    # # Удаляем сообщение о загрузке
    # await processing_msg.delete()

### ПРОКСИ ХЭНДЛ НЕ УВЕРЕН ЧТО ЗАГРУЗИТ ССЫЛКУ

#@command_router.message(F.text, Download.wait_link)
# async def handle_links(message: types.Message, state: FSMContext):
#     user_url = message.text.strip()
#
#     processing_msg = await message.answer("🔎 Начинаю загрузку... Это может занять несколько минут",reply_markup=escape_keyboard)
#
#     try:
#         audio_path = await download_audio(user_url, message.from_user.id)
#
#         if audio_path:
#             await message.answer_audio(
#                 FSInputFile(audio_path),
#             )
#             await message.answer(text="Вот ваш аудиофайл!👆",reply_markup=escape_keyboard)
#             try:
#                 os.remove(audio_path)
#             except Exception as e:
#                 print(f"File deletion error: {e}")
#         else:
#             await message.answer(
#                 "❌ Не удалось загрузить аудио после нескольких попыток. "
#                 "Попробуйте позже или другую ссылку.",
#                 reply_markup=escape_keyboard
#             )
#
#     except Exception as e:
#         await message.answer(
#             "⚠️ Произошла непредвиденная ошибка. Администратор уже уведомлен.",
#             reply_markup=escape_keyboard
#         )
#         logger.error(f"Critical error for {user_url}: {str(e)}")
#     finally:
#         await processing_msg.delete()


async def get_track_info(url: str):
    """Получение информации о треке без загрузки"""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'http_headers': {
            'User-Agent': random.choice(USER_AGENTS),
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Неизвестно'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail'),
                'uploader': info.get('uploader', 'Неизвестный исполнитель')
            }
    except Exception as e:
        logger.error(f"Error getting track info: {e}")
        return None


@command_router.message(F.text, Download.wait_link)
async def handle_links(message: types.Message, state: FSMContext):
    user_url = message.text.strip()

    # Проверка URL
    if not is_valid_url(user_url):
        await message.answer("❌ Это не похоже на валидную ссылку.")
        return

    if not is_supported_platform(user_url):
        await message.answer("⚠️ Поддерживается только SoundCloud.")
        return

    # Получаем информацию о треке
    track_info = await get_track_info(user_url)
    if not track_info:
        await message.answer("❌ Не удалось получить информацию о треке.")
        return

    # Форматируем длительность
    duration = int(track_info['duration'])
    minutes, seconds = divmod(duration, 60)
    formatted_duration = f"{minutes}:{seconds:02d}"

    # Отправляем предпросмотр
    preview_msg = (
        "🎵 <b>Информация о треке:</b>\n"
        f"├ <b>Название:</b> {track_info['title']}\n"
        f"├ <b>Исполнитель:</b> {track_info['uploader']}\n"
        f"└ <b>Длительность:</b> {formatted_duration}\n\n"
        "🔎 Начинаю загрузку, это может занять пару минут..."
    )

    if track_info['thumbnail']:
        try:
            await message.answer_photo(
                track_info['thumbnail'],
                caption=preview_msg,
                parse_mode="HTML",
            )
        except:
            await message.answer(preview_msg, parse_mode="HTML")
    else:
        await message.answer(preview_msg, parse_mode="HTML")

    # Загрузка аудио
    try:
        audio_path = await download_audio(user_url, message.from_user.id)
        if audio_path:
            await message.answer_audio(
                FSInputFile(audio_path),
                title=track_info['title'],
                performer=track_info['uploader']
            )
            await message.answer("✅ Готово! Вот твой тречок!👆", reply_markup=inline.escape_keyboard)
        else:
            await message.answer("❌ Не удалось загрузить аудио.", reply_markup=inline.escape_keyboard)
    except ValueError as e:
        await message.answer(f"❌ {str(e)}", reply_markup=inline.escape_keyboard)
    except Exception as e:
        logger.error(f"Download failed: {e}")
        await message.answer("⚠️ Произошла ошибка при загрузке.", reply_markup=inline.escape_keyboard   )
    finally:
        # Удаление временного файла
        try:
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
        except Exception as e:
            logger.error(f"Error deleting file: {e}")





