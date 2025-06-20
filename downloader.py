import yt_dlp
import os
import random
from proxy_manager import proxy_manager
from datetime import datetime, timedelta
from constants import USER_AGENTS
import asyncio
import hashlib
import sqlite3
import shutil
from apscheduler.schedulers.background import BackgroundScheduler

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

#### РАБОЧАЯ СНАЧАЛА ТРЕК ПотОМ ПРОКСИ

#async def download_audio(url: str, user_id: int, retry_count: int = 2) -> str:
    # """Улучшенная загрузка аудио: сначала без прокси, затем с прокси."""
    # ydl_opts_base = {
    #     'format': 'bestaudio/best',
    #     'postprocessors': [{
    #         'key': 'FFmpegExtractAudio',
    #         'preferredcodec': 'mp3',
    #         'preferredquality': '192',
    #     }],
    #     'outtmpl': f'downloads/{user_id}/%(title)s.%(ext)s',
    #     'quiet': True,
    #     'http_headers': {
    #         'User-Agent': random.choice(USER_AGENTS),
    #         'Referer': 'https://soundcloud.com/',
    #     },
    #     'socket_timeout': 15,
    #     'extract_flat': False
    # }
    #
    # os.makedirs(f'downloads/{user_id}', exist_ok=True)
    # audio_path = None
    #
    # for attempt in range(retry_count):
    #     ydl_opts = ydl_opts_base.copy()
    #
    #     # Чередуем стратегии: сначала без прокси, потом с прокси
    #     if attempt >= 1:  # На второй попытке используем прокси
    #         proxy = proxy_manager.get_working_proxy()
    #         if proxy:
    #             ydl_opts['proxy'] = proxy
    #             print(f"Attempt {attempt + 1}: Using proxy {proxy}")
    #         else:
    #             print("No working proxy available, skipping proxy attempt")
    #             continue
    #
    #     try:
    #         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #             info = await asyncio.to_thread(ydl.extract_info, url, download=True)
    #             filename = ydl.prepare_filename(info)
    #             audio_filename = filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')
    #
    #             # Добавляем timestamp к имени файла
    #             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #             new_path = f"{audio_filename[:-4]}_{timestamp}.mp3"
    #             os.rename(audio_filename, new_path)
    #             audio_path = new_path
    #             break  # Успешная загрузка
    #
    #     except Exception as e:
    #         print(f"Attempt {attempt + 1} failed: {str(e)}")
    #         if attempt < retry_count - 1:
    #             wait_time = min((attempt + 1) * 3, 6)  # Максимум 10 сек
    #             print(f"Waiting {wait_time} seconds before retry...")
    #             await asyncio.sleep(wait_time)
    #
    #         # Удаляем частично загруженные файлы
    #         if audio_path and os.path.exists(audio_path):
    #             try:
    #                 os.remove(audio_path)
    #             except:
    #                 pass
    #
    # return audio_path

### ЗАГРУЗКА С КЭШИРОВАНИЕМ #######


# Инициализация базы данных для кэша
def init_cache_db():
    conn = sqlite3.connect('cache.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS audio_cache
                     (url_hash TEXT PRIMARY KEY,
                      url TEXT NOT NULL,
                      file_path TEXT NOT NULL,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()


init_cache_db()


def get_url_hash(url: str) -> str:
    """Генерирует хэш URL для использования в качестве ключа кэша"""
    return hashlib.md5(url.encode('utf-8')).hexdigest()


def get_cached_audio(url: str) -> str | None:
    """Проверяет наличие аудио в кэше и возвращает путь к файлу"""
    url_hash = get_url_hash(url)
    conn = sqlite3.connect('cache.db')
    cursor = conn.cursor()

    cursor.execute('SELECT file_path FROM audio_cache WHERE url_hash = ?', (url_hash,))
    result = cursor.fetchone()
    conn.close()

    if result and os.path.exists(result[0]):
        return result[0]
    return None


def save_to_cache(url: str, file_path: str):
    """Сохраняет информацию о загруженном аудио в кэш"""
    url_hash = get_url_hash(url)
    conn = sqlite3.connect('cache.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT OR REPLACE INTO audio_cache (url_hash, url, file_path)
        VALUES (?, ?, ?)
        ''', (url_hash, url, file_path))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при сохранении в кэш: {e}")
    finally:
        conn.close()


def cleanup_old_cache(days_to_keep: int = 1, max_cache_size_mb: int = 1024):
    """Очистка старых кэшированных файлов и записей в БД"""
    try:
        conn = sqlite3.connect('cache.db')
        cursor = conn.cursor()

        # Удаляем записи старше days_to_keep дней
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cursor.execute('SELECT file_path FROM audio_cache WHERE created_at < ?',
                       (cutoff_date.strftime('%Y-%m-%d %H:%M:%S'),))
        old_files = cursor.fetchall()

        # Удаляем файлы
        for file_record in old_files:
            file_path = file_record[0]
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")

        # Удаляем записи из БД
        cursor.execute('DELETE FROM audio_cache WHERE created_at < ?',
                       (cutoff_date.strftime('%Y-%m-%d %H:%M:%S'),))

        # Проверяем размер кэша и удаляем самые старые файлы, если превышен лимит
        cache_dir = "downloads/cache"
        if os.path.exists(cache_dir):
            total_size = sum(os.path.getsize(os.path.join(cache_dir, f)) for f in os.listdir(cache_dir)
                             if os.path.isfile(os.path.join(cache_dir, f))) / (1024 * 1024)

            if total_size > max_cache_size_mb:
                # Получаем список файлов отсортированный по дате создания (сначала старые)
                cursor.execute('SELECT file_path FROM audio_cache ORDER BY created_at ASC')
                all_files = cursor.fetchall()

                while total_size > max_cache_size_mb * 0.9 and all_files:  # Удаляем до 90% от лимита
                    file_to_remove = all_files.pop(0)[0]
                    try:
                        if os.path.exists(file_to_remove):
                            file_size = os.path.getsize(file_to_remove) / (1024 * 1024)
                            os.remove(file_to_remove)
                            total_size -= file_size
                            cursor.execute('DELETE FROM audio_cache WHERE file_path = ?', (file_to_remove,))
                    except Exception as e:
                        print(f"Ошибка при удалении файла {file_to_remove}: {e}")

        conn.commit()
        print(f"Cache cleanup completed. Removed {len(old_files)} old entries.")

    except Exception as e:
        print(f"Ошибка при очистке кэша: {e}")
    finally:
        conn.close()


# Инициализация планировщика для очистки кэша
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_old_cache, 'interval', days=1,
                  kwargs={'days_to_keep': 1, 'max_cache_size_mb': 1024})
scheduler.start()


async def download_audio(url: str, user_id: int, retry_count: int = 2) -> str:
    """Улучшенная загрузка аудио с кэшированием"""
    # Сначала проверяем кэш
    cached_path = get_cached_audio(url)
    if cached_path:
        print(f"Используем кэшированную версию для {url}")
        # Создаем копию файла для пользователя
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_dir = f'downloads/{user_id}'
        os.makedirs(user_dir, exist_ok=True)
        new_path = f"{user_dir}/{os.path.basename(cached_path)[:-4]}_{timestamp}.mp3"
        shutil.copy2(cached_path, new_path)
        return new_path

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

        if attempt >= 1:
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

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_path = f"{audio_filename[:-4]}_{timestamp}.mp3"
                os.rename(audio_filename, new_path)
                audio_path = new_path

                # Сохраняем в кэш оригинальную версию (без user_id в пути)
                cache_dir = "downloads/cache"
                os.makedirs(cache_dir, exist_ok=True)
                cache_path = f"{cache_dir}/{os.path.basename(audio_filename[:-4])}.mp3"
                shutil.copy2(new_path, cache_path)
                save_to_cache(url, cache_path)

                break

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < retry_count - 1:
                wait_time = min((attempt + 1) * 3, 6)
                print(f"Waiting {wait_time} seconds before retry...")
                await asyncio.sleep(wait_time)

            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except:
                    pass

    return audio_path