import operator

from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Group, Row, Column, \
    Back, Select, SwitchTo, Multiselect, Cancel
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from .category_func import new_category, remove_category, new_name_category
from .category_getters import show_categories
from dialogs.admin_windows.admin_states import CategoryStates
from lexicon.lexicon import LEXICON_ADMIN_BTN
from ..admin_main.main_func import switch_to_products, checkbox_clicked, reset_checked

# Меню действий с категориями
category_window = Window(
    Format("Что будем делать с категориями?"),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Row(
            Select(
                Format("Категория {item[0]} ({item[1]})"),
                id="categ",
                item_id_getter=operator.itemgetter(0),
                items="categories",
                on_click=switch_to_products,
            )
        ), width=1,
    ),
    Group(
        Row(
            SwitchTo(Format(LEXICON_ADMIN_BTN['add_category']), id="add_category",
                     state=CategoryStates.add_category_state),
            SwitchTo(Format(LEXICON_ADMIN_BTN['del_category']), id="del_category",
                     state=CategoryStates.del_category_state),
            SwitchTo(Format(LEXICON_ADMIN_BTN["update_category"]), id="update_category",
                     state=CategoryStates.update_category_state),
        ),
        Column(
            Cancel(Const("◀️ Вернуться"), id="cancel"),
        ),
        width=2,
    ),
    state=CategoryStates.category_state,
    getter=show_categories,
)

# Окно создания категории
add_category_window = Window(
    Const('Введите имя категории, например "Духи"'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=new_category,
        content_types=ContentType.TEXT,
    ),
    Column(
        Back(Const("◀️ Вернуться"), id="back"),
    ),
    state=CategoryStates.add_category_state,
)


# Окно удаления категории
del_category_window = Window(
    Const("Нажмите на категорию, которую хотите удалить"),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Row(
            Multiselect(
                    checked_text=Format("[✔️] {item[0]}"),
                    unchecked_text=Format("[ ] {item[0]}"),
                    id="categ",
                    item_id_getter=operator.itemgetter(0),
                    items="categories",
                    on_state_changed=checkbox_clicked,
                    on_click=reset_checked,
                    max_selected=1,
                    ),
        ), width=1,
    ),
    Column(
        SwitchTo(Const("◀️ Вернуться"), id="back", state=CategoryStates.category_state),
        Button(Const("❌Удалить"), id="delete", when="checked", on_click=remove_category),
    ),
    state=CategoryStates.del_category_state,
    getter=show_categories,
)

# Окно обновления категории
update_category_window = Window(
    Const("Нажмите на категорию, которую хотите переименовать"),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Row(
            Multiselect(
                    checked_text=Format("[✔️] {item[0]}"),
                    unchecked_text=Format("[ ] {item[0]}"),
                    id="categ",
                    item_id_getter=operator.itemgetter(0),
                    items="categories",
                    on_state_changed=checkbox_clicked,
                    on_click=reset_checked,
                    max_selected=1,
                    ),
        ), width=1,
    ),
    Column(
        SwitchTo(Const("◀️ Вернуться"), id="back", state=CategoryStates.category_state),
        SwitchTo(Const("Переименовать"), id="update", when="checked", state=CategoryStates.rename_category_state),
    ),
    state=CategoryStates.update_category_state,
    getter=show_categories,
)


# Окно замены имени категории
rename_category_window = Window(
    Const('Введите новое имя категории'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=new_name_category,
        content_types=ContentType.TEXT,
    ),
    Column(
        Back(Const("◀️ Вернуться"), id="back"),
    ),
    state=CategoryStates.rename_category_state,
)
