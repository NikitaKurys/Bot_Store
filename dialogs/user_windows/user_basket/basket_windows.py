import operator

from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.media import StaticMedia

from dialogs.user_windows.user_basket.basket_func import select_checkbox_clicked, delete_basket, to_pay
from dialogs.user_windows.user_basket.basket_getters import display_basket
from dialogs.user_windows.user_states import UserStates, BasketStates
from aiogram_dialog.widgets.kbd import Row, Multiselect, SwitchTo, Group, Cancel, Button
from aiogram_dialog.widgets.text import Const, Format

# Окно корзины
basket_window = Window(
    Format("В вашей корзине находится <b><u>{count}</u></b>\nпродуктов,"
           " общей стоимостью <b><u>{summ}</u></b> ₽\n"
           "выделите нужные товары для их приобретения или удаления", when="is_basket"),
    Format("Ваша корзина пока пуста ☹️", when="not_basket"),
    StaticMedia(
        path="static/images/basket.jpg",
        type=ContentType.PHOTO,
    ),
    Group(
        Multiselect(
            checked_text=Format("✔️ {item[3]} {item[1]} {item[4]} {item[2]} ₽"),
            unchecked_text=Format(" {item[3]} {item[1]} {item[4]} {item[2]} ₽"),
            id="basket",
            item_id_getter=operator.itemgetter(0),
            items="products",
            on_state_changed=select_checkbox_clicked,
            when="products",
        ),
        width=1,
    ),
    Group(
        Button(
            Format("❌Удалить "),
            id='del',
            when="checked",
            on_click=delete_basket
        ),
        Button(
            Format("✅ Купить {summ_price}₽"),
            id="pay",
            when="checked",
            on_click=to_pay
        ),
        width=2,
    ),
    Cancel(Const("◀️ Вернуться"), id="back"),
    getter=display_basket,
    state=BasketStates.menu_state,
)
