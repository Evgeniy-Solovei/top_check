from aiogram import Router, types

from aiogram_bot.keyboard.start_keyboard import get_main_keyboard
from top_check_core.models import UserProfile, Referral

router = Router()


@router.message(lambda message: message.contact is not None)
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
            f"- от 100 000 000 рублей, например, За этот Год.\n\n")
        # Убираем клавиатуру с кнопкой "Поделиться номером"
        await message.answer(success_message, reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")
        # Отправляем клавиатуру с кнопками "Подарки", "Баланс", "Продвижение"
        await message.answer("Выберите действие:", reply_markup=await get_main_keyboard())
    except UserProfile.DoesNotExist:
        await message.answer("Вы не зарегистрированы. Используйте реферальную ссылку для регистрации.")
