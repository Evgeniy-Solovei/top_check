from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def balance_keyboard():
    buttons = [
        KeyboardButton(text="Посмотреть"),
        KeyboardButton(text="Пополнить"),
        KeyboardButton(text="Вывести"),
        KeyboardButton(text="Назад"),  # Кнопка для возврата в главное меню
    ]
    builder = ReplyKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
