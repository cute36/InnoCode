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
from states import Download,ID,Sticker,Photo,UsernameStates
from id_database import get_user_by_username,save_user_to_db

callback_router = Router()

@callback_router.callback_query(F.data == "start")
async def handle_cancel(callback: aiogram.types.CallbackQuery,state: FSMContext):
    await callback.answer("Начинаем...")
    await callback.message.edit_text(text=start_message(callback.from_user),parse_mode="HTML",reply_markup=start_keyboard)
    await state.clear()

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
    await callback.message.answer(text=get_id_prompts,parse_mode="HTML",reply_markup=inline.id_keyboard)
    await state.set_state(ID.wait_id)

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


