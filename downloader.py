import yt_dlp
import os
import random
import time
from proxy_manager import proxy_manager
from aiogram.types import FSInputFile
from datetime import datetime
from constants import USER_AGENTS
import asyncio


#async def download_audio(url: str, user_id: int, retry_count: int = 3) -> str:
    # """Улучшенная функция загрузки с обработкой ошибок соединения"""
    #
    # for attempt in range(retry_count):
    #     ydl_opts = {
    #         'format': 'bestaudio/best',
    #         'postprocessors': [{
    #             'key': 'FFmpegExtractAudio',
    #             'preferredcodec': 'mp3',
    #             'preferredquality': '192',
    #         }],
    #         'outtmpl': f'downloads/{user_id}/%(title)s.%(ext)s',
    #         'quiet': True,
    #         'http_headers': {
    #             'User-Agent': random.choice(USER_AGENTS),
    #             'Referer': 'https://soundcloud.com/',
    #             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #             'Accept-Language': 'en-US,en;q=0.5'
    #         },
    #         'socket_timeout': 30,
    #         'extract_flat': False
    #     }
    #
    #     # Чередуем использование прокси и прямого соединения
    #     if attempt % 2 == 0:
    #         proxy = proxy_manager.get_working_proxy()
    #         if proxy:
    #             ydl_opts['proxy'] = proxy
    #             print(f"Attempt {attempt + 1}: Using proxy {proxy}")
    #         else:
    #             print(f"Attempt {attempt + 1}: No proxy available, trying direct connection")
    #     else:
    #         print(f"Attempt {attempt + 1}: Trying direct connection")
    #         ydl_opts.pop('proxy', None)
    #
    #     try:
    #         os.makedirs(f'downloads/{user_id}', exist_ok=True)
    #
    #         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #             info = ydl.extract_info(url, download=True)
    #             filename = ydl.prepare_filename(info)
    #             audio_filename = filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')
    #
    #             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #             new_path = f"{audio_filename[:-4]}_{timestamp}.mp3"
    #             os.rename(audio_filename, new_path)
    #
    #             return new_path
    #
    #     except Exception as e:
    #         print(f"Attempt {attempt + 1} failed: {str(e)}")
    #         if attempt < retry_count - 1:
    #             wait_time = (attempt + 1) * 5  # Увеличиваем время ожидания
    #             print(f"Waiting {wait_time} seconds before retry...")
    #             time.sleep(wait_time)
    #         continue
    #
    # return None

async def download_audio(url: str, user_id: int, retry_count: int = 2) -> str:
    """Улучшенная загрузка аудио: сначала без прокси, затем с прокси."""
    ydl_opts_base = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'downloads/{user_id}/%(title)s.%(ext)s',
        'quiet': True,
        'http_headers': {
            'User-Agent': random.choice(USER_AGENTS),
            'Referer': 'https://soundcloud.com/',
        },
        'socket_timeout': 15,
        'extract_flat': False
    }

    os.makedirs(f'downloads/{user_id}', exist_ok=True)
    audio_path = None

    for attempt in range(retry_count):
        ydl_opts = ydl_opts_base.copy()

        # Чередуем стратегии: сначала без прокси, потом с прокси
        if attempt >= 1:  # На второй попытке используем прокси
            proxy = proxy_manager.get_working_proxy()
            if proxy:
                ydl_opts['proxy'] = proxy
                print(f"Attempt {attempt + 1}: Using proxy {proxy}")
            else:
                print("No working proxy available, skipping proxy attempt")
                continue

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, url, download=True)
                filename = ydl.prepare_filename(info)
                audio_filename = filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')

                # Добавляем timestamp к имени файла
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_path = f"{audio_filename[:-4]}_{timestamp}.mp3"
                os.rename(audio_filename, new_path)
                audio_path = new_path
                break  # Успешная загрузка

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < retry_count - 1:
                wait_time = min((attempt + 1) * 3, 6)  # Максимум 10 сек
                print(f"Waiting {wait_time} seconds before retry...")
                await asyncio.sleep(wait_time)

            # Удаляем частично загруженные файлы
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except:
                    pass

    return audio_path