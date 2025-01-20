from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Подарки"))
    builder.add(types.KeyboardButton(text="Баланс"))
    builder.add(types.KeyboardButton(text="Продвижение"))
    builder.adjust(1)  # Кнопки располагаются в один столбец
    return builder.as_markup(resize_keyboard=True)


# def get_share_keyboard(referral_link: str):
#     # Создаем кнопку "Поделиться ссылкой"
#     share_button = InlineKeyboardButton(
#         text="Поделиться ссылкой",
#         switch_inline_query=referral_link
#     )
#
#     # Создаем клавиатуру с кнопкой
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[[share_button]])
#     return keyboard
