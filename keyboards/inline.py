from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

CHANNEL_LINK = "https://t.me/uroduzhir"  # Ссылка

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
             InlineKeyboardButton(text="Помощь🙋‍♂️",callback_data="help_pressed"),
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

subscription_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="ПОДПИСАТЬСЯ🔔",url=CHANNEL_LINK)
        ],
        [
            InlineKeyboardButton(text="Проверить подписку✅",callback_data="check_sub")
        ]
    ]
)
format_keyboard =InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="▶️MP4",callback_data="mp4"),
            InlineKeyboardButton(text="▶️MP3",callback_data="mp3")
        ],
        [
            InlineKeyboardButton(text="Назад❌",callback_data="escape_caption_pressed")
        ]

    ]
)

id_keyboard =InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="МОЙ🆔", callback_data="user_id"),
            InlineKeyboardButton(text="СТИКЕР🆔",callback_data="sticker_id"),
            InlineKeyboardButton(text="ФОТО🆔",callback_data="photo_id")
        ],
        [
            InlineKeyboardButton(text="ЧУЖОЙ🆔",callback_data="another_id")
        ],
        [
            InlineKeyboardButton(text="Назад❌",callback_data="escape_caption_pressed")
        ]
    ]

)
escape_id=InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад❌",callback_data="escape_id")
        ]
    ]
)

start=InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Начать!",callback_data="start")
        ]
    ]
)
