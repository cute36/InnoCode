from aiogram import Bot, types, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove,FSInputFile, Message, User, Sticker, Contact, Document, PhotoSize
from handlers.source.texts import start_message,help_text,about_text
from keyboards import inline
router = Router()

# Настройки канала
CHANNEL_ID = -1001967423322  # Замените на реальный ID канала
CHANNEL_USERNAME = "@uroduzhir"  # Юзернейм канала
CHANNEL_LINK = "https://t.me/uroduzhir"  # Ссылка


class SubscriptionMiddleware:
    async def __call__(self, handler, event: Message | CallbackQuery, data):
        # Пропускаем команду start и проверку подписки
        if (isinstance(event, Message) and event.text == "/start") or \
                (isinstance(event, CallbackQuery) and event.data == "check_sub"):
            return await handler(event, data)

        bot: Bot = data['bot']
        user_id = event.from_user.id

        try:
            member = await bot.get_chat_member(CHANNEL_ID, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                if isinstance(event, CallbackQuery):
                    await event.answer("❌ Сначала подпишитесь на канал!", show_alert=True)
                else:
                    await event.answer("❌ Сначала подпишитесь на канал!")
                return
        except Exception as e:
            print(f"Subscription check error: {e}")
            await event.answer("⚠️ Ошибка проверки подписки")
            return

        return await handler(event, data)


# def subscription_keyboard():
#     builder = InlineKeyboardBuilder()
#     builder.button(text="🔔 Подписаться", url=CHANNEL_LINK)
#     builder.button(text="✅ Проверить подписку", callback_data="check_sub")
#     builder.adjust(1)
#     return builder.as_markup()


@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            photo = FSInputFile("SRC/start2.jpg")
            await message.answer_photo(photo,caption=start_message(message.from_user),reply_markup=inline.start_keyboard, parse_mode="HTML")
            return
    except Exception as e:
        print(f"Error: {e}")

    await message.answer(
        f"Для использования бота подпишитесь на канал {CHANNEL_USERNAME}",
        reply_markup=inline.subscription_keyboard
    )


@router.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery, bot: Bot):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, callback.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            await callback.message.edit_text(
                "✅ Спасибо за подписку! Теперь вам доступны все команды.",
                reply_markup=None
            )
            return
    except Exception as e:
        print(f"Error: {e}")

    await callback.answer("❌ Вы ещё не подписались!", show_alert=True)


@router.message(F.text == "Проверить доступ")
@router.message(Command("check"))
async def check_access(message: Message, bot: Bot):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            await message.answer("✅ Доступ разрешён!")
            return
    except Exception as e:
        print(f"Error: {e}")

    await message.answer(
        "❌ Доступ запрещён. Подпишитесь на канал:",
        reply_markup=subscription_keyboard()
    )


# Защищённая команда
@router.message(Command("secret"))
async def secret_command(message: Message):
    await message.answer("🔐 Это секретная команда для подписчиков!")