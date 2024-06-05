import logging
from datetime import datetime

from aiogram import Router, F, types, Bot
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from config.config_data import Config, load_config
from data_base.db_config import session
from data_base.requests.basket_requests import del_basket
from data_base.requests.user_requests import create_user, get_all_admins
from dialogs.user_windows.user_states import UserStates

router = Router()

config: Config = load_config()
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Создание юзера
@router.message(CommandStart())
async def process_start(msg: Message, dialog_manager: DialogManager):
    await create_user(session, msg.from_user.id, msg.from_user.first_name,
                      msg.from_user.last_name, msg.from_user.username)
    await dialog_manager.start(state=UserStates.menu_state, mode=StartMode.RESET_STACK)


# pre checkout  (оплата в течении 10 секунд)
@router.pre_checkout_query(lambda query: True, )
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# успешная оплата
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message, dialog_manager: DialogManager):

    handler = logging.FileHandler(f'user_logs/buy_logs/{datetime.now().strftime("%Y_%m_%d")}_buy.log',
                                  encoding="UTF-8")
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s] %(message)s'))
    logger.addHandler(handler)

    username = message.from_user.first_name
    summ_price = dialog_manager.dialog_data.get('summ_price')
    delivery_price = dialog_manager.dialog_data.get('delivery_price')
    location = dialog_manager.dialog_data.get('location')
    contact = dialog_manager.dialog_data.get('contact')

    products = []
    summer = 0

    for product in dialog_manager.start_data[0]:
        summer += 1
        products.append(f"{summer} - ")
        products.append(product['category'])
        products.append(product['name'])
        if product.get('value'):
            products.append(product['value'])
        products.append(f"{product['price']} ₽\n")

    await message.bot.send_message(message.chat.id,
                                   f"Платеж на сумму {message.successful_payment.total_amount // 100}"
                                   f" {message.successful_payment.currency} прошел успешно!!!\n"
                                   f"Спасибо за покупку! Скоро с вами свяжется наш администратор")
    if delivery_price is not None:
        logger.info(f"Пользователь {username} оплатил заказ на сумму "
                    f"{summ_price} + {delivery_price} ₽, соберите заказ:"
                    f"{' '.join(str(i) for i in products)} и отправьте по адресу Почты России "
                    f"{location}. Для связи с покупателем используйте номер:"
                    f"{contact}")
    else:
        logger.info(f"Пользователь {username} оплатил заказ на сумму "
                    f"{summ_price} ₽, соберите заказ:"
                    f"{' '.join(str(i) for i in products)} и отправьте по адресу СДЭКа "
                    f"{location}. Для связи с покупателем используйте номер:"
                    f"{contact}")

    admins = await get_all_admins(session)
    for admin in admins:
        if delivery_price is not None:
            await message.bot.send_message(
                chat_id=admin.id,
                text=f"Пользователь <b>{username}</b> оплатил заказ на сумму "
                     f"<b>{summ_price} + {delivery_price} ₽</b>, соберите заказ: \n"
                     f"<b>{' '.join(str(i) for i in products)}</b>\nи отправьте по адресу Почты России "
                     f"<b>{location}</b>. Для связи с покупателем используйте номер:\t"
                     f"<b>{contact}</b>"
            )
        else:
            await message.bot.send_message(
                chat_id=admin.id,
                text=f"Пользователь <b>{username}</b> оплатил заказ на сумму "
                     f"<b>{summ_price} ₽</b>, соберите заказ: \n"
                     f"<b>{' '.join(str(i) for i in products)}</b>\nи отправьте по адресу СДЭКа "
                     f"<b>{location}</b>. Для связи с покупателем используйте номер:\t"
                     f"<b>{contact}</b>"
            )

    await del_basket(session, dialog_manager.start_data[1])

    await dialog_manager.start(state=UserStates.menu_state, mode=StartMode.RESET_STACK)

