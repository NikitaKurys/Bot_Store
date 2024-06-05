from data_base.db_config import session
from data_base.requests.basket_requests import show_basket
from aiogram_dialog import DialogManager


# Показать содержимое корзины
async def display_basket(dialog_manager: DialogManager, **kwargs):
    user_id = kwargs['event_from_user'].id
    checked = dialog_manager.dialog_data.get('item')
    summ_price = dialog_manager.dialog_data.get("summ_price")
    products = []
    is_basket = False
    summ = 0

    for basket in await show_basket(session, user_id):
        summ += int(basket.products["price"])
        if basket.products["category"].lower() == 'духи' or basket.products['category'].lower() == 'масло':
            products.append(
                (
                    basket.id,
                    basket.products["name"],
                    basket.products.get("price"),
                    basket.products["category"],
                    basket.products.get("value")
                )
            )

        else:
            products.append(
                (
                    basket.id,
                    basket.products["name"],
                    basket.products.get("price"),
                    basket.products["category"],
                    "-",
                )
            )

    if products:
        is_basket = True

    count_products = len(products)

    return {
        "products": products,
        "checked": checked,
        "is_basket": is_basket,
        "not_basket": not is_basket,
        "summ": summ,
        "summ_price": summ_price,
        "count": count_products,
    }
