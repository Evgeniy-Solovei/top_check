from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram_bot.keyboard.phone_keyboard import get_share_phone_keyboard
from aiogram_bot.keyboard.start_keyboard import get_main_keyboard
from top_check_core.models import UserProfile, Referral

router = Router()


@router.message(Command("start"))
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
                reply_markup=await get_main_keyboard())
            return
        try:
            # Проверяем, существует ли реферер
            referrer = await UserProfile.objects.aget(user_id=int(referral_code))
        except UserProfile.DoesNotExist:
            # Если реферер не найден, отправляем сообщение и завершаем выполнение
            await message.answer("Неверный реферальный код.")
            return  # Важно: завершаем выполнение функции
        # Получаем или создаем профиль пользователя
        user_profile, created = await UserProfile.objects.aget_or_create(
            user_id=user_id, username=username)
        # Если пользователь только что создан (created = True), то добавляем реферера
        if created:
            # Создаем запись в Referral
            await Referral.objects.acreate(referrer=referrer, referred_user=user_profile)
            # Формируем имя пригласившего
            referrer_name = f"@{referrer.username}" if referrer.username else f"пользователь с ID {referrer.user_id}"
            welcome_message = (
                f"Администрация проекта \"TOP-CHECK\" приветствует тебя!\n\n"
                f"Проект \"TOP-CHECK\" - это подарочная система, где люди дарят денежные подарки, "
                f"и могут получить безлимитное количество денежных подарков согласно нашего уникального маркетинга!\n\n"
                f"Тебя пригласил {referrer_name}\n\n"
                f"Жми кнопку - Поделиться номером и добро пожаловать в наш клуб Друзей!")
            await message.answer(welcome_message, reply_markup=await get_share_phone_keyboard())
        else:
            # Если пользователь уже был зарегистрирован, не добавляем реферера
            await message.answer(
                "Вы уже зарегистрированы. Реферальная ссылка не может быть применена.",
                reply_markup=await get_main_keyboard())
    else:
        # Если реферального кода нет, проверяем, есть ли пользователь в базе
        try:
            user_profile = await UserProfile.objects.aget(user_id=user_id)
            await message.answer(
                "Вы уже зарегистрированы. Используйте реферальную ссылку для приглашения друзей.",
                reply_markup=await get_main_keyboard())
        except UserProfile.DoesNotExist:
            # Если пользователя нет в базе, просто отправляем сообщение
            await message.answer(
                "Для начала работы с ботом используйте реферальную ссылку.",
                reply_markup=await get_main_keyboard())
