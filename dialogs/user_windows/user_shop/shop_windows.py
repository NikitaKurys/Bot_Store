import operator

from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import Row, Group, Start, Select, Cancel, Multiselect, \
     StubScroll, Button, Checkbox, FirstPage, PrevPage, CurrentPage, NextPage, LastPage
from aiogram_dialog.widgets.text import Const, Format, Multi

from dialogs.admin_windows.admin_category.category_getters import show_categories
from dialogs.user_windows.user_basket.basket_func import create_basket
from dialogs.user_windows.user_main.main_func import checkbox_clicked, reset_checkbox_clicked
from dialogs.user_windows.user_shop.shop_func import show_products, switch_to_categories, select_clicked, sort_gender
from dialogs.user_windows.user_shop.shop_getters import show_product, select_gender
from dialogs.user_windows.user_states import ShopStates, BasketStates
from lexicon.lexicon import LEXICON

# Меню категорий
category_window = Window(
    Const(text=LEXICON["shop"]),
    StaticMedia(
        path="static/images/shop.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Row(
            Select(
                Format("{item[0]}"),
                id="categ",
                item_id_getter=operator.itemgetter(0),
                items="categories",
                on_click=show_products,
            )
        ), width=3,
    ),
    Cancel(Const("◀️ Вернуться"), id="cancel"),
    state=ShopStates.category_states,
    getter=show_categories
)

# Окно сортировки по гендеру, если это духи
gender_window = Window(
    Const(text='Какие духи интересуют?'),
    StaticMedia(
        path="static/images/shop.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Row(
            Select(
                Format("{item[1]}"),
                id="categ",
                item_id_getter=operator.itemgetter(1),
                items="gender",
                on_click=sort_gender,
            )
        ), width=2,
    ),
    Cancel(Const("◀️ Вернуться"), id="cancel"),
    state=ShopStates.gender_states,
    getter=select_gender,
)

# Меню продуктов
product_window = Window(
    StaticMedia(
        path=Format("{products[img]}"),
        type=ContentType.PHOTO,
    ),
    Multi(
        Format("<b>{products[category]} {products[name]}</b>\n"
               "<b>{products[gender]}</b>\n"
               "{products[description]}\n"
               "{page} товар из {pages}\n"),
        Format('У нас можно приобрести как духи, так и масло\n'
               'Нажмите на "Духи" для просмотра цены "Масла"\n'
               '👇Цена за духи👇', when="checked"),
        Format('У нас можно приобрести как духи, так и масло\n'
               'Нажмите на "Масло" для просмотра цены "Духи"\n'
               '👇Цена за масло👇', when="not_checked"),
        when="add_oil",
    ),
    Multi(
        Format("<b>{products[category]} {products[name]}</b>\n"
               "{products[description]}\n"
               "{page} товар из {pages}\n"),
        when="not_oil"
    ),
    Format("<b>Цена:</b> {products[price]} ₽", when="not_oil"),
    Checkbox(
        checked_text=Format('🌷Духи🌷'),
        unchecked_text=Format('🌹Масло🌹'),
        id='checkbox',
        on_state_changed=checkbox_clicked,
        when='add_oil',
        default=True,
    ),
    Group(
        Multiselect(
            checked_text=Format('🟢 {item[0]} - {item[1]} ₽'),
            unchecked_text=Format('⚪️ {item[0]} - {item[1]} ₽'),
            id='price',
            item_id_getter=operator.itemgetter(0, 1),
            items='add_oil',
            on_state_changed=select_clicked,
            on_click=reset_checkbox_clicked,
            max_selected=1,
        ),
        Button(Format('Добавить в корзину ✔️'), when="clicked", id='basket', on_click=create_basket),
        width=2,
        when='add_oil',
    ),
    Button(Format('Добавить в корзину'), when="not_oil", id='basket', on_click=create_basket),
    Start(Format('🛒Перейти в корзину ({basket})'), id='go_to_basket', state=BasketStates.menu_state),
    Group(
        StubScroll(
            id="stub_scroll",
            pages="pages",
        ),
        width=5,
    ),
    Row(
        FirstPage(
            scroll="stub_scroll", text=Format("⏮️ {target_page1}"),
        ),
        PrevPage(
            scroll="stub_scroll", text=Format("◀️"),
        ),
        CurrentPage(
            scroll="stub_scroll", text=Format("{current_page1}"),
        ),
        NextPage(
            scroll="stub_scroll", text=Format("▶️"),
        ),
        LastPage(
            scroll="stub_scroll", text=Format("{target_page1} ⏭️"),
        ),
    ),
    Button(Const("◀️ Категории"), id="switch", on_click=switch_to_categories),
    state=ShopStates.product_states,
    getter=show_product
)


