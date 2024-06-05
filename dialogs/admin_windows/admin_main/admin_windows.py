from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, Row, Column, Cancel, Start
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from dialogs.admin_windows.admin_states import AdminStates, CategoryStates, NewsStates, AdminLogsStates, AddAdminStates
from dialogs.user_windows.user_main.user_getters import get_username
from lexicon.lexicon import LEXICON_ADMIN_BTN


# Начальное меню
menu_window = Window(
    Format("{username}, Добро пожаловать в админку, \nчто планируем делать?"),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Row(
            Start(Format(LEXICON_ADMIN_BTN['categories']), id="categories", state=CategoryStates.category_state),
            Start(Format(LEXICON_ADMIN_BTN['dispatch']), id="news", state=NewsStates.content_state),
            Start(Format(LEXICON_ADMIN_BTN["user_info"]), id="user_info", state=AdminLogsStates.logs_state),
            Start(Format(LEXICON_ADMIN_BTN["set_admin"]), id="set_admin", state=AddAdminStates.show_admin_state),
        ),
        Column(
            Cancel(Const("◀️ Вернуться"), id="back"),
        ),
        width=2,
    ),
    state=AdminStates.admin_state,
    getter=get_username,
)
