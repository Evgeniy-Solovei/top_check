from aiogram import Router, types
from aiogram_bot.keyboard.balance_keyboard import balance_keyboard
from top_check_core.models import UserProfile

router = Router()


@router.message(lambda message: message.text == "Баланс")
async def handle_balance(message: types.Message):
    """Обработчик команды 'Баланс'"""
    # Получаем профиль пользователя из базы данных
    user_profile = await UserProfile.objects.filter(user_id=message.from_user.id).afirst()

    if user_profile:
        balance_text = f"{user_profile.balance:,.2f} ₽"  # Форматируем баланс
    else:
        balance_text = "Не найден 😢"

    # Формируем сообщение
    balance_message = (
        f"💰 Ваш текущий баланс: {balance_text}\n"
        f"💰 Доступно к выводу: {balance_text}\n\n"
        "В данном модуле, Вы сможете увидеть Баланс своих подарков, "
        "после чего пополнить или вывести денежные средства на свой Payeer кошелёк."
    )
    await message.answer(balance_message, reply_markup=await balance_keyboard())
