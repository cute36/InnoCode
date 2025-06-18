import yt_dlp
import os
from aiogram.types import FSInputFile
from datetime import datetime

async def download_audio(url: str, user_id: int) -> str:
    """
    Загружает аудио с SoundCloud и возвращает путь к файлу.
    """
    # Настройки для yt-dlp (загрузка аудио в формате MP3)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'downloads/{user_id}/%(title)s.%(ext)s',
        'quiet': True,
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