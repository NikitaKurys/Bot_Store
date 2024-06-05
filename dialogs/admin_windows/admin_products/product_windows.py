import operator

from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Row, Column, \
    SwitchTo, Cancel, Back, Select, ScrollingGroup, Multiselect, Button
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from .products_func import remove_product, create_name_product, create_photo_product, create_description_product, \
    create_price_product, create_gender_product, update_name, update_gender_product, update_price, update_photo_product, \
    update_category_product
from .products_getter import get_gender, show_products, get_product
from dialogs.admin_windows.admin_category.category_getters import show_categories
from dialogs.admin_windows.admin_states import ProductStates
from lexicon.lexicon import LEXICON_ADMIN_BTN
from ..admin_main.main_func import checkbox_clicked, reset_checked

# Меню действий с продуктами
product_window = Window(
    Format("Продукты категории <b>{category}</b>\n"
           "Чтобы изменить или удалить продукт нажмите на него"),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        ScrollingGroup(
            Multiselect(
                Format("✓ {item[1]} - {item[3]} - {item[2]}🤑"),
                Format("{item[1]} - {item[3]} - {item[2]}🤑"),
                id='product',
                item_id_getter=operator.itemgetter(0),
                items="products",
                on_state_changed=checkbox_clicked,
                on_click=reset_checked,
                max_selected=1,
            ),
            width=1,
            id="scroll",
            height=2,
        ),
        Group(
            Row(
                Button(Format(LEXICON_ADMIN_BTN['del_product']), id="del_product",
                       when="checked", on_click=remove_product),
                SwitchTo(Format(LEXICON_ADMIN_BTN["update_product"]), id="update_product",
                         state=ProductStates.update_product_state, when="checked"),
                SwitchTo(Format(LEXICON_ADMIN_BTN['add_product']), id="add_product",
                         state=ProductStates.add_name_state),
                Cancel(Const("◀️ Вернуться"), id="back"),
            ),
            width=1,
        ),
    ),
    state=ProductStates.product_state,
    getter=show_products,
)


# Окно добавления имени продукта
add_product_window = Window(
    Const('Введите имя продукта, например "Dior v2"'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=create_name_product,
        content_types=ContentType.TEXT,
    ),
    Column(
        Back(Const("◀️ Вернуться"), id="back"),
    ),
    state=ProductStates.add_name_state,
)

# Окно добавления фото продукта
add_product_photo = Window(
    Const('Скиньте фото продукта'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=create_photo_product,
        content_types=ContentType.PHOTO,
    ),
    Column(
        Back(Const("◀️ Вернуться"), id="back"),
    ),
    state=ProductStates.add_photo_state,
)

# Окно добавления описания продукта
add_product_description = Window(
    Const('Напиши описание продукта, например "Обладает теплой, успокаивающей мягкостью, '
          'которая поднимет вас на вершину мира!"'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=create_description_product,
        content_types=ContentType.TEXT,
    ),
    Column(
        Back(Const("◀️ Вернуться"), id="back"),
    ),
    state=ProductStates.add_description_state,
)


# Окно добавления цены продукта
add_product_price = Window(
    Const('Напиши цену товара за 5 мл духов, далее цену я рассчитаю сам)'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=create_price_product,
        content_types=ContentType.TEXT,
    ),
    Column(
        Back(Const("◀️ Вернуться"), id="back"),
    ),
    state=ProductStates.add_price_state,
)


# Окно выбора гендера продукта
add_product_gender = Window(
    Const('Выберите для кого предназначен товар'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Select(
        Format('{item[0]}'),
        id='gender',
        item_id_getter=operator.itemgetter(0),
        items='genders',
        on_click=create_gender_product,
    ),
    state=ProductStates.add_gender_state,
    getter=get_gender,
)


# Окно изменения продукта
update_product_window = Window(
    Format('Имя - {product[name]}\n'
           'Описание - {product[description]}\n'
           'Гендер - {product[gender]}\n'
           'Цена за 5 мл духов - {product[price]}\n'
           'Категория товара - {product[category_id]}\n'
           '\n<b>Что будем менять?</b>'),
    StaticMedia(
        path=Format("{product[img]}"),
        type=ContentType.PHOTO,
    ),
    Group(
        Row(
            SwitchTo(Format(LEXICON_ADMIN_BTN["update_name"]), id="update_product",
                     state=ProductStates.update_name_state),
            SwitchTo(Format(LEXICON_ADMIN_BTN['update_description']), id="update_description",
                     state=ProductStates.update_description_state),
            SwitchTo(Format(LEXICON_ADMIN_BTN['update_gender']), id="update_gender",
                     state=ProductStates.update_gender_state),
            SwitchTo(Format(LEXICON_ADMIN_BTN['update_price']), id="update_price",
                     state=ProductStates.update_price_state),
            SwitchTo(Format(LEXICON_ADMIN_BTN['update_photo']), id="update_photo",
                     state=ProductStates.update_photo_state),
            SwitchTo(Format(LEXICON_ADMIN_BTN['update_cat']), id="update_category",
                     state=ProductStates.update_category_state),
            Cancel(Const("◀️ Вернуться"), id="back"),
        ),
        width=1,
    ),

    getter=get_product,
    state=ProductStates.update_product_state
)


# Окно изменения имени продукта
update_name_window = Window(
    Format('Сейчас продукт имеет название <b>{product[name]}</b>\n'
           'Введите новое имя продукта, например "Dior v2"'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=update_name,
        content_types=ContentType.TEXT,
    ),
    Column(
        SwitchTo(Const("◀️ Вернуться"), id="back", state=ProductStates.update_product_state),
    ),
    state=ProductStates.update_name_state,
    getter=get_product,
)


# Окно изменения имени продукта
update_description_window = Window(
    Format('Сейчас продукт имеет описание <b>{product[description]}</b>\n'
           'Введите новое описание продукта'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=update_name,
        content_types=ContentType.TEXT,
    ),
    Column(
        SwitchTo(Const("◀️ Вернуться"), id="back", state=ProductStates.update_product_state),
    ),
    state=ProductStates.update_description_state,
    getter=get_product,
)


# Окно изменения гендера продукта
update_product_gender = Window(
    Const('Выберите новый гендер'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Select(
        Format('{item[0]}'),
        id='gender',
        item_id_getter=operator.itemgetter(0),
        items='genders',
        on_click=update_gender_product,
    ),
    state=ProductStates.update_gender_state,
    getter=get_gender,
)


# Окно изменения цены продукта
update_price_window = Window(
    Format('Сейчас продукт имеет цену <b>{product[price]}</b>\n'
           'Введите новую цену продукта'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=update_price,
        content_types=ContentType.TEXT,
    ),
    Column(
        SwitchTo(Const("◀️ Вернуться"), id="back", state=ProductStates.update_product_state),
    ),
    state=ProductStates.update_price_state,
    getter=get_product,
)


# Окно обновления фото продукта
update_product_photo = Window(
    Const('Скиньте новое фото продукта'),
    StaticMedia(
        path=Format("{product[img]}"),
        type=ContentType.PHOTO,
    ),
    MessageInput(
        func=update_photo_product,
        content_types=ContentType.PHOTO,
    ),
    Column(
        SwitchTo(Const("◀️ Вернуться"), id="back", state=ProductStates.update_product_state),
    ),
    state=ProductStates.update_photo_state,
    getter=get_product,
)


# Окно изменения категории продукта
update_product_category = Window(
    Const('Выберите новую категорию'),
    StaticMedia(
        path="static/images/admin.jpg",
        type=ContentType.PHOTO,
    ),
    Select(
        Format('{item[0]}'),
        id='cat',
        item_id_getter=operator.itemgetter(0),
        items='categories',
        on_click=update_category_product,
    ),
    Column(
        SwitchTo(Const("◀️ Вернуться"), id="back", state=ProductStates.update_product_state),
    ),
    state=ProductStates.update_category_state,
    getter=show_categories,
)
