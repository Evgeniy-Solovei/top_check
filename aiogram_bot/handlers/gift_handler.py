import uuid
from decimal import Decimal
from aiogram import Router, types
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_bot.keyboard.gift_keyboard import gifts_keyboard, prices_keyboard, payment_keyboard
from top_check_core.views import get_user_profile, process_subscription_payment

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


subscription_prices = {
    "comfort": ("COMFORT", [48, 240, 480, 1200, 2400, 4800]),
    "premium": ("PREMIUM", [240, 600, 2400, 6000, 24000, 60000]),
    "exclusive": ("EXCLUSIVE", [1200, 3000, 6000, 15000, 30000, 75000]),
}


@router.callback_query(lambda c: c.data in subscription_prices)
async def show_prices(callback: CallbackQuery):
    """Обрабатывает нажатия на inline-кнопки и показывает цены"""
    name, prices = subscription_prices[callback.data]
    text = f"💎 Тариф **{name}**\nВыберите стоимость подписки:"

    unique_id = str(uuid.uuid4())
    await callback.message.edit_text(text, reply_markup=prices_keyboard(prices, callback.data, unique_id))
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("buy_"))
async def process_purchase(callback: CallbackQuery):
    """Обрабатывает выбор суммы подписки"""
    _, tariff, price, unique_id = callback.data.split("_")  # Разбираем callback_data на части
    text = f"Вы выбрали подписку **{tariff.upper()}** за {price} ₽.\n\nОплатить сейчас?"
    #
    # await callback.message.delete()
    await callback.message.answer(text, reply_markup=payment_keyboard(price, tariff, unique_id))


@router.callback_query(lambda c: c.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery):
    """Обрабатывает оплату подписки"""
    print('***********')
    print(callback.data)
    _, tariff, price, unique_id = callback.data.split("_")
    price = Decimal(price)  # Конвертируем цену в float
    # Получаем пользователя по его user_id с помощью сервиса
    user_id = callback.from_user.id
    user_profile = await get_user_profile(user_id)
    if user_profile:
        # Проверяем, достаточно ли средств с помощью сервиса
        payment_successful = await process_subscription_payment(user_profile, price)
        if payment_successful:
            text = f"✅ Вы успешно оформили подписку **{tariff.upper()}** за {price} ₽."
        else:
            text = (
                f"❌ У вас недостаточно средств для оформления подписки **{tariff.upper()}**.\n"
                "Вы можете пополнить баланс, чтобы продолжить."
            )
            text += "\n\n⬆️ Пополнить баланс"
        await callback.message.edit_text(text, reply_markup=None)  # Убираем кнопки
        await callback.answer()
    else:
        # Если не найден профиль пользователя
        await callback.message.edit_text("❌ Пользователь не найден. Повторите попытку.")
        await callback.answer()
