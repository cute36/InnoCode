from aiogram import  types
import aiogram
from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
import random
from keyboards import inline
from handlers.source.texts import start_message,download_prompts,get_id_prompts,help_text,about_text
from keyboards.inline import escape_keyboard, start_keyboard, escape_keyboard_caption
from aiogram.types import FSInputFile
from states import Download,ID,Sticker,Photo,UsernameStates,CircleVideo
from id_database import get_user_by_username,save_user_to_db
import os
import subprocess
import asyncio
import shutil

callback_router = Router()

@callback_router.callback_query(F.data == "start")
async def handle_cancel(callback: aiogram.types.CallbackQuery,state: FSMContext):
    await callback.answer("Начинаем...")
    await callback.message.delete()
    photo = FSInputFile("SRC/download4.png")
    await callback.message.answer_photo(photo, caption=download_prompts, parse_mode="HTML",
                                        reply_markup=escape_keyboard_caption)
    #await callback.message.edit_text(text=start_message(callback.from_user),parse_mode="HTML",reply_markup=start_keyboard)
    await state.clear()

@callback_router.callback_query(F.data == "music_pressed")
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
    await callback.message.answer(text=get_id_prompts,parse_mode="HTML",reply_markup=inline.id_keyboard)
    await state.set_state(ID.wait_id)

@callback_router.callback_query(F.data == "circle_pressed")
async def handle_circle(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Обрабатывается...")
    await callback.message.delete()
    await callback.message.answer(
        "🌀 Отправьте мне видео, и я превращу его в кружок Telegram:",
        reply_markup=inline.escape_keyboard
    )
    await state.set_state(CircleVideo.waiting_for_video)

@callback_router.callback_query(F.data == "escape_id")
async def handle_cancel(callback: aiogram.types.CallbackQuery,state: FSMContext):
    await callback.answer("Возвращаю...")
    await callback.message.delete()
    await callback.message.answer(text=get_id_prompts,parse_mode="HTML",reply_markup=inline.id_keyboard)
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

### ОБРАБОТКА СВОЕГО АЙДИ ###
@callback_router.callback_query(F.data == "user_id",ID.wait_id)
async def show_user_id(callback: types.CallbackQuery,state: FSMContext):
    user = callback.from_user

    # Форматируем ответ
    response = (
        "👤 <b>Ваши данные:</b>\n"
        f"├ 🔖 Имя: {user.full_name}\n"
        f"├ 🆔 ID: <code>{user.id}</code>\n"
        f"├ @ Юзернейм: @{user.username if user.username else 'нет'}\n"
        f"└ 🤖 Бот: {'Да' if user.is_bot else 'Нет'}"
    )

    await callback.message.edit_text(
        response,
        parse_mode="HTML",
        reply_markup=inline.escape_id  # Убираем кнопку после нажатия
    )
    await callback.answer()


#### ОБРАБОТКА СТИКЕРА#####
@callback_router.callback_query(F.data == "sticker_id")
async def request_sticker_id(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📌 Отправьте мне стикер, и я покажу его информацию:",
        reply_markup=inline.escape_id
    )
    await state.set_state(Sticker.waiting_for_sticker)
    await callback.answer()


# Обработчик стикера в состоянии ожидания
@callback_router.message(Sticker.waiting_for_sticker, F.sticker)
async def handle_sticker_input(message: types.Message, state: FSMContext):
    sticker = message.sticker

    response = (
        "📌 <b>Информация о стикере:</b>\n"
        f"├ 🆔 <b>ID:</b> <code>{sticker.file_id}</code>\n"
        f"├ 📦 <b>Набор:</b> {sticker.set_name if sticker.set_name else 'нет'}\n"
        f"├ 😀 <b>Эмодзи:</b> {sticker.emoji if sticker.emoji else 'нет'}\n"
        f"├ 📏 <b>Размер:</b> {sticker.file_size // 1024} KB\n"
        f"├ 🖼 <b>Тип:</b> {sticker.type}\n"
        f"└ 🔄 <b>Анимированный:</b> {'Да' if sticker.is_animated else 'Нет'}"
    )

    await message.reply(response, parse_mode="HTML",reply_markup=inline.escape_id)
    await state.clear()

# Обработчик не-стикера в состоянии ожидания
@callback_router.message(Sticker.waiting_for_sticker)
async def handle_non_photo_input(message: types.Message):
    # Удаляем неправильное сообщение пользователя
    try:
        await message.delete()
    except:
        pass

    # Отправляем предупреждение, которое само удалится через 5 секунд
    await message.answer(
        "⚠️ Пожалуйста, отправьте именно стикер",
        reply_markup=inline.escape_id
    )


###ИНФА ПРО ФОТКИ####


@callback_router.callback_query(F.data == "photo_id")
async def request_photo_info(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📷 Отправьте мне фото, и я покажу его информацию:",
        reply_markup=inline.escape_id
    )
    await state.set_state(Photo.waiting_for_photo)
    await callback.answer()


# Обработчик фото в состоянии ожидания
@callback_router.message(Photo.waiting_for_photo, F.photo)
async def handle_photo_input(message: types.Message, state: FSMContext):
    photo = message.photo[-1]  # Берем самое высококачественное фото

    response = (
        "📸 <b>Информация о фото:</b>\n"
        f"├ 🆔 <b>File ID:</b> <code>{photo.file_id}</code>\n"
        f"├ 📏 <b>Размер:</b> {photo.file_size // 1024} KB\n"
        f"├ 🖼 <b>Разрешение:</b> {photo.width}x{photo.height}\n"
        f"└ 📁 <b>Unique ID:</b> <code>{photo.file_unique_id}</code>"
    )

    await message.reply(response, parse_mode="HTML",reply_markup=inline.escape_id)
    await state.clear()
    # Обработчик не-фото в состоянии ожидания

@callback_router.message(Photo.waiting_for_photo)
async def handle_non_photo_input(message: types.Message):
    # Удаляем неправильное сообщение пользователя
    try:
        await message.delete()
    except:
        pass

    # Отправляем предупреждение, которое само удалится через 5 секунд
    await message.answer(
        "⚠️ Пожалуйста, отправьте именно фото\n"
        "Используйте кнопку '📎' в меню",
        reply_markup=inline.escape_id
    )

### ИНФА ЧУЖОГО ИЮЗЕРНЕМЙА####

@callback_router.callback_query(F.data == "another_id")
async def request_photo_info(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Отправьте мне юзернейм и я покажу информацию о нём:",
        reply_markup=inline.escape_id
    )
    await state.set_state(UsernameStates.waiting_for_username)
    await callback.answer()


@callback_router.message(UsernameStates.waiting_for_username, F.text)
async def handle_username_input(message: types.Message, state: FSMContext):
    username = message.text.strip().lstrip('@')  # Удаляем @ если есть

    # Сначала проверяем в базе данных
    user_from_db = get_user_by_username(username)

    if user_from_db:
        # Если пользователь найден в базе
        response = (
            "📋 <b>Информация из базы данных:</b>\n"
            f"├ 🆔 <b>ID:</b> <code>{user_from_db[0]}</code>\n"
            f"├ 📛 <b>Имя:</b> {user_from_db[2]}\n"
            f"└ @ <b>Юзернейм:</b> @{user_from_db[1]}\n\n"
            f"ℹ️ Это локальные данные из нашей базы"
        )
        await message.reply(response, parse_mode="HTML", reply_markup=inline.escape_id)
        return

    try:
        # Если нет в базе, запрашиваем у Telegram
        chat = await message.bot.get_chat(f"@{username}")

        response = (
            "👤 <b>Информация о пользователе:</b>\n"
            f"├ 🆔 <b>ID:</b> <code>{chat.id}</code>\n"
            f"├ 📛 <b>Имя:</b> {chat.full_name}\n"
            f"├ @ <b>Юзернейм:</b> @{chat.username}\n"
            f"└ 🤖 <b>Бот:</b> {'Да' if chat.is_bot else 'Нет'}\n\n"
            f"ℹ️ Эти данные получены от Telegram и могут быть не трушными..."
        )

        await message.reply(response, parse_mode="HTML", reply_markup=inline.escape_id)

        # Сохраняем пользователя в базу данных
        save_user_to_db(
            user_id=chat.id,
            username=chat.username,
            first_name=chat.full_name,
            is_bot=chat.is_bot
        )

    except Exception as e:
        await message.reply(
            f"❌ Не удалось найти пользователя @{username}\n"
            f"Ошибка: {str(e)}",
            reply_markup=inline.escape_id
        )




# Обработчик не-юзернейма в состоянии ожидания
@callback_router.message(UsernameStates.waiting_for_username)
async def handle_non_username_input(message: types.Message):
    try:
        await message.delete()
    except:
        pass

    warning = await message.answer(
        "⚠️ Пожалуйста, отправьте юзернейм (например, @username)",
        reply_markup=inline.escape_id
    )


#### ОБРАБОТЧИК В КРУЖОК #####


#@callback_router.message(CircleVideo.waiting_for_video, F.video)
# async def handle_circle_video(message: types.Message, state: FSMContext):
#     # Проверка размера видео
#     MAX_SIZE = 20 * 1024 * 1024  # 20 МБ
#     if message.video.file_size > MAX_SIZE:
#         await message.answer("❌ Видео должно быть меньше 20 МБ")
#         await state.clear()
#         return
#
#     # Пути к файлам
#     user_dir = f"downloads/{message.from_user.id}"
#     os.makedirs(user_dir, exist_ok=True)
#
#     input_path = f"{user_dir}/input.mp4"
#     output_path = f"{user_dir}/circle.mp4"
#     mask_path = "static/circle_mask.png"  # Ваша маска
#
#     try:
#         # 1. Скачиваем видео
#         await message.answer("📥 Загружаю видео...")
#         await message.bot.download(message.video.file_id, destination=input_path)
#
#         # 2. Обрабатываем видео в кружок
#         await message.answer("🌀 Создаю кружок...")
#         subprocess.run([
#             'ffmpeg', '-y',
#             '-i', input_path,
#             '-i', mask_path,
#             '-filter_complex',
#             '[0]scale=512:512:force_original_aspect_ratio=increase,'
#             'crop=512:512[vid];'
#             '[vid][1]alphamerge[out]',
#             '-map', '[out]',
#             '-map', '0:a?',
#             '-c:v', 'libx264',
#             '-preset', 'fast',
#             '-crf', '20',
#             '-c:a', 'aac',
#             '-movflags', '+faststart',
#             '-pix_fmt', 'yuva420p',  # Важно для прозрачности
#             output_path
#         ], check=True)
#
#         # 3. Отправляем как кружок
#         await message.answer_video_note(
#             video_note=FSInputFile(output_path),
#             duration=message.video.duration,
#             length=512  # Размер кружка (512x512)
#         )
#         await message.answer("Ваш кружок готов!👆",reply_markup=escape_keyboard)
#
#     except subprocess.CalledProcessError as e:
#         await message.answer("❌ Ошибка обработки видео",reply_markup=escape_keyboard)
#     except Exception as e:
#         await message.answer(f"❌ Ошибка: {str(e)}",reply_markup=escape_keyboard)
#     finally:
#         # Удаляем временные файлы
#         for file in [input_path, output_path]:
#             try:
#                 if os.path.exists(file):
#                     os.remove(file)
#             except:
#                 pass
#
#     await state.clear()
@callback_router.message(CircleVideo.waiting_for_video, F.video)
async def handle_circle_video(message: types.Message, state: FSMContext):
    MAX_SIZE = 20 * 1024 * 1024  # 20 МБ
    if message.video.file_size > MAX_SIZE:
        await message.answer("❌ Видео должно быть меньше 20 МБ")
        await state.clear()
        return

    user_dir = f"downloads/{message.from_user.id}"
    os.makedirs(user_dir, exist_ok=True)
    input_path = f"{user_dir}/input.mp4"
    output_path = f"{user_dir}/circle.mp4"
    mask_path = "static/circle_mask.png"

    try:
        # 1. Скачиваем видео
        await message.answer("📥 Загружаю видео...")
        await message.bot.download(message.video.file_id, destination=input_path)

        # 2. Обрабатываем видео в кружок
        await message.answer("🌀 Создаю кружок...")
        subprocess.run([
            'ffmpeg', '-y',
            '-i', input_path,
            '-i', mask_path,
            '-filter_complex',
            '[0]scale=512:512:force_original_aspect_ratio=increase,'
            'crop=512:512[vid];'
            '[vid][1]alphamerge[out]',
            '-map', '[out]',
            '-map', '0:a?',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '20',
            '-c:a', 'aac',
            '-movflags', '+faststart',
            '-pix_fmt', 'yuva420p',
            output_path
        ], check=True)

        # 3. Отправляем кружок
        await message.answer_video_note(
            video_note=FSInputFile(output_path),
            duration=message.video.duration,
            length=512
        )
        await message.answer("✅ Ваш кружок готов! 👆", reply_markup=escape_keyboard)

    except subprocess.CalledProcessError as e:
        await message.answer("❌ Ошибка обработки видео", reply_markup=escape_keyboard)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}", reply_markup=escape_keyboard)
    finally:
        # Удаляем файлы в любом случае (даже если была ошибка)
        for file_path in [input_path, output_path]:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Удалён временный файл: {file_path}")
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")

    await state.clear()

@callback_router.message(CircleVideo.waiting_for_video)
async def handle_non_video_input(message: types.Message):
    """
    Ловит всё, что не является видео, когда бот ждёт видео для кружка.
    """
    # Удаляем сообщение пользователя (если возможно)
    try:
        await message.delete()
    except:
        pass

    # Отправляем предупреждение с кнопкой "Отмена"
    warning = await message.answer(
        "⚠️ Пожалуйста, отправьте именно <b>видео</b> (не фото, не файл).\n"
        "Используйте кнопку \"📎\" в меню Telegram.",
        reply_markup=escape_keyboard

    )

    # Удаляем предупреждение через 10 секунд
    await asyncio.sleep(10)
    try:
        await warning.delete()
    except:
        pass