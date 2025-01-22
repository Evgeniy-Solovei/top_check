from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def get_main_keyboard():
    # Создаем кнопки
    buttons = [
        KeyboardButton(text="Подарки"),
        KeyboardButton(text="Баланс"),
        KeyboardButton(text="Продвижение"),
    ]
    builder = ReplyKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
