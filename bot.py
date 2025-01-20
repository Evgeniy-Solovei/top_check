import logging
import sys

import django_setup
import asyncio
import os
import django
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
from top_check_core.models import UserProfile, Referral
from handlers import handle_gifts, handle_promotion, handle_back, handle_balance, handle_referral_link
from keyboard import get_main_keyboard


load_dotenv()
TOKEN = os.getenv("TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.message.register(handle_gifts, lambda message: message.text == "Подарки")
dp.message.register(handle_balance, lambda message: message.text == "Баланс")
dp.message.register(handle_promotion, lambda message: message.text == "Продвижение")
dp.message.register(handle_back, lambda message: message.text == "Назад")
dp.message.register(handle_referral_link, lambda message: message.text == "Реф.ссылка")


# Клавиатура с кнопкой "Поделиться номером"
def get_share_phone_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Поделиться номером", request_contact=True))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


# Команда /start с реферальным кодом
@dp.message(CommandStart())
async def handle_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверяем, есть ли реферальный код в команде
    referral_code = None
    if len(message.text.split()) > 1:
        referral_code = message.text.split()[1]

    # Если есть реферальный код, проверяем, не является ли он собственным user_id
    if referral_code:
        if int(referral_code) == user_id:
            await message.answer(
                "Вы не можете использовать свою собственную реферальную ссылку. Вот главное меню:",
                reply_markup=get_main_keyboard()
            )
            return

        try:
            # Создаем или получаем профиль пользователя
            user_profile, created = await UserProfile.objects.aget_or_create(
                user_id=user_id,
                defaults={'username': username}
            )

            # Проверяем, есть ли уже запись в таблице Referral для этого пользователя
            referral_exists = await Referral.objects.filter(referred_user=user_profile).aexists()
            if referral_exists:
                await message.answer(
                    "Вы уже зарегистрированы через реферальную ссылку. Вот главное меню:",
                    reply_markup=get_main_keyboard()
                )
                return

            # Находим пользователя, который пригласил
            referrer = await UserProfile.objects.aget(user_id=int(referral_code))

            # Создаем запись в Referral
            await Referral.objects.acreate(referrer=referrer, referred_user=user_profile)

            # Формируем имя пригласившего
            referrer_name = f"@{referrer.username}" if referrer.username else f"пользователь с ID {referrer.user_id}"

            welcome_message = (
                f"Администрация проекта \"TOP-CHECK\" приветствует тебя!\n\n"
                f"Проект \"TOP-CHECK\" - это подарочная система, где люди дарят денежные подарки, "
                f"и могут получить безлимитное количество денежных подарков согласно нашего уникального маркетинга!\n\n"
                f"Тебя пригласил {referrer_name}\n\n"
                f"Жми кнопку - Поделиться номером и добро пожаловать в наш клуб Друзей!"
            )
            await message.answer(welcome_message, reply_markup=get_share_phone_keyboard())
        except UserProfile.DoesNotExist:
            await message.answer("Неверный реферальный код.")
    else:
        # Если реферального кода нет, проверяем, есть ли пользователь в базе
        try:
            user_profile = await UserProfile.objects.aget(user_id=user_id)
            await message.answer(
                "Вы уже зарегистрированы. Используйте реферальную ссылку для приглашения друзей.",
                reply_markup=get_main_keyboard()
            )
        except UserProfile.DoesNotExist:
            # Если пользователя нет в базе, просто отправляем сообщение
            await message.answer(
                "Для начала работы с ботом используйте реферальную ссылку.",
                reply_markup=get_main_keyboard()
            )


# Обработка номера телефона
@dp.message(lambda message: message.contact is not None)
async def handle_contact(message: types.Message):
    user_id = message.from_user.id
    phone_number = message.contact.phone_number

    try:
        # Получаем профиль пользователя
        user_profile = await UserProfile.objects.aget(user_id=user_id)
        user_profile.phone_number = phone_number
        await user_profile.asave()

        # Получаем информацию о пригласителе
        referral = await Referral.objects.select_related('referrer').filter(referred_user=user_profile).afirst()
        if referral:
            referrer = referral.referrer
            if referrer.username:
                referrer_name = f'<a href="tg://resolve?domain={referrer.username}">@{referrer.username}</a>'
            else:
                referrer_name = f'<a href="tg://user?id={referrer.user_id}">пользователь с ID {referrer.user_id}</a>'
        else:
            referrer_name = "администратор"

        success_message = (
            f"Поздравляем с успешной регистрацией в проекте \"TOP-CHECK\" 🥳🥳🥳🥳🥳\n\n"
            f"Если что-то не понятно, пиши в личку {referrer_name}\n"
            f"Это твой пригласитель и наставник!\n"
            f"Твоя задача — его слушаться и выполнять все рекомендации в пошаговом режиме, "
            f"конечно, лучше всё переспросить и перепроверить у вышестоящих наставников и админов проекта!\n\n"
            f"Желаем тебе много денег:\n"
            f"- от 10 000 рублей Каждый Час;\n"
            f"- от 1 000 000 рублей Ежемесячно;\n"
            f"- от 100 000 000 рублей, например, За этот Год.\n\n"
        )
        # Убираем клавиатуру с кнопкой "Поделиться номером"
        await message.answer(success_message, reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")

        # Отправляем клавиатуру с кнопками "Подарки", "Баланс", "Продвижение"
        await message.answer("Выберите действие:", reply_markup=get_main_keyboard())
    except UserProfile.DoesNotExist:
        await message.answer("Вы не зарегистрированы. Используйте реферальную ссылку для регистрации.")


# Команда /referral
@dp.message(Command("referral"))
async def cmd_referral(message: types.Message):
    user_id = message.from_user.id

    # Получаем профиль пользователя
    user_profile = await UserProfile.objects.aget(user_id=user_id)
    referral_link = f"https://t.me/TOP_CHECK_Gifts_bot?start={user_profile.user_id}"
    await message.answer(f"Ваша реферальная ссылка: {referral_link}")


# async def start_bot():
#     await dp.start_polling(bot)
#
#
# # Запуск бота
# if __name__ == "__main__":
#     print("Скрипт запущен!")
#     main()  # Ваша синхронная функция
#     asyncio.run(start_bot())

async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
