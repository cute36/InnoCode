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
             InlineKeyboardButton(text="🆔Получить ID",callback_data="id_pressed"),
         ],
         [
             InlineKeyboardButton(text="🖐Наш канал",url="https://t.me/uroduzhir")
         ],
         [
             InlineKeyboardButton(text="Помошь🙋‍♂️",callback_data="help_pressed"),
             InlineKeyboardButton(text="О проекте❓",callback_data="about_pressed"),
             InlineKeyboardButton(text="Отзыв🙌",url="https://t.me/vandal_325")
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

escape_keyboard_caption = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад❌",callback_data="escape_caption_pressed")
        ]
    ]
)