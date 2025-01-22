from aiogram import Router, types
from aiogram_bot.keyboard.balance_keyboard import balance_keyboard

router = Router()


@router.message(lambda message: message.text == "Баланс")
async def handle_balance(message: types.Message):
    balance_message = (
        "В данном модуле, Вы сможете увидеть Баланс своих подарков, "
        "после чего пополнить или вывести денежные средства на свой Payeer кошелёк.")
    await message.answer(balance_message, reply_markup=await balance_keyboard())
