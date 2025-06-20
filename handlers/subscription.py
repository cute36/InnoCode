from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import  CallbackQuery
from aiogram.types import FSInputFile, Message
from handlers.source.texts import start_message
from keyboards import inline
from id_database import add_user
from aiogram.fsm.context import FSMContext
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
                    await event.answer("❌ Сначала подпишитесь на канал!", show_alert=True,reply_markup=inline.subscription_keyboard)
                else:
                    await event.answer("❌ Сначала подпишитесь на канал!",reply_markup=inline.subscription_keyboard)
                return
        except Exception as e:
            print(f"Subscription check error: {e}")
            await event.answer("⚠️ Ошибка проверки подписки",reply_markup=inline.subscription_keyboard)
            return

        return await handler(event, data)


# def subscription_keyboard():
#     builder = InlineKeyboardBuilder()
#     builder.button(text="🔔 Подписаться", url=CHANNEL_LINK)
#     builder.button(text="✅ Проверить подписку", callback_data="check_sub")
#     builder.adjust(1)
#     return builder.as_markup()


@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot,state: FSMContext):
    text= """
    📢 <b>Для использования бота подпишитесь на канал!!!</b>
    👉 <a href="https://t.me/uroduzhir">вандалы325</a> 👈
    """
    try:
        # Добавляем пользователя в БД (без is_bot)
        add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )

        member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            photo = FSInputFile("SRC/start2.jpg")
            await message.answer_photo(photo,caption=start_message(message.from_user),reply_markup=inline.start_keyboard, parse_mode="HTML")
            return
    except Exception as e:
        print(f"Error: {e}")
        # Повторно добавляем в БД в случае ошибки
        add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )


    await message.answer(
        text=text,
        reply_markup=inline.subscription_keyboard,
        parse_mode="HTML"
    )
    await state.clear()



@router.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery, bot: Bot):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, callback.from_user.id)
        if member.status in ['member', 'administrator', 'creator']:
            await callback.message.edit_text(
                "✅ Спасибо за подписку! Теперь вам доступны все команды.",
                reply_markup=inline.start
            )
            return
    except Exception as e:
        print(f"Error: {e}")

    await callback.answer("❌ Вы ещё не подписались!", show_alert=True,reply_markup=inline.subscription_keyboard)


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
        reply_markup=inline.subscription_keyboard
    )


# Защищённая команда
@router.message(Command("secret"))
async def secret_command(message: Message):
    await message.answer("🔐 Это секретная команда для подписчиков!")