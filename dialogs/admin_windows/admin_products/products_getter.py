from aiogram_dialog import DialogManager

from data_base.db_config import session
from data_base.requests.product_requests import get_products, get_one_product


async def get_gender(**kwargs):
    genders = [
        ('Мужские', 1),
        ('Женские', 2),
        ('Унисекс', 3),
    ]
    return {'genders': genders}


async def show_products(dialog_manager: DialogManager, **kwargs):
    category = dialog_manager.start_data
    checked = dialog_manager.dialog_data.get('is_checked')
    products = []
    for product in await get_products(session, category):
        products.append(
            (
                product.id,
                product.name,
                round(product.price),
                product.gender,
            )
        )
    return {
            "products": products,
            "category": category,
            "checked": checked,
            "not_checked": not checked
            }


async def get_product(dialog_manager: DialogManager, **kwargs):
    product_id = int(dialog_manager.dialog_data["item"])
    product = await get_one_product(session, product_id)
    return {
        "product": product
    }
