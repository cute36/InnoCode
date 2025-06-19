import yt_dlp
import os
from aiogram.types import FSInputFile
from datetime import datetime
import random
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
]
#async def download_audio(url: str, user_id: int) -> str:
    # """
    # Загружает аудио с SoundCloud и возвращает путь к файлу.
    # """
    # # Настройки для yt-dlp (загрузка аудио в формате MP3)
    # ydl_opts = {
    #      'format': 'bestaudio/best',
    #      'postprocessors': [{
    #          'key': 'FFmpegExtractAudio',
    #          'preferredcodec': 'mp3',
    #          'preferredquality': '192',
    #      }],
    #      'outtmpl': f'downloads/{user_id}/%(title)s.%(ext)s',
    #      'quiet': True,
    #  }
    #
    #
    # try:
    #     # Создаем папку для загрузок, если её нет
    #     os.makedirs(f'downloads/{user_id}', exist_ok=True)
    #
    #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #         info = ydl.extract_info(url, download=True)
    #         filename = ydl.prepare_filename(info)
    #         audio_filename = filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')
    #
    #     return audio_filename
    # except Exception as e:
    #     print(f"Ошибка при загрузке аудио: {e}")
    #     return None


async def download_audio(url: str, user_id: int) -> str:
    """Загружает аудио с SoundCloud и возвращает путь к файлу."""

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'downloads/{user_id}/%(title)s.%(ext)s',
        'quiet': True,
        'http_headers': {
            'User-Agent': random.choice(USER_AGENTS),  # Случайный выбор User-Agent
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://soundcloud.com/'
        },
        'retries': 3,  # Количество попыток при ошибках
        'socket_timeout': 30,  # Таймаут соединения
        'extract_flat': False
    }

    try:
        # Создаем папку для загрузок, если её нет
        os.makedirs(f'downloads/{user_id}', exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            audio_filename = filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')

        return audio_filename

    except Exception as e:
        print(f"Ошибка при загрузке аудио: {e}")
        return None