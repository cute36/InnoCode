from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup


help_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🛠️Поддержка🛠️",url="https://t.me/vandal_325")
        ]
    ]
)

start_keyboard = InlineKeyboardMarkup(
     inline_keyboard=[
         [
             InlineKeyboardButton(text="️▶️Скачать видео",callback_data="download_pressed"),
             InlineKeyboardButton(text="🆔Получить ID",callback_data="id_pressed")
         ]

     ]
 )


escape_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад❌",callback_data="escape_pressed")
        ]
    ]
)