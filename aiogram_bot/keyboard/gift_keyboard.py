from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def gifts_keyboard():
    # Создаем кнопки
    buttons = [
        KeyboardButton(text="COMFORT"),
        KeyboardButton(text="PREMIUM"),
        KeyboardButton(text="EXCLUSIVE"),
        KeyboardButton(text="Назад"),
    ]
    builder = ReplyKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
