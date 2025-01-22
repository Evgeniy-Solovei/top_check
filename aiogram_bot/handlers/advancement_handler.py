from urllib.parse import quote, unquote

from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_bot.keyboard.advancement_keyboard import promotion_keyboard
from top_check_core.models import UserProfile
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = Router()


@router.message(lambda message: message.text == "Продвижение")
async def handle_promotion(message: types.Message):
    promotion_message = (
        "В данном модуле, Вы сможете скопировать свою реф.ссылку, "
        "сгенерировать новую, и посмотреть статистику ссылок.")

    await message.answer(promotion_message, reply_markup=await promotion_keyboard())


# @router.message(lambda message: message.text == "Реф.ссылка")
# async def handle_referral_link(message: types.Message):
#     user_id = message.from_user.id
#
#     try:
#         # Получаем профиль пользователя
#         user_profile = await UserProfile.objects.aget(user_id=user_id)
#         referral_link = f"https://t.me/TOP_CHECK_Gifts_bot?start={user_profile.user_id}"
#         # Сообщение с реферальной ссылкой
#         referral_message = (
#             f"Ваша реферальная ссылка:\n\n"
#             f"{referral_link}\n\n"
#             f"Копируй и поделись с другом.")
#
#         await message.answer(referral_message)
#     except UserProfile.DoesNotExist:
#         await message.answer("Вы не зарегистрированы. Используйте команду /start для регистрации.")


@router.message(lambda message: message.text == "Реф.ссылка")
async def handle_referral_link(message: types.Message):
    user_id = message.from_user.id
    referral_link = f"https://t.me/TOP_CHECK_Gifts_bot?start={user_id}"

    # Сообщение с реферальной ссылкой и текстом
    referral_message = (
        f"Присоединяйся к TOP-CHECK через мою реферальную ссылку!\n\n"
        f"{referral_link}\n\n"
        f"Поделись с другом, чтобы он тоже участвовал!"
    )

    # Создаем inline-кнопку "Поделиться ссылкой"
    share_button = InlineKeyboardButton(
        text="Поделиться ссылкой",
        url=f"https://t.me/share/url?url={referral_link}&text=Присоединяйся к TOP-CHECK!"
    )

    # Создаем клавиатуру с кнопкой
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[share_button]])

    # Отправляем сообщение с текстом и кнопкой
    await message.answer(referral_message, reply_markup=keyboard)
