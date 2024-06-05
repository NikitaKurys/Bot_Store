import operator

from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Group, Row, Select, SwitchTo, Column, Cancel

from dialogs.admin_windows.admin_logs.logs_func import get_buy_logs, get_subscribers_logs
from dialogs.admin_windows.admin_logs.logs_getters import get_buy_logs_gettr, get_subscribers_logs_gettr
from dialogs.admin_windows.admin_states import AdminLogsStates

# Меню логов
logs_window = Window(
    Format("Выберите логи, которые хотите посмотреть"),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Row(
            SwitchTo(Format('Покупки 💰'), id='buy', state=AdminLogsStates.buy_state),
            SwitchTo(Format('Посещения 👀'), id='subscribers', state=AdminLogsStates.subscribers_state),
        ),
        Column(
            Cancel(Const("◀️ Вернуться"), id="back"),
        ),
        width=2,
    ),
    state=AdminLogsStates.logs_state,
)


# Окно логов покупок
buy_logs_window = Window(
    Format("Выберите нужную дату"),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Select(
            Format('{item[1]}'),
            id='buy_logs',
            item_id_getter=operator.itemgetter(1),
            items='buy_logs',
            on_click=get_buy_logs,
        ),
        width=1,
    ),
    Column(
        Cancel(Const("◀️ Вернуться"), id="back"),
    ),
    getter=get_buy_logs_gettr,
    state=AdminLogsStates.buy_state,
)


# Окно логов пользователей
subscribers_logs_window = Window(
    Format("Выберите нужную дату"),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Select(
            Format('{item[1]}'),
            id='subscribers_logs',
            item_id_getter=operator.itemgetter(1),
            items='subscribers_logs',
            on_click=get_subscribers_logs,
        ),
        width=1,
    ),
    Column(
        Cancel(Const("◀️ Вернуться"), id="back"),
    ),
    getter=get_subscribers_logs_gettr,
    state=AdminLogsStates.subscribers_state,
)
