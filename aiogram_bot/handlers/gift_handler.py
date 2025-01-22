from aiogram import Router, types
from aiogram_bot.keyboard.gift_keyboard import gifts_keyboard

router = Router()


@router.message(lambda message: message.text == "Подарки")
async def handle_gifts(message: types.Message):
    gifts_message = (
        "В данном модуле Вы можете выбрать одну или несколько подарочных программ:\n\n"
        "Программа “Comfort” - дарим и получаем возможности получать денежные Подарки каждый час, в режиме 24/7;\n\n"
        "Программа “Premium” - дарим и получаем возможности получать денежные Подарки - Ежемесячно;\n\n"
        "Программа “Exclusive” - дарим и получаем возможности получать денежные Подарки - согласно глубины команды до бесконечности.\n\n"
        "Важно: все денежные транзакции в нашем проекте, это добровольные и безвозмездные Подарки!")
    await message.answer(gifts_message, reply_markup=await gifts_keyboard())
