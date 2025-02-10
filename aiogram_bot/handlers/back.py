from aiogram import Router, types
from aiogram.types import CallbackQuery

from aiogram_bot.keyboard.gift_keyboard import gifts_keyboard
from aiogram_bot.keyboard.start_keyboard import get_main_keyboard

router = Router()


@router.message(lambda message: message.text == "Назад")
async def handle_back(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=await get_main_keyboard())


@router.callback_query(lambda c: c.data == "back_to_tariffs")
async def back_to_tariffs(callback: types.CallbackQuery):
    """Возвращаемся к выбору тарифов"""
    await callback.message.delete()

    gifts_message = (
        "В данном модуле Вы можете выбрать одну или несколько подарочных программ:\n\n"
        "Программа “Comfort” - дарим и получаем возможности получать денежные Подарки каждый час, в режиме 24/7;\n\n"
        "Программа “Premium” - дарим и получаем возможности получать денежные Подарки - Ежемесячно;\n\n"
        "Программа “Exclusive” - дарим и получаем возможности получать денежные Подарки - согласно глубины команды до бесконечности.\n\n"
        "Важно: все денежные транзакции в нашем проекте, это добровольные и безвозмездные Подарки!")

    # Отправляем сообщение с кнопками
    await callback.message.answer(gifts_message, reply_markup=await gifts_keyboard())
