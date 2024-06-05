from aiogram.enums import ContentType
from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.kbd import Row, Group, Column, Url, Start, SwitchTo
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media import StaticMedia

from dialogs.admin_windows.admin_states import AdminStates
from dialogs.user_windows.user_main.user_getters import get_admin_id
from dialogs.user_windows.user_states import UserStates, ShopStates, BasketStates
from lexicon.lexicon import LEXICON, LEXICON_USER_BTN

# Стартовое меню
menu_window = Window(
    Const(text=LEXICON["/start"]),
    StaticMedia(
        path="static/images/logo.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Row(
            Start(Format(LEXICON_USER_BTN['shop']), id="shop", state=ShopStates.category_states),
            SwitchTo(Format(LEXICON_USER_BTN['about_us']), id="about_us", state=UserStates.about_us_state),
            SwitchTo(Format(LEXICON_USER_BTN["contacts"]), id="contacts", state=UserStates.contacts_state),
            Start(Format(LEXICON_USER_BTN["basket"]), id="basket", state=BasketStates.menu_state),
        ),
        Column(
            Start(Format(LEXICON_USER_BTN["admin"]), id="admin",
                  state=AdminStates.admin_state, when="is_admin", mode=StartMode.NORMAL)
        ),
        width=2,
    ),
    state=UserStates.menu_state,
    getter=get_admin_id,
)

# Окно контактов
contacts_window = Window(
    Const(text=LEXICON["contacts"]),
    StaticMedia(
        path="static/images/contact.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Row(
            Url(text=Const("instagram"), url=Const(LEXICON_USER_BTN["Instagram"]), id="instagram"),
            Url(text=Const("VK"), url=Const(LEXICON_USER_BTN["VK"]), id="VK"),
            Url(text=Const("Whatsapp"), url=Const(LEXICON_USER_BTN["Whatsapp"]), id="whatsapp"),
            Url(text=Const("Telegram"), url=Const(LEXICON_USER_BTN["Telegram"]), id="telegram")
        ),
        width=2,
    ),
    SwitchTo(Const("◀️ Вернуться"), id="back", state=UserStates.menu_state),
    state=UserStates.contacts_state,
)

# Окно информации
about_us_window = Window(
    Const(text=LEXICON["about_us"]),
    StaticMedia(
        path="static/images/about_us.png",
        type=ContentType.PHOTO,
    ),
    SwitchTo(Const("◀️ Вернуться"), id="back", state=UserStates.menu_state),
    state=UserStates.about_us_state,
)
