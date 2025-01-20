import django_setup
from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from keyboard import get_main_keyboard
from top_check_core.models import UserProfile


async def handle_gifts(message: types.Message):
    gifts_message = (
        "В данном модуле Вы можете выбрать одну или несколько подарочных программ:\n\n"
        "Программа “Comfort” - дарим и получаем возможности получать денежные Подарки каждый час, в режиме 24/7;\n\n"
        "Программа “Premium” - дарим и получаем возможности получать денежные Подарки - Ежемесячно;\n\n"
        "Программа “Exclusive” - дарим и получаем возможности получать денежные Подарки - согласно глубины команды до бесконечности.\n\n"
        "Важно: все денежные транзакции в нашем проекте, это добровольные и безвозмездные Подарки!"
    )

    # Клавиатура для выбора программы
    gifts_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="COMFORT")],
            [KeyboardButton(text="PREMIUM")],
            [KeyboardButton(text="EXCLUSIVE")],
            [KeyboardButton(text="Назад")],  # Кнопка для возврата в главное меню
        ],
        resize_keyboard=True,
    )

    await message.answer(gifts_message, reply_markup=gifts_keyboard)


async def handle_balance(message: types.Message):
    balance_message = (
        "В данном модуле, Вы сможете увидеть Баланс своих подарков, "
        "после чего пополнить или вывести денежные средства на свой Payeer кошелёк."
    )

    # Клавиатура для работы с балансом
    balance_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Посмотреть")],
            [KeyboardButton(text="Пополнить")],
            [KeyboardButton(text="Вывести")],
            [KeyboardButton(text="Назад")],  # Кнопка для возврата в главное меню
        ],
        resize_keyboard=True,
    )

    await message.answer(balance_message, reply_markup=balance_keyboard)


async def handle_promotion(message: types.Message):
    promotion_message = (
        "В данном модуле, Вы сможете скопировать свою реф.ссылку, "
        "сгенерировать новую, и посмотреть статистику ссылок."
    )

    # Клавиатура для работы с продвижением
    promotion_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Реф.ссылка")],
            [KeyboardButton(text="Сгенерировать")],
            [KeyboardButton(text="Статистика")],
            [KeyboardButton(text="Назад")],  # Кнопка для возврата в главное меню
        ],
        resize_keyboard=True,
    )

    await message.answer(promotion_message, reply_markup=promotion_keyboard)


async def handle_referral_link(message: types.Message):
    user_id = message.from_user.id

    try:
        # Получаем профиль пользователя
        user_profile = await UserProfile.objects.aget(user_id=user_id)
        referral_link = f"https://t.me/TOP_CHECK_Gifts_bot?start={user_profile.user_id}"

        # Сообщение с реферальной ссылкой
        referral_message = (
            f"Ваша реферальная ссылка:\n\n"
            f"{referral_link}\n\n"
            f"Копируй и поделись с другом."
        )

        # # Клавиатура с кнопкой "Поделиться ссылкой"
        # share_keyboard = get_share_keyboard(referral_link)
        #
        await message.answer(referral_message)
    except UserProfile.DoesNotExist:
        await message.answer("Вы не зарегистрированы. Используйте команду /start для регистрации.")


async def handle_back(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=get_main_keyboard())
