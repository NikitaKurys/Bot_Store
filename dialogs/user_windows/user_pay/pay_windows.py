import operator

from aiogram import F
from aiogram.enums import ContentType
from aiogram.types import KeyboardButton
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, RequestLocation, Button, Row, Select, SwitchTo
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format, List

from dialogs.user_windows.user_pay.pay_func import create_location, create_contact, go_to_puy, go_to_location
from dialogs.user_windows.user_pay.pay_getters import get_check, get_delivery
from dialogs.user_windows.user_states import PayStates
from lexicon.lexicon import LEXICON

# Окно выбора локации
select_location_window = Window(
    StaticMedia(
        path="static/images/delivery.jpg",
        type=ContentType.PHOTO,
    ),
    Format("Выберете способ отправки"),
    Select(
        Format('{item[1]}'),
        id='delivery',
        item_id_getter=operator.itemgetter(1),
        items='delivery',
        on_click=go_to_location,
    ),
    Cancel(Const("◀️ Вернуться"), id="back",),
    getter=get_delivery,
    state=PayStates.select_location_state,
)


# Окно заполнения адреса доставки
location_window = Window(
    Format(f"{LEXICON['location_mail']}", when='mail'),
    Format(f"{LEXICON['location_sdek']}", when='sdek'),
    MessageInput(
        func=create_location,
        content_types=ContentType.TEXT,
    ),
    SwitchTo(Const("◀️ Вернуться"), id='back', state=PayStates.select_location_state),

    getter=get_delivery,
    state=PayStates.location_state,
)

# Окно контактов
contact_window = Window(
    Format(f"{LEXICON['contact']}"),
    MessageInput(
        func=create_contact,
        content_types=ContentType.TEXT,
    ),
    SwitchTo(Const("◀️ Вернуться"), id='back', state=PayStates.location_state),
    state=PayStates.contact_state,
)

# Окно проверки
check_window = Window(
    Format("{username}, Ваши данные:\n"
           "<b>{location}</b>\n"
           "Ваш номер телефона: <b>{contact}</b>\n"
           "Сумма к оплате: <b>{summ_price} ₽</b>"),
    Row(
        Button(Const("✅Верно!"), id='go_to_pay', on_click=go_to_puy),
        SwitchTo(Const('❌Не верно!'), id='back', state=PayStates.select_location_state),
    ),
    getter=get_check,
    state=PayStates.check_state,
)
