import re
from pprint import pprint

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedMultiselect, Button

from data_base.db_config import session
from data_base.requests.basket_requests import add_basket, del_basket, get_product_basket
from data_base.requests.product_requests import get_name_product
from dialogs.user_windows.user_states import PayStates


# Добавление кнопки корзины
async def select_checkbox_clicked(callback: CallbackQuery, checkbox: ManagedMultiselect,
                                  dialog_manager: DialogManager, item: str) -> None:
    dialog_manager.dialog_data.update(item=item, clicked=checkbox.is_checked(item))
    summ_price = 0
    products = []

    # Если ничего не выбрано - сбрасываем выделения
    if len(checkbox.get_checked()) == 0:
        del dialog_manager.dialog_data['item']

    # Добавляем выбранные продукты в список
    elif len(checkbox.get_checked()) >= 1:
        for product in checkbox.get_checked():
            products.append(await get_product_basket(session, int(product)))

    # Считаем сумму выбранных продуктов
    for price in products:
        summ_price += int(price['price'])

    dialog_manager.dialog_data.update(summ_price=summ_price, products=products,
                                      checked_item=dialog_manager.find('basket').get_checked())


# Добавить в корзину
async def create_basket(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    check_category = dialog_manager.find('checkbox').is_checked()
    if dialog_manager.dialog_data['category'].lower() == 'духи' and check_category is False:
        dialog_manager.dialog_data.update(category='Масло')
    category = dialog_manager.dialog_data['category']
    product_id = dialog_manager.dialog_data["product_id"]
    name = await get_name_product(session, product_id)
    user_id = callback.from_user.id

    if category.lower() == 'духи' or category.lower() == 'масло':
        value = dialog_manager.dialog_data["item"].split()[0]
        price = dialog_manager.dialog_data["item"].split()[1]
        products = {
            "category": category,
            "price": price.replace(")", ""),
            "value": value.replace("('", "").replace("',", ""),
            "name": name,
        }
        await add_basket(session, user_id, products)
        await callback.answer(text=f"Продукт {name} {products['value']} добавлен")
        await dialog_manager.find("price").reset_checked()

    else:   # В случае, есть продукт не духи и не масло
        price = dialog_manager.dialog_data.get('product_price')
        product = {
            "category": category,
            "name": name,
            "price": price,
        }
        await add_basket(session, user_id, product)
        await callback.answer(text=f"Продукт {name} добавлен")
    dialog_manager.dialog_data.update(clicked=False)


# Удалить продукт с корзины
async def delete_basket(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.answer(await del_basket(session, dialog_manager.find('basket').get_checked()))
    await dialog_manager.find('basket').reset_checked()
    del dialog_manager.dialog_data['item']


# Перейти в покупки
async def to_pay(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(PayStates.select_location_state, data=[dialog_manager.dialog_data['products'],
                                                                      dialog_manager.dialog_data['checked_item']])
