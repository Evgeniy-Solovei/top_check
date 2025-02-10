import uuid

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gifts_keyboard():
    # Создаем кнопки
    buttons = [
        [InlineKeyboardButton(text="COMFORT", callback_data="comfort")],
        [InlineKeyboardButton(text="PREMIUM", callback_data="premium")],
        [InlineKeyboardButton(text="EXCLUSIVE", callback_data="exclusive")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def prices_keyboard(prices, tariff, unique_id):
    """Создает клавиатуру с ценами"""
    buttons = [[InlineKeyboardButton(text=f"{price} ₽", callback_data=f"buy_{tariff}_{price}_{unique_id}")] for price in prices]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def payment_keyboard(price, tariff, unique_id):
    """Клавиатура для подтверждения оплаты"""
    buttons = [
        [InlineKeyboardButton(text="✅ Оплатить", callback_data=f"pay_{tariff}_{price}_{unique_id}")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data=f"back_to_tariffs")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

