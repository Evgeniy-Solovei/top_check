from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def promotion_keyboard():
    buttons = [
        KeyboardButton(text="Реф.ссылка"),
        KeyboardButton(text="Сгенерировать"),
        KeyboardButton(text="Статистика"),
        KeyboardButton(text="Назад"),  # Кнопка для возврата в главное меню
    ]
    builder = ReplyKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
