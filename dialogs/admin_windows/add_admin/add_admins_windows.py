import operator

from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Group, Cancel, Column, Select, Button, SwitchTo

from dialogs.admin_windows.add_admin.add_admins_func import create_admin
from dialogs.admin_windows.add_admin.add_admins_getters import show_admins
from dialogs.admin_windows.admin_states import AddAdminStates

# Показать всех админов
show_admin_window = Window(
    Format("⬇️Администраторы⬇️"),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Select(
            Format('😎Админ - {item[1]}, id - {item[0]}'),
            id='admins',
            item_id_getter=operator.itemgetter(0),
            items='admins',
        ),
        SwitchTo(
            Format('✅Добавить админа'),
            id='add_admin',
            state=AddAdminStates.add_admin_state
        ),
        width=1,
    ),
    Column(
        Cancel(Const("◀️ Вернуться"), id="back"),
    ),
    getter=show_admins,
    state=AddAdminStates.show_admin_state,
)


# Добавить админа
create_admin_window = Window(
    Format(f"Введите id пользователя\n"
           f"ℹ️ @username_to_id_bot здесь можно узнать ID\n"
           f"❗️Перед тем, как дать права администратора пользователю, он должен хоть раз написать нашему боту :)"),
    MessageInput(
        func=create_admin,
        content_types=ContentType.TEXT,
    ),
    Cancel(Const("◀️ Вернуться"), id="back",),
    state=AddAdminStates.add_admin_state,
)
