from aiogram import Router, types
from aiogram_bot.keyboard.start_keyboard import get_main_keyboard

router = Router()


@router.message(lambda message: message.text == "Назад")
async def handle_back(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=await get_main_keyboard())
