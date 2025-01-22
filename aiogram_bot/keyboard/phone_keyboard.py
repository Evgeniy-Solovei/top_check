from aiogram.types import KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def get_share_phone_keyboard():
    # Создаем кнопки
    buttons = [KeyboardButton(text="Поделиться номером", request_contact=True),]
    builder = ReplyKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
